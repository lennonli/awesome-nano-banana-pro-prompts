from typing import Dict, List, Any
from difflib import SequenceMatcher

class AlignmentEngine:
    """Align paragraphs and tables between two document versions."""

    def align_documents(self, doc1: Dict, doc2: Dict) -> Dict[str, Any]:
        """Align documents and return mapping."""
        paragraphs1 = doc1.get('paragraphs', [])
        paragraphs2 = doc2.get('paragraphs', [])
        tables1 = doc1.get('tables', [])
        tables2 = doc2.get('tables', [])

        aligned_pairs = []

        for i, para1 in enumerate(paragraphs1):
            best_match = self._find_best_match(para1, paragraphs2)

            if best_match is not None:
                aligned_pairs.append({
                    'doc1_idx': i,
                    'doc2_idx': best_match['idx'],
                    'similarity': best_match['similarity'],
                    'text1': para1['text'],
                    'text2': paragraphs2[best_match['idx']]['text'],
                    'type': 'paragraph'
                })

        table_alignments = self._align_tables(tables1, tables2)
        for idx, table_align in enumerate(table_alignments):
            aligned_pairs.append({
                'doc1_idx': len(paragraphs1) + idx,
                'doc2_idx': len(paragraphs2) + idx,
                'similarity': table_align['similarity'],
                'text1': table_align['text1'],
                'text2': table_align['text2'],
                'type': 'table',
                'table_idx1': table_align.get('table_idx1'),
                'table_idx2': table_align.get('table_idx2')
            })

        return {
            'aligned_pairs': aligned_pairs,
            'orphan_doc1': [],
            'orphan_doc2': [],
            'table_alignments': table_alignments
        }

    def _find_best_match(self, para: Dict, paragraphs: List[Dict]) -> Dict:
        """Find best matching paragraph by text similarity."""
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

    def _align_tables(self, tables1: List[Dict], tables2: List[Dict]) -> List[Dict]:
        """Align tables by comparing their content."""
        alignments = []

        if not tables1 or not tables2:
            return alignments

        table_summaries1 = [self._create_table_summary(t) for t in tables1]
        table_summaries2 = [self._create_table_summary(t) for t in tables2]

        for i, summary1 in enumerate(table_summaries1):
            best_match = None
            best_similarity = 0.5

            for j, summary2 in enumerate(table_summaries2):
                similarity = self._compare_table_summaries(summary1, summary2)

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = {
                        'idx1': i,
                        'idx2': j,
                        'similarity': similarity,
                        'text1': summary1['text'][:200],
                        'text2': summary2['text'][:200],
                        'table_idx1': i,
                        'table_idx2': j,
                        'rows1': summary1['rows'],
                        'rows2': summary2['rows']
                    }

            if best_match is not None and best_similarity > 0.4:
                alignments.append(best_match)

        return alignments

    def _create_table_summary(self, table: Dict) -> Dict:
        """Create a summary of table for comparison."""
        summary = {
            'rows': table.get('rows', 0),
            'cols': table.get('cols', 0),
            'text': self._get_table_text(table),
            'data_cells': []
        }

        if 'cells' in table and table['cells']:
            for row in table['cells']:
                for cell in row:
                    if str(cell).strip() and len(str(cell).strip()) > 2:
                        summary['data_cells'].append(str(cell).strip())

        return summary

    def _compare_table_summaries(self, summary1: Dict, summary2: Dict) -> float:
        """Compare two table summaries."""
        text_similarity = self._calculate_similarity(summary1['text'], summary2['text'])

        if len(summary1['data_cells']) == 0 or len(summary2['data_cells']) == 0:
            return text_similarity

        cells1_set = set(summary1['data_cells'])
        cells2_set = set(summary2['data_cells'])

        intersection = len(cells1_set.intersection(cells2_set))
        union = len(cells1_set.union(cells2_set))

        if union == 0:
            return text_similarity

        jaccard_similarity = intersection / union

        return (text_similarity * 0.3) + (jaccard_similarity * 0.7)

    def _get_table_text(self, table: Dict) -> str:
        """Extract text from table for comparison."""
        text_parts = []

        if 'cells' in table and table['cells']:
            for row in table['cells']:
                text_parts.extend([str(cell) for cell in row if str(cell).strip()])

        return ' '.join(text_parts)[:500]
