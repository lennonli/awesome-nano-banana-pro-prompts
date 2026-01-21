import pytest
from core.comparator import DocumentComparator

def test_strict_comparison():
    """Test strict mode comparison identifies all differences."""
    comparator = DocumentComparator(mode='strict')

    text1 = "The company has 100 employees."
    text2 = "The company has 101 employees."

    differences = comparator.compare_texts(text1, text2)

    assert len(differences) == 1
    assert differences[0]['type'] == 'numeric'
    assert differences[0]['text1'] == '100'
    assert differences[0]['text2'] == '101'
    assert differences[0]['risk_level'] == 'medium'

def test_compliance_verification():
    """Test compliance mode identifies unauthorized changes."""
    comparator = DocumentComparator(mode='compliance')

    text1 = "The company assumes full liability for all claims."
    text2 = "The company assumes responsibility for some claims."

    differences = comparator.compare_texts(text1, text2)

    assert len(differences) >= 1
    assert any(d['type'] == 'compliance_risk' for d in differences)
