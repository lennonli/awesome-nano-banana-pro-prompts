from typing import Dict, List, Any, Optional
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

    def _find_best_match(self, para: Dict, paragraphs: List[Dict]) -> Optional[Dict]:
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
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, text1, text2).ratio()

    def _align_tables(self, tables1: List[Dict], tables2: List[Dict]) -> List[Dict]:
        """Align tables with advanced matching strategy."""
        alignments = []

        if not tables1 or not tables2:
            return alignments

        for i, table1 in enumerate(tables1):
            best_match = None
            best_score = 0.0

            summary1 = self._create_enhanced_table_summary(table1)

            for j, table2 in enumerate(tables2):
                summary2 = self._create_enhanced_table_summary(table2)
                score = self._calculate_table_score(summary1, summary2)

                if score > best_score:
                    best_score = score
                    best_match = {
                        'idx1': i,
                        'idx2': j,
                        'similarity': score,
                        'text1': summary1['text'][:150],
                        'text2': summary2['text'][:150],
                        'table_idx1': i,
                        'table_idx2': j,
                        'rows1': summary1['rows'],
                        'rows2': summary2['rows'],
                        'table_type1': summary1.get('type'),
                        'table_type2': summary2.get('type'),
                        'matched_entities': summary1.get('matched_entities', 0)
                    }

            if best_match is not None and best_score > 0.25:
                alignments.append(best_match)

        return alignments

    def _create_enhanced_table_summary(self, table: Dict) -> Dict:
        """Create enhanced table summary with entity extraction."""
        summary = {
            'rows': table.get('rows', 0),
            'cols': table.get('cols', 0),
            'text': self._get_table_text(table),
            'data_cells': []
        }

        if 'cells' in table and table['cells']:
            for row in table['cells']:
                for cell in row:
                    cell_str = str(cell).strip()
                    if cell_str and len(cell_str) > 2:
                        summary['data_cells'].append(cell_str)

        return summary

    def _classify_table_type(self, table: Dict) -> str:
        """Classify table by structure and content."""
        if 'cells' not in table or not table['cells']:
            return 'unknown'

        cells = table['cells']
        if len(cells) == 0:
            return 'empty'

        first_row = cells[0] if len(cells[0]) > 0 else []
        has_multi_col = len(first_row) > 1

        text = ' '.join([str(cell) for row in cells for cell in row]).lower()

        if has_multi_col:
            if '关联方' in text or '股东' in text or '持股' in text:
                return 'related_parties'
            elif '专利' in text or '商标' in text or '知识产权' in text:
                return 'ip'
            else:
                return 'multi_column'
        else:
        if len(cells) > 5 and '关联方' in text:
                return 'related_parties'
            elif '关联方' in text or '股东' in text or '持股' in text:
                return 'related_parties'
            elif '专利' in text or '商标' in text or '知识产权' in text:
                return 'ip'
            elif '承租' in text or '租赁' in text:
                return 'lease'
            elif '房产' in text or '房屋' in text or '土地使用权' in text:
                return 'real_estate'
            elif '域名' in text or '网址' in text or '备案' in text:
                return 'domain'
            else:
                return 'related_parties'

    def _calculate_table_score(self, summary1: Dict, summary2: Dict) -> float:
        """Calculate comprehensive table similarity score."""
        type1 = summary1.get('type', 'unknown')
        type2 = summary2.get('type', 'unknown')

        if type1 != type2:
            return 0.0

        text_similarity = self._calculate_similarity(summary1['text'], summary2['text'])
        
        cells1_set = set(summary1['data_cells'])
        cells2_set = set(summary2['data_cells'])

        if len(cells1_set) == 0 and len(cells2_set) == 0:
            return text_similarity * 0.5

        intersection = len(cells1_set.intersection(cells2_set))
        union = len(cells1_set.union(cells2_set))

        if union == 0:
            return text_similarity * 0.5

        jaccard_similarity = intersection / union

        row_diff = abs(summary1['rows'] - summary2['rows']) / max(summary1['rows'], summary2['rows']) if max(summary1['rows'], summary2['rows']) > 0 else 1

        score = (text_similarity * 0.3) + (jaccard_similarity * 0.5) + ((1 - row_diff) * 0.2)

        return score

    def _get_table_text(self, table: Dict) -> str:
        """Extract text from table for comparison."""
        text_parts = []

        if 'cells' in table and table['cells']:
            for row in table['cells']:
                text_parts.extend([str(cell) for cell in row if str(cell).strip()])

        return ' '.join(text_parts)[:500]
