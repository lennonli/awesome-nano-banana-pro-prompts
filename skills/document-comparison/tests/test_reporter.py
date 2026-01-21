import pytest
from pathlib import Path
from core.reporter import ReportGenerator

def test_generate_markdown_report():
    """Test that reporter generates markdown report."""
    generator = ReportGenerator()

    differences = [
        {
            'type': 'numeric',
            'text1': '100',
            'text2': '101',
            'description': 'Numeric values differ',
            'risk_level': 'medium'
        }
    ]

    metadata = {
        'doc1_file': 'securities_firm.docx',
        'doc2_file': 'legal_counsel.docx',
        'mode': 'substantive'
    }

    report = generator.generate_report(differences, metadata, format='markdown')

    assert '# Document Comparison Report' in report
    assert '## Overview' in report
    assert '## Differences' in report
    assert '100' in report
    assert '101' in report
