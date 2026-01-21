from typing import Dict, List
import re

from core.llm_analyzer import LLMAnalyzer

class DocumentComparator:
    """Compare document contents in different modes."""

    def __init__(self, mode: str = 'substantive'):
        """Initialize comparator with comparison mode."""
        self.mode = mode
        self.supported_modes = ['strict', 'substantive', 'compliance']
        self.llm_analyzer = LLMAnalyzer()

        if mode not in self.supported_modes:
            raise ValueError(f"Unsupported mode: {mode}")

    def compare_texts(self, text1: str, text2: str) -> List[Dict]:
        """Compare two text strings and return differences."""
        if self.mode == 'strict':
            return self._strict_compare(text1, text2)
        elif self.mode == 'substantive':
            return self._substantive_compare(text1, text2)
        elif self.mode == 'compliance':
            return self._compliance_compare(text1, text2)

    def _strict_compare(self, text1: str, text2: str) -> List[Dict]:
        """Strict character-by-character comparison."""
        differences = []

        if text1 == text2:
            return differences

        numbers1 = re.findall(r'\d+', text1)
        numbers2 = re.findall(r'\d+', text2)

        if numbers1 != numbers2:
            differences.append({
                'type': 'numeric',
                'text1': ', '.join(numbers1),
                'text2': ', '.join(numbers2),
                'description': 'Numeric values differ',
                'risk_level': 'medium'
            })

        if text1 != text2 and not differences:
            differences.append({
                'type': 'content',
                'text1': text1,
                'text2': text2,
                'description': 'Text content differs',
                'risk_level': 'low'
            })

        return differences

    def _substantive_compare(self, text1: str, text2: str) -> List[Dict]:
        """Compare using LLM to detect substantive differences."""
        differences = []

        if text1 == text2:
            return differences

        analysis = self.llm_analyzer.analyze_difference(text1, text2)

        if analysis['is_substantive']:
            differences.append({
                'type': 'substantive',
                'text1': text1,
                'text2': text2,
                'description': analysis['explanation'],
                'risk_level': analysis['risk_level']
            })

        return differences
