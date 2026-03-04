import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from app.config import settings
from app.models.state import WorkflowState


class PDFGenerator:
    def __init__(self):
        self.output_dir = settings.PDF_OUTPUT_DIR
        self.styles = getSampleStyleSheet()

        self.title_style = ParagraphStyle(
            "CustomTitle", parent=self.styles["Heading1"],
            fontSize=22, spaceAfter=16, textColor=colors.HexColor("#1a1a2e"),
            alignment=TA_CENTER,
        )
        self.heading_style = ParagraphStyle(
            "CustomHeading", parent=self.styles["Heading2"],
            fontSize=15, spaceBefore=18, spaceAfter=8,
            textColor=colors.HexColor("#16213e"), borderPadding=(4, 0, 4, 0),
        )
        self.sub_heading = ParagraphStyle(
            "CustomSubHeading", parent=self.styles["Heading3"],
            fontSize=12, spaceBefore=10, spaceAfter=6,
            textColor=colors.HexColor("#0f3460"),
        )
        self.normal_style = ParagraphStyle(
            "CustomNormal", parent=self.styles["Normal"],
            fontSize=10, leading=14, spaceAfter=6,
            alignment=TA_JUSTIFY,
        )
        self.bullet_style = ParagraphStyle(
            "BulletItem", parent=self.normal_style,
            leftIndent=24, bulletIndent=12,
            spaceAfter=4, spaceBefore=2,
        )
        self.gap_title_style = ParagraphStyle(
            "GapTitle", parent=self.heading_style,
            fontSize=16, spaceBefore=12, spaceAfter=10,
            textColor=colors.HexColor("#e94560"),
        )
        self.meta_style = ParagraphStyle(
            "MetaInfo", parent=self.normal_style,
            fontSize=8, textColor=colors.HexColor("#666666"),
            alignment=TA_CENTER, spaceBefore=12,
        )


    def _c(self, text: str) -> str:
        """Escape XML-sensitive characters for ReportLab."""
        if not text:
            return "N/A"
        t = str(text)
        for old, new in [("&", "&amp;"), ("<", "&lt;"), (">", "&gt;")]:
            t = t.replace(old, new)
        return t

    def _md_to_paragraphs(self, text: str, story: list):
        """Convert markdown-ish LLM output into a list of ReportLab Paragraphs.

        Handles: **bold**, numbered lists, bullet lists (- or *), headings, and
        plain paragraphs. Each logical block becomes its own Paragraph so that
        ReportLab can lay them out and paginate properly.
        """
        if not text:
            return

        lines = text.split("\n")
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                story.append(Spacer(1, 4))
                continue

            line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
            line = line.replace("&", "&amp;")

            if line.startswith("## ") or line.startswith("### "):
                clean = re.sub(r"^#+\s*", "", line)
                story.append(Paragraph(clean, self.sub_heading))

            elif re.match(r"^\d+\.\s", line):
                content = re.sub(r"^\d+\.\s*", "", line)
                story.append(Paragraph(f"• {content}", self.bullet_style))

            elif line.startswith("- ") or line.startswith("* "):
                content = line[2:]
                story.append(Paragraph(f"• {content}", self.bullet_style))

            else:
                story.append(Paragraph(line, self.normal_style))

    def _authors_str(self, authors) -> str:
        if not authors:
            return "N/A"
        parts = []
        for a in authors:
            name = a.name if hasattr(a, "name") else a.get("name", "")
            aff = a.affiliation if hasattr(a, "affiliation") else a.get("affiliation", "")
            parts.append(f"{name} ({aff})" if aff else name)
        return ", ".join(parts)

    def _add_section_header(self, story, title, style=None):
        """Add a visually distinct section header with a colored rule."""
        style = style or self.heading_style
        story.append(Spacer(1, 8))
        story.append(HRFlowable(
            width="100%", thickness=1.5,
            color=colors.HexColor("#3b82f6"), spaceAfter=6,
        ))
        story.append(Paragraph(title, style))

    def _add_research_gaps_section(self, story, gaps_text: str):
        """Render research gaps as a prominent, well-formatted section."""
        if not gaps_text or not gaps_text.strip():
            return

        story.append(PageBreak())

        banner_data = [["Research Gaps & Future Directions"]]
        banner = Table(banner_data, colWidths=[6.5 * inch])
        banner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#e94560")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 16),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(banner)
        story.append(Spacer(1, 14))

        self._md_to_paragraphs(gaps_text, story)

    def _add_mermaid_image_section(self, story, img_path: str, title: str = "Workflow Diagram"):
        """Render a downloaded mermaid JS image safely into the PDF, scaling it to fit."""
        if not img_path or not os.path.exists(img_path):
            return

        self._add_section_header(story, title)
        
        try:
            max_width = 6.5 * inch
            max_height = 8 * inch

            img = Image(img_path)
            iw, ih = img.drawWidth, img.drawHeight
            if iw > max_width:
                img.drawHeight = ih * (max_width / float(iw))
                img.drawWidth = max_width
            if img.drawHeight > max_height:
                img.drawWidth = img.drawWidth * (max_height / float(img.drawHeight))
                img.drawHeight = max_height
                
            img.hAlign = 'CENTER'
            story.append(KeepTogether([img]))
            story.append(Spacer(1, 12))
        except Exception as e:
            import logging
            logging.error(f"Failed to add image {img_path} to PDF: {e}")


    def generate_best_paper_pdf(self, state: WorkflowState) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"best_paper_{ts}.pdf")
        doc = SimpleDocTemplate(
            filepath, pagesize=letter,
            leftMargin=0.75 * inch, rightMargin=0.75 * inch,
            topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        )
        story = []

        story.append(Paragraph("Best Research Paper Report", self.title_style))
        story.append(HRFlowable(
            width="80%", thickness=2, color=colors.HexColor("#3b82f6"),
            spaceAfter=8, hAlign="CENTER",
        ))
        story.append(Paragraph(
            f"Query: <i>{self._c(state.get('query', ''))}</i>", self.normal_style,
        ))
        story.append(Spacer(1, 12))

        best = state.get("best_paper")
        if best:
            story.append(Paragraph(f"Title: {self._c(best.title)}", self.heading_style))
            story.append(Spacer(1, 6))
            story.append(Paragraph(
                f"<b>Authors:</b> {self._c(self._authors_str(best.authors))}",
                self.normal_style,
            ))
            if best.university:
                story.append(Paragraph(
                    f"<b>University:</b> {self._c(best.university)}", self.normal_style,
                ))
            if best.journal:
                story.append(Paragraph(
                    f"<b>Journal:</b> {self._c(best.journal)}", self.normal_style,
                ))
            story.append(Paragraph(
                f"<b>Year:</b> {best.year or 'N/A'} | <b>Citations:</b> {best.citationCount or 0}",
                self.normal_style,
            ))
            story.append(Spacer(1, 8))

            self._add_section_header(story, "Score Breakdown")
            score_data = [
                ["Metric", "Score"],
                ["Similarity", f"{best.similarity:.4f}"],
                ["Citation Score", f"{best.citation_score:.4f}"],
                ["Recency Score", f"{best.recency_score:.4f}"],
                ["Novelty Score", f"{best.novelty_score:.4f}"],
                ["Final Score", f"{best.final_score:.4f}"],
            ]
            t = Table(score_data, colWidths=[2.5 * inch, 1.5 * inch])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e8f4f8")),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#94a3b8")),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#f8fafc")]),
            ]))
            story.append(t)
            story.append(Spacer(1, 12))

            self._add_section_header(story, "Abstract")
            story.append(Paragraph(self._c(best.abstract), self.normal_style))
            story.append(Spacer(1, 12))

            if best.methodology:
                self._add_section_header(story, "Methodology")
                story.append(Paragraph(self._c(best.methodology), self.normal_style))
                story.append(Spacer(1, 12))
                
                best_img = state.get("best_paper_mermaid_img")
                if best_img:
                    self._add_mermaid_image_section(story, best_img, "Methodology Workflow")

        summary = state.get("best_paper_summary", "")
        if summary:
            self._add_section_header(story, "Detailed Summary & Analysis")
            self._md_to_paragraphs(summary, story)
            story.append(Spacer(1, 12))

        gaps = state.get("research_gaps", "")
        self._add_research_gaps_section(story, gaps)

        story.append(Spacer(1, 20))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
            f"AI Research Synthesis Engine v2.0",
            self.meta_style,
        ))
        doc.build(story)
        return filepath

    def generate_combined_pdf(self, state: WorkflowState) -> str:
        """Merged PDF of ALL retrieved papers with details."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"merged_papers_{ts}.pdf")
        doc = SimpleDocTemplate(
            filepath, pagesize=letter,
            leftMargin=0.75 * inch, rightMargin=0.75 * inch,
            topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        )
        story = []

        story.append(Paragraph("Merged Research Papers Report", self.title_style))
        story.append(HRFlowable(
            width="80%", thickness=2, color=colors.HexColor("#3b82f6"),
            spaceAfter=8, hAlign="CENTER",
        ))
        story.append(Paragraph(
            f"Query: <i>{self._c(state.get('query', ''))}</i>", self.normal_style,
        ))
        story.append(Spacer(1, 12))

        cs = state.get("combined_summary", "")
        if cs:
            self._add_section_header(story, "Combined Research Synthesis")
            self._md_to_paragraphs(cs, story)
            story.append(Spacer(1, 12))
            
            comb_img = state.get("combined_mermaid_img")
            if comb_img:
                self._add_mermaid_image_section(story, comb_img, "Synthesis Workflow")

        scores = state.get("scores", [])
        papers = scores if scores else (state.get("papers") or [])

        for i, p in enumerate(papers, 1):
            story.append(PageBreak())
            paper_num_style = ParagraphStyle(
                f"PaperNum{i}", parent=self.heading_style,
                textColor=colors.HexColor("#3b82f6"),
            )
            story.append(Paragraph(f"Paper {i}: {self._c(p.title)}", paper_num_style))
            story.append(HRFlowable(
                width="100%", thickness=1, color=colors.HexColor("#e2e8f0"),
                spaceAfter=6,
            ))
            story.append(Paragraph(
                f"<b>Authors:</b> {self._c(self._authors_str(p.authors))}",
                self.normal_style,
            ))
            if hasattr(p, "university") and p.university:
                story.append(Paragraph(
                    f"<b>University:</b> {self._c(p.university)}", self.normal_style,
                ))
            if hasattr(p, "journal") and p.journal:
                story.append(Paragraph(
                    f"<b>Journal:</b> {self._c(p.journal)}", self.normal_style,
                ))
            y = p.year or "N/A"
            c = p.citationCount or 0
            story.append(Paragraph(
                f"<b>Year:</b> {y} | <b>Citations:</b> {c}", self.normal_style,
            ))

            if hasattr(p, "final_score"):
                score_data = [
                    ["Similarity", "Citation", "Recency", "Novelty", "Final"],
                    [
                        f"{p.similarity:.4f}",
                        f"{p.citation_score:.4f}",
                        f"{p.recency_score:.4f}",
                        f"{p.novelty_score:.4f}",
                        f"{p.final_score:.4f}",
                    ],
                ]
                st = Table(score_data, colWidths=[1.2 * inch] * 5)
                st.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#94a3b8")),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]))
                story.append(Spacer(1, 6))
                story.append(st)
            story.append(Spacer(1, 8))

            story.append(Paragraph("<b>Abstract:</b>", self.normal_style))
            story.append(Paragraph(self._c(p.abstract or "N/A"), self.normal_style))
            story.append(Spacer(1, 6))

            if hasattr(p, "methodology") and p.methodology:
                story.append(Paragraph("<b>Methodology:</b>", self.normal_style))
                story.append(Paragraph(self._c(p.methodology), self.normal_style))

            story.append(Spacer(1, 12))

        gaps = state.get("research_gaps", "")
        self._add_research_gaps_section(story, gaps)

        story.append(Spacer(1, 20))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
            f"AI Research Synthesis Engine v2.0",
            self.meta_style,
        ))
        doc.build(story)
        return filepath
