import pytest
from core.alignment import AlignmentEngine

def test_simple_alignment():
    """Test that alignment engine matches identical paragraphs."""
    engine = AlignmentEngine()

    doc1 = {
        'paragraphs': [
            {'text': 'Section 1: Introduction', 'level': 1},
            {'text': 'This is paragraph one.', 'level': 0},
            {'text': 'This is paragraph two.', 'level': 0}
        ]
    }

    doc2 = {
        'paragraphs': [
            {'text': 'Section 1: Introduction', 'level': 1},
            {'text': 'This is paragraph one.', 'level': 0},
            {'text': 'This is paragraph two.', 'level': 0}
        ]
    }

    alignment = engine.align_documents(doc1, doc2)

    assert len(alignment['aligned_pairs']) == 3
    assert alignment['aligned_pairs'][0]['doc1_idx'] == 0
    assert alignment['aligned_pairs'][0]['doc2_idx'] == 0
