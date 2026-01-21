# Document Comparison Skill Design

## Overview
A skill for comparing securities firm documents with legal counsel documents, identifying substantive differences, and providing detailed audit reports. Targeted at disclosure documents like IPO prospectuses.

## Use Cases
- Primary: Comparing disclosure documents (IPO prospectuses, due diligence reports, announcements)
- Document Types: Word documents (.docx) with complex structures (tables, multi-level numbering, appendices)
- Source Materials: Securities firm versions vs. legal counsel versions

## Comparison Modes
Three supported modes:

1. **Strict Consistency Check**
   - Character-by-character comparison including punctuation, spacing, formatting
   - Flag all differences without semantic analysis
   - Use case: Absolute consistency required (legal clauses, commitment letters)

2. **Substantive Difference Identification** (Recommended)
   - LLM-powered semantic analysis to determine if differences are substantive
   - Focus on: numeric differences, rights/obligations changes, risk warning additions/removals, warranty clause modifications
   - Rule-based filtering for non-substantive differences (synonyms, minor phrasing)

3. **Compliance Verification**
   - Legal counsel version as standard
   - Identify unauthorized modifications, omissions, inappropriate additions in securities firm version
   - Flag potential compliance risks

## Architecture

### Document Parsing Layer
- **Tool**: python-docx library
- **Capabilities**:
  - Parse complete document DOM tree
  - Extract paragraphs, tables, lists with structure and styling
  - Preserve metadata (version, author, revision history)
  - Handle complex document structures (multi-level numbering, tables, appendices)

### Alignment Engine
Multi-strategy alignment to handle structural differences:

1. **Numbering/Title-based alignment**
   - Identify section headers (Chapter 1, 1.1, etc.)
   - Build mapping between document versions

2. **Text similarity-based alignment**
   - Use cosine similarity for paragraph matching
   - Match closest corresponding paragraphs

3. **Structure-based alignment**
   - Consider context of structured elements (tables, lists)
   - Match based on structural relationships

**Output**: Virtual alignment tree pairing elements from both documents

### Comparison Engine
Core comparison pipeline:
1. Element-wise comparison based on alignment tree
2. Text difference calculation using difflib
3. LLM analysis for substantive difference detection
4. Rule-based filtering and enhancement
5. Risk level calculation (High/Medium/Low)

### Report Generation Layer
Detailed difference reports with:

**Structure**:
1. **Overview**
   - Document metadata (filename, size, modification time)
   - Comparison mode and timestamp
   - Difference statistics (total differences, high-risk count)

2. **Difference Details** (by section or risk level)
   Each difference includes:
   - Difference ID and type (numeric, terminology, legal statement, formatting)
   - Location (section number, paragraph/table reference)
   - Securities firm version content vs. legal counsel version content
   - Difference description and impact analysis
   - Risk level (High/Medium/Low)
   - Suggested modification (optional automated suggestions)

3. **Appendix**
   - Alignment algorithm mapping explanation
   - List of unaligned orphan paragraphs
   - Rule library details

**Output Formats**: Markdown (default), JSON, HTML

## Technology Stack
- **Python 3.9+**
- **python-docx**: Document parsing
- **scikit-learn**: Text similarity (TF-IDF, cosine similarity)
- **LangChain**: LLM integration
- **OpenAI API**: Semantic analysis (or other LLM providers)

## Key Implementation Details

### Document Structure Recognition
- Use paragraph styles (Heading 1-9) for section identification
- Recognize numbering formats (1.1, Chapter 1, 1.1.1)
- Identify table boundaries and row/column structures

### Performance Optimization
- Chunk-based processing for long documents
- LLM call result caching
- Parallel processing of independent sections

### Configuration Flexibility
- Custom rule library (YAML configuration)
- Adjustable risk level thresholds
- Extensible comparison mode plugins

### Error Handling
- Document format exception handling
- LLM call failure retry mechanism
- Degradation strategy for partial failures

## Success Criteria
- Accurately identify substantive differences between documents
- Handle complex document structures with proper alignment
- Generate clear, actionable difference reports
- Support multiple comparison modes flexibly
- Maintain performance on large documents (100+ pages)
