# Multi-Collection PDF Analysis System

A sophisticated command-line PDF analysis system designed for Challenge 1b that extracts and prioritizes the most relevant sections from PDF collections based on specific personas and their job-to-be-done tasks. The system operates under strict performance constraints (≤60 seconds processing time, ≤1GB memory usage, CPU-only) while delivering high-quality, ranked content analysis.

## 🎯 Challenge 1b Results

**Structure Compliance: 100% (33/33 points)**
- ✅ Collection 1 (Travel): 12 sections, 14 subsections (0.39s, 629MB)
- ✅ Collection 2 (HR/Acrobat): 15 sections, 15 subsections (3.85s, 749MB)  
- ✅ Collection 3 (Culinary): 9 sections, 8 subsections (1.41s, 750MB)

All outputs match the expected JSON structure exactly.

## Features

- **Multi-Document Processing**: Handles collections of 3-10 PDF documents simultaneously
- **Persona-Based Analysis**: Tailors content extraction to specific user roles and expertise areas
- **Job-Aligned Ranking**: Prioritizes content based on job-to-be-done requirements
- **Intelligent Segmentation**: Uses both header-based and topic-based content segmentation
- **Subsection Refinement**: Extracts and enhances detailed content for maximum relevance
- **Performance Optimized**: Operates within 60-second processing constraint with 1GB model limit

## Quick Start

### Installation and Usage

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run Challenge 1b collections:
```bash
# Run specific collection
python run_challenge.py 1  # Collection 1 (Travel Planning)
python run_challenge.py 2  # Collection 2 (HR/Acrobat Forms)  
python run_challenge.py 3  # Collection 3 (Menu Planning)

# Run all collections
python run_challenge.py
```

3. Analyze compliance with expected outputs:
```bash
python analyze_compliance.py
```

4. Test individual components:
```bash
python test_sample.py
```

### Using Docker

1. **Quick Setup** (automated):
```bash
python docker_setup.py
```

2. **Manual Setup**:
```bash
# Build image
docker build -t pdf-analysis-system .

# Run all collections
docker run --rm pdf-analysis-system

# Run specific collection
docker run --rm pdf-analysis-system python run_challenge.py 1

# Run with output volume
docker run --rm -v $(pwd)/output:/app/output pdf-analysis-system
```

3. **Using Docker Compose**:
```bash
# Run all collections
docker-compose up

# Run specific collection
docker-compose --profile collection up pdf-analysis-collection1

# Run compliance check
docker-compose --profile test up pdf-analysis-compliance
```

## Input Format

The system expects JSON input with the following structure:

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_002",
    "test_case_name": "travel_planning",
    "description": "Travel planning for college friends"
  },
  "documents": [
    {
      "filename": "document1.pdf",
      "title": "Travel Guide"
    }
  ],
  "persona": {
    "role": "Travel planning specialist helping a group of 10 college friends plan their 4-day trip"
  },
  "job_to_be_done": {
    "task": "Plan a comprehensive 4-day itinerary including accommodations, activities, and dining"
  }
}
```

## Output Format

The system generates structured JSON output:

```json
{
  "metadata": {
    "input_documents": [...],
    "persona": {...},
    "job_to_be_done": {...},
    "processing_timestamp": "2025-01-01T12:00:00.000000"
  },
  "extracted_sections": [
    {
      "document": "document1.pdf",
      "section_title": "Beach Activities",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "document1.pdf", 
      "refined_text": "Detailed analysis of beach activities...",
      "page_number": 3
    }
  ]
}
```

## Architecture

The system consists of modular components:

- **Input Validator**: Validates JSON input and extracts structured data
- **PDF Parser**: Extracts text content with page number preservation
- **Content Segmenter**: Divides content into logical sections
- **Persona Analyzer**: Analyzes relevance based on persona and job requirements
- **Section Ranker**: Ranks sections by importance and relevance
- **Subsection Refiner**: Extracts and enhances detailed content
- **Output Generator**: Creates structured JSON output

## Performance Characteristics

- **Processing Time**: ≤60 seconds for typical document collections
- **Memory Usage**: ≤1GB total model size
- **CPU Only**: No GPU requirements
- **Offline Capable**: Works without internet access

## Supported Domains

The system is optimized for multiple domains:

- **Travel Planning**: Destinations, accommodations, activities, restaurants
- **HR/Document Management**: Forms, workflows, policies, procedures  
- **Culinary/Catering**: Recipes, menus, dietary requirements, kitchen management

## Error Handling

The system provides graceful error handling:

- PDF parsing errors: Continues processing remaining documents
- Validation errors: Returns descriptive error messages
- Timeout handling: Returns partial results when approaching time limits
- Memory constraints: Implements efficient processing strategies

## Development

### Project Structure

```
├── src/
│   ├── components/          # Core processing components
│   ├── models/             # Data models and structures
│   └── main.py            # Main application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── run_analysis.py        # Test runner and demo script
└── README.md             # This file
```

### Testing

Run the included test script:

```bash
python run_analysis.py
```

This will create sample input and demonstrate the system capabilities.

## License

This project is designed for hackathon/competition use and follows performance optimization requirements for Challenge 1b.