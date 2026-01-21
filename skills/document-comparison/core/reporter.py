from typing import List, Dict
from datetime import datetime

class ReportGenerator:
    """Generate comparison reports in various formats."""

    def generate_report(self, differences: List[Dict],
                       metadata: Dict,
                       format: str = 'markdown') -> str:
        """Generate report in specified format."""
        if format == 'markdown':
            return self._generate_markdown(differences, metadata)
        elif format == 'json':
            return self._generate_json(differences, metadata)
        elif format == 'html':
            return self._generate_html(differences, metadata)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _generate_markdown(self, differences: List[Dict], metadata: Dict) -> str:
        """Generate markdown report."""
        report = []

        report.append("# Document Comparison Report\n")

        report.append("## Overview\n")
        report.append(f"- **Securities Firm Document:** {metadata.get('doc1_file', 'N/A')}")
        report.append(f"- **Legal Counsel Document:** {metadata.get('doc2_file', 'N/A')}")
        report.append(f"- **Comparison Mode:** {metadata.get('mode', 'N/A')}")
        report.append(f"- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"- **Total Differences:** {len(differences)}")

        high_risk = [d for d in differences if d.get('risk_level') == 'high']
        medium_risk = [d for d in differences if d.get('risk_level') == 'medium']
        low_risk = [d for d in differences if d.get('risk_level') == 'low']

        report.append(f"- **High Risk:** {len(high_risk)}")
        report.append(f"- **Medium Risk:** {len(medium_risk)}")
        report.append(f"- **Low Risk:** {len(low_risk)}")
        report.append("")

        report.append("## Differences\n")

        for i, diff in enumerate(differences, 1):
            risk_emoji = self._get_risk_emoji(diff.get('risk_level', 'low'))

            report.append(f"### {risk_emoji} Difference {i}: {diff.get('type', 'Unknown')}")
            report.append(f"- **Risk Level:** {diff.get('risk_level', 'unknown').upper()}")
            report.append(f"- **Description:** {diff.get('description', 'N/A')}")

            if 'text1' in diff:
                report.append(f"- **Securities Firm:** {diff['text1']}")
            if 'text2' in diff:
                report.append(f"- **Legal Counsel:** {diff['text2']}")

            report.append("")

        return "\n".join(report)

    def _generate_json(self, differences: List[Dict], metadata: Dict) -> str:
        """Generate JSON report."""
        import json

        report = {
            'metadata': metadata,
            'generated': datetime.now().isoformat(),
            'statistics': {
                'total_differences': len(differences),
                'high_risk': len([d for d in differences if d.get('risk_level') == 'high']),
                'medium_risk': len([d for d in differences if d.get('risk_level') == 'medium']),
                'low_risk': len([d for d in differences if d.get('risk_level') == 'low'])
            },
            'differences': differences
        }

        return json.dumps(report, indent=2)

    def _generate_html(self, differences: List[Dict], metadata: Dict) -> str:
        """Generate HTML report."""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Document Comparison Report</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        .high-risk { background-color: #ffebee; border-left: 4px solid #f44336; }
        .medium-risk { background-color: #fff3e0; border-left: 4px solid #ff9800; }
        .low-risk { background-color: #e8f5e9; border-left: 4px solid #4caf50; }
        .difference { padding: 15px; margin: 10px 0; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Document Comparison Report</h1>

    <h2>Overview</h2>
    <ul>
        <li><strong>Securities Firm Document:</strong> {doc1}</li>
        <li><strong>Legal Counsel Document:</strong> {doc2}</li>
        <li><strong>Comparison Mode:</strong> {mode}</li>
        <li><strong>Total Differences:</strong> {total}</li>
    </ul>

    <h2>Differences</h2>
    {differences}
</body>
</html>
""".format(
            doc1=metadata.get('doc1_file', 'N/A'),
            doc2=metadata.get('doc2_file', 'N/A'),
            mode=metadata.get('mode', 'N/A'),
            total=len(differences),
            differences=self._format_html_differences(differences)
        )

        return html

    def _format_html_differences(self, differences: List[Dict]) -> str:
        """Format differences as HTML."""
        html_parts = []

        for diff in differences:
            risk_class = f"{diff.get('risk_level', 'low')}-risk"
            html_parts.append(f"""
<div class="difference {risk_class}">
    <h3>{diff.get('type', 'Unknown')}</h3>
    <p><strong>Risk Level:</strong> {diff.get('risk_level', 'unknown').upper()}</p>
    <p><strong>Description:</strong> {diff.get('description', 'N/A')}</p>
    <p><strong>Securities Firm:</strong> {diff.get('text1', 'N/A')}</p>
    <p><strong>Legal Counsel:</strong> {diff.get('text2', 'N/A')}</p>
</div>
""")

        return "\n".join(html_parts)

    def _get_risk_emoji(self, risk_level: str) -> str:
        """Get emoji for risk level."""
        emojis = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }
        return emojis.get(risk_level.lower(), '⚪')
