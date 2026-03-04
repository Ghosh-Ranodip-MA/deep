import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Research Synthesis Engine", layout="wide", page_icon="🔬")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.markdown("""
<style>
.paper-card {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    padding: 1.2rem; border-radius: 12px; margin: 0.5rem 0;
    border-left: 4px solid #3b82f6; color: #e2e8f0;
}
.score-badge {
    background: #3b82f6; color: white; padding: 4px 12px;
    border-radius: 20px; font-weight: bold; font-size: 0.9rem;
}
.best-badge {
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: white; padding: 4px 14px; border-radius: 20px;
    font-weight: bold; font-size: 0.9rem;
}
.history-item {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.5rem; border-radius: 8px; margin: 0.3rem 0;
    border-left: 3px solid #3b82f6;
    background: #1e293b;
}
.stat-box {
    background: #1e293b; padding: 1rem; border-radius: 8px;
    text-align: center; margin-bottom: 1rem;
    border: 1px solid #334155;
}
.stat-value {
    font-size: 1.8rem; font-weight: 800; color: #3b82f6;
}
.stat-label {
    font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


def render_results(data, prefix=""):
    """Render research results (shared between live query and history view)."""
    status = data.get("status", "unknown")

    if status == "no_papers_found" or not data.get("papers"):
        st.warning("⚠️ No matching papers were found for this query.")
        st.info("Try modifying your search keywords. If you are querying frequently, you may also have hit an API rate limit.")
        if data.get("combined_summary"):
            st.markdown(data["combined_summary"])
        return

    best = data.get("best_paper")
    if best:
        st.header("Best Research Paper")
        if best.get("url"):
            st.markdown(f"### [{best.get('title', 'N/A')}]({best.get('url')})")
        else:
            st.markdown(f"### {best.get('title', 'N/A')}")

        authors = best.get("authors", [])
        author_str = ", ".join(
            f"**{a.get('name', '')}** ({a.get('affiliation', '')})"
            for a in authors
        )
        if author_str:
            st.markdown(f"**Authors:** {author_str}")

        cols = st.columns(5)
        cols[0].metric("Final Score", f"{best.get('final_score', 0):.4f}")
        cols[1].metric("Similarity", f"{best.get('similarity', 0):.4f}")
        cols[2].metric("Citations", best.get("citationCount", 0))
        cols[3].metric("Year", best.get("year", "N/A"))
        cols[4].metric("Novelty", f"{best.get('novelty_score', 0):.4f}")

        if best.get("university"):
            st.markdown(f"**University:** {best['university']}")
        if best.get("journal"):
            st.markdown(f"**Journal:** {best['journal']}")

    if data.get("best_paper_summary"):
        st.header("Best Paper Summary (Abstract & Methodology)")
        st.info(data["best_paper_summary"])

    papers = data.get("papers", [])
    if papers:
        st.header(f"All Retrieved Papers ({len(papers)})")
        for i, p in enumerate(papers):
            score = p.get("final_score", 0)
            badge = "[BEST] " if i == 0 else ""
            with st.expander(f"{badge}{p.get('title', 'N/A')} — Score: {score:.4f}", expanded=False):
                pauthors = p.get("authors", [])
                pauthor_str = ", ".join(
                    f"{a.get('name', '')} ({a.get('affiliation', '')})"
                    for a in pauthors
                )
                st.markdown(f"**Authors:** {pauthor_str or 'N/A'}")
                st.markdown(f"**University:** {p.get('university', 'N/A')} | **Journal:** {p.get('journal', 'N/A')}")
                st.markdown(f"**Year:** {p.get('year', 'N/A')} | **Citations:** {p.get('citationCount', 0)}")

                sc = st.columns(4)
                sc[0].metric("Similarity", f"{p.get('similarity', 0):.4f}")
                sc[1].metric("Citation Score", f"{p.get('citation_score', 0):.4f}")
                sc[2].metric("Recency", f"{p.get('recency_score', 0):.4f}")
                sc[3].metric("Novelty", f"{p.get('novelty_score', 0):.4f}")

                if p.get("abstract"):
                    st.markdown("**Abstract:**")
                    st.markdown(f"> {p['abstract']}")
                if p.get("methodology"):
                    st.markdown("**Methodology:**")
                    st.markdown(f"> {p['methodology']}")
                if p.get("url"):
                    st.markdown(f"**[🔗 Read Full Paper on OpenAlex]({p.get('url')})**")

    if data.get("combined_summary"):
        st.header("Combined Research Synthesis")
        st.success(data["combined_summary"])

    if data.get("research_gaps"):
        st.header("Research Gaps & Future Directions")
        st.error(data["research_gaps"])

    pdf_paths = data.get("pdf_paths", [])
    if pdf_paths:
        st.header("Download Reports")
        for pdf_path in pdf_paths:
            pdf_name = os.path.basename(pdf_path)
            pdf_url = f"{BACKEND_URL}/api/pdf?path={pdf_path}"
            try:
                pdf_resp = requests.get(pdf_url, timeout=10)
                if pdf_resp.status_code == 200:
                    label = "Best Paper Report" if "best_paper" in pdf_name else "Merged Papers Report"
                    st.download_button(
                        label=f"{label} ({pdf_name})",
                        data=pdf_resp.content,
                        file_name=pdf_name,
                        mime="application/pdf",
                        key=f"{prefix}{pdf_name}",
                    )
            except Exception:
                st.write(f"Could not load PDF: {pdf_name}")


with st.sidebar:
    st.header("Query History")
    try:
        hist_resp = requests.get(f"{BACKEND_URL}/api/history", timeout=5)
        if hist_resp.status_code == 200:
            hist_data = hist_resp.json()
            history_items = hist_data.get("history", [])
            if history_items:
                for item in history_items:
                    hid = item["id"]
                    hquery = item["query"]
                    htime = item.get("created_at", "")[:16].replace("T", " ")
                    pcount = item.get("paper_count", 0)
                    
                    icon = "✅" if item.get("status") == "completed" else "❌"
                    
                    st.markdown('<div class="history-item">', unsafe_allow_html=True)
                    hc1, hc2 = st.columns([0.8, 0.2])
                    
                    with hc1:
                        if st.button(
                            f"{icon} {hquery[:40]}{'...' if len(hquery) > 40 else ''}\n",
                            key=f"hist_btn_{hid}",
                            use_container_width=True,
                            help=f"Queried: {htime}"
                        ):
                            st.session_state["view_history_id"] = hid
                            st.session_state["view_history_query"] = hquery
                            
                    with hc2:
                        if st.button("🗑️", key=f"del_btn_{hid}", help="Delete this query history"):
                            try:
                                requests.delete(f"{BACKEND_URL}/api/history/{hid}", timeout=5)
                                st.rerun()
                            except Exception as e:
                                st.error("Failed to delete")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.caption("No past queries yet. Run a search to start building history.")
        else:
            st.caption("Could not load history")
    except Exception:
        st.caption("Backend not connected")

    st.divider()
    st.subheader("About")
    st.markdown("""
    **AI Research Synthesis Engine** helps anyone find, read, and understand academic research! 
    
    Just type what you're curious about—like "polar bears", "climate change", or "deep learning"—and we will automatically search OpenAlex for the best research papers, summarize them, and highlight gaps in current knowledge for you.
    """)


st.title("AI Research Synthesis Engine")

if st.session_state.get("view_history_id"):
    hid = st.session_state["view_history_id"]
    hquery = st.session_state.get("view_history_query", "")
    st.info(f"Viewing past query: **{hquery}**")

    if st.button("Back to New Search", type="secondary"):
        del st.session_state["view_history_id"]
        if "view_history_query" in st.session_state:
            del st.session_state["view_history_query"]
        st.rerun()

    try:
        r = requests.get(f"{BACKEND_URL}/api/history/{hid}", timeout=10)
        if r.status_code == 200:
            hist_record = r.json()
            st.caption(f"Queried at: {hist_record.get('created_at', 'N/A')}")
            render_results(hist_record, prefix=f"hist{hid}_")
        else:
            st.error("Could not load this history record.")
    except Exception as e:
        st.error(f"Error loading history: {e}")

else:
    st.markdown("Enter a research topic to retrieve similar papers, analyze gaps, and generate reports.")
    query = st.text_input("Research Query", placeholder="e.g., Deep learning for medical image analysis")

    if st.button("Run Research Analysis", type="primary", use_container_width=True):
        if not query.strip():
            st.warning("Please enter a research topic.")
        else:
            with st.spinner("Running research pipeline... (planning → retrieval → scoring → summarization → PDF generation)"):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/api/research",
                        json={"query": query}, timeout=300
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Research analysis completed!")
                        render_results(data, prefix="live_")
                    elif response.status_code == 500 and "rate_limit_exceeded" in response.text:
                        st.error("Error: Rate limit exceeded. The API has received too many requests in a short period. Please wait a moment before trying again.")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to backend. Make sure it's running on port 8000.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")