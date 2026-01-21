from pathlib import Path
from typing import Dict, Any
from docx import Document

class DocumentParser:
    """Parse Word documents into structured data."""

    def parse_document(self, filepath: str) -> Dict[str, Any]:
        """Parse a Word document and return structured data."""
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Document not found: {filepath}")

        doc = Document(filepath)

        result = {
            'paragraphs': [],
            'tables': [],
            'metadata': {
                'paragraph_count': len(doc.paragraphs),
                'table_count': len(doc.tables)
            }
        }

        for para in doc.paragraphs:
            if para.text.strip():
                result['paragraphs'].append({
                    'text': para.text,
                    'style': para.style.name,
                    'level': self._get_heading_level(para.style.name)
                })

        return result

    def _get_heading_level(self, style_name: str) -> int:
        """Extract heading level from style name."""
        if 'Heading 1' in style_name:
            return 1
        elif 'Heading 2' in style_name:
            return 2
        elif 'Heading 3' in style_name:
            return 3
        return 0
