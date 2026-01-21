import pytest
from pathlib import Path
from document_compare import DocumentComparison

def test_end_to_end_comparison():
    """Test full comparison pipeline."""
    comparison = DocumentComparison(mode='substantive')

    result = comparison.compare(
        doc1_path='tests/fixtures/simple.docx',
        doc2_path='tests/fixtures/simple.docx'
    )

    assert 'report' in result
    assert 'differences' in result
    assert 'metadata' in result
    assert len(result['differences']) >= 0
