from typing import Dict
import re

class LLMAnalyzer:
    """Use LLM to analyze if differences are substantive."""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """Initialize LLM analyzer."""
        try:
            from openai import OpenAI
            self.client = OpenAI()
            self.model = model_name
            self._use_llm = True
        except (ImportError, Exception):
            self._use_llm = False

    def analyze_difference(self, text1: str, text2: str) -> Dict:
        """Analyze if the difference between two texts is substantive."""
        if not self._use_llm or text1 == text2:
            return self._rule_based_analysis(text1, text2)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """You are analyzing differences between legal documents for disclosure purposes.
Determine if the difference is SUBSTANTIVE (affects rights, obligations, risks, or guarantees) or NON-SUBSTANTIVE.
Respond with JSON: {"is_substantive": true/false, "explanation": "text", "risk_level": "high/medium/low"}"""
                }, {
                    "role": "user",
                    "content": f"Original: {text1}\nModified: {text2}"
                }],
                temperature=0
            )
            result = response.choices[0].message.content

            if '"is_substantive": true' in result.lower():
                return {
                    'is_substantive': True,
                    'explanation': 'LLM analysis indicates substantive difference',
                    'risk_level': self._extract_risk_level(result)
                }
            else:
                return {
                    'is_substantive': False,
                    'explanation': 'LLM analysis indicates non-substantive difference',
                    'risk_level': 'low'
                }
        except Exception as e:
            return {
                'is_substantive': True,
                'explanation': f'LLM analysis failed: {str(e)}',
                'risk_level': 'medium'
            }

    def _rule_based_analysis(self, text1: str, text2: str) -> Dict:
        """Fallback rule-based analysis."""
        numeric_diff = re.findall(r'\d+', text1) != re.findall(r'\d+', text2)
        legal_terms = ['liability', 'warranty', 'guarantee', 'obligation', 'right', 'risk']
        has_legal_term = any(term in text1.lower() or term in text2.lower() for term in legal_terms)

        if numeric_diff or has_legal_term:
            return {
                'is_substantive': True,
                'explanation': 'Rule-based analysis: numeric or legal term change detected',
                'risk_level': 'medium' if numeric_diff else 'high'
            }
        return {
            'is_substantive': False,
            'explanation': 'Rule-based analysis: no substantive differences detected',
            'risk_level': 'low'
        }

    def _extract_risk_level(self, response: str) -> str:
        """Extract risk level from LLM response."""
        if '"risk_level": "high"' in response:
            return 'high'
        elif '"risk_level": "medium"' in response:
            return 'medium'
        return 'low'
