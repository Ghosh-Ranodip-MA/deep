"""Tests for PDF generation."""

import pytest
import os
from app.pdf.pdf_generator import pdf_generator


def test_generate_report(tmp_path):
    """Test PDF report generation."""
    research_data = {
        "title": "Test Research",
        "content": "This is test content",
        "findings": ["Finding 1", "Finding 2"],
    }

    original_dir = pdf_generator.output_dir
    pdf_generator.output_dir = str(tmp_path)

    report_path = pdf_generator.generate_report(research_data, title="Test Report")

    assert report_path is not None
    assert "test" in report_path.lower() or "report" in report_path.lower()

    pdf_generator.output_dir = original_dir


if __name__ == "__main__":
    pytest.main([__file__])
