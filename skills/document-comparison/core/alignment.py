from typing import Dict, List, Any
from difflib import SequenceMatcher

class AlignmentEngine:
    """Align paragraphs between two document versions."""

    def align_documents(self, doc1: Dict, doc2: Dict) -> Dict[str, Any]:
        """Align documents and return mapping."""
        paragraphs1 = doc1['paragraphs']
        paragraphs2 = doc2['paragraphs']

        aligned_pairs = []

        for i, para1 in enumerate(paragraphs1):
            best_match = self._find_best_match(para1, paragraphs2)

            if best_match is not None:
                aligned_pairs.append({
                    'doc1_idx': i,
                    'doc2_idx': best_match['idx'],
                    'similarity': best_match['similarity'],
                    'text1': para1['text'],
                    'text2': paragraphs2[best_match['idx']]['text']
                })

        return {
            'aligned_pairs': aligned_pairs,
            'orphan_doc1': [],
            'orphan_doc2': []
        }

    def _find_best_match(self, para: Dict, paragraphs: List[Dict]) -> Dict:
        """Find the best matching paragraph by text similarity."""
        best_match = None
        best_similarity = 0.8

        for i, p in enumerate(paragraphs):
            similarity = self._calculate_similarity(para['text'], p['text'])

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = {'idx': i, 'similarity': similarity}

        return best_match

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using SequenceMatcher."""
        return SequenceMatcher(None, text1, text2).ratio()
