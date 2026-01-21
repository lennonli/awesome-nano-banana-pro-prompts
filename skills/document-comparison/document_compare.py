from typing import Dict, Any
from pathlib import Path

from core.parser import DocumentParser
from core.alignment import AlignmentEngine
from core.comparator import DocumentComparator
from core.reporter import ReportGenerator

class DocumentComparison:
    """Main orchestration class for document comparison."""

    def __init__(self, mode: str = 'substantive'):
        """Initialize document comparison with specified mode."""
        self.mode = mode
        self.parser = DocumentParser()
        self.alignment = AlignmentEngine()
        self.comparator = DocumentComparator(mode=mode)
        self.reporter = ReportGenerator()

    def compare(self,
                doc1_path: str,
                doc2_path: str,
                output_format: str = 'markdown') -> Dict[str, Any]:
        """
        Compare two documents and generate report.

        Args:
            doc1_path: Path to securities firm document
            doc2_path: Path to legal counsel document
            output_format: Report format (markdown/json/html)

        Returns:
            Dictionary containing report, differences, and metadata
        """
        doc1 = self.parser.parse_document(doc1_path)
        doc2 = self.parser.parse_document(doc2_path)

        alignment = self.alignment.align_documents(doc1, doc2)

        all_differences = []
        for pair in alignment['aligned_pairs']:
            differences = self.comparator.compare_texts(
                pair['text1'],
                pair['text2']
            )

            for diff in differences:
                diff['location'] = {
                    'doc1_index': pair['doc1_idx'],
                    'doc2_index': pair['doc2_idx']
                }

            all_differences.extend(differences)

        metadata = {
            'doc1_file': Path(doc1_path).name,
            'doc2_file': Path(doc2_path).name,
            'doc1_paragraphs': doc1['metadata']['paragraph_count'],
            'doc2_paragraphs': doc2['metadata']['paragraph_count'],
            'mode': self.mode,
            'aligned_pairs': len(alignment['aligned_pairs'])
        }

        report = self.reporter.generate_report(
            all_differences,
            metadata,
            format=output_format
        )

        return {
            'report': report,
            'differences': all_differences,
            'metadata': metadata,
            'alignment': alignment
        }

    def compare_and_save(self,
                        doc1_path: str,
                        doc2_path: str,
                        output_path: str,
                        output_format: str = 'markdown') -> str:
        """
        Compare documents and save report to file.

        Args:
            doc1_path: Path to securities firm document
            doc2_path: Path to legal counsel document
            output_path: Path for output report
            output_format: Report format (markdown/json/html)

        Returns:
            Path to saved report
        """
        result = self.compare(doc1_path, doc2_path, output_format)

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result['report'])

        return str(output_file)
