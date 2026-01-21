import pytest
from pathlib import Path
from core.parser import DocumentParser

def test_parse_document_structure():
    """Test that parser extracts paragraphs, tables, and lists correctly."""
    parser = DocumentParser()
    result = parser.parse_document("tests/fixtures/simple.docx")

    assert result is not None
    assert 'paragraphs' in result
    assert 'tables' in result
    assert 'metadata' in result
    assert len(result['paragraphs']) > 0

def test_parse_table_structure():
    """Test that parser extracts tables with cell content."""
    parser = DocumentParser()
    result = parser.parse_document("tests/fixtures/with_tables.docx")

    assert 'tables' in result
    assert len(result['tables']) > 0

    first_table = result['tables'][0]
    assert 'rows' in first_table
    assert 'cols' in first_table
    assert 'cells' in first_table
