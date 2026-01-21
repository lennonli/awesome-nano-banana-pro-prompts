import pytest
from core.llm_analyzer import LLMAnalyzer

def test_substantive_difference_detection():
    """Test LLM analyzer detects substantive differences."""
    analyzer = LLMAnalyzer()

    text1 = "The company guarantees full refund within 30 days."
    text2 = "The company guarantees partial refund within 30 days."

    result = analyzer.analyze_difference(text1, text2)

    assert result['is_substantive'] == True
    assert result['risk_level'] in ['high', 'medium', 'low']
