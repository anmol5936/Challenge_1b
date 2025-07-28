# Multi-Collection PDF Analysis System

A sophisticated document analysis system that processes PDF collections and extracts persona-relevant content with intelligent section ranking and subsection analysis.

## Features

- **Multi-Document Processing**: Handles collections of 3-10 PDF documents simultaneously
- **Persona-Based Analysis**: Tailors content extraction to specific user roles and expertise areas
- **Job-Aligned Ranking**: Prioritizes content based on job-to-be-done requirements
- **Intelligent Segmentation**: Uses both header-based and topic-based content segmentation
- **Subsection Refinement**: Extracts and enhances detailed content for maximum relevance
- **Performance Optimized**: Operates within 60-second processing constraint with 1GB model limit

## Quick Start

### Using Python

1. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. Run the analysis:
```bash
python run_analysis.py [input_json_file] [documents_path]
```

### Using Docker

1. Build the container:
```bash
docker build -t pdf-analyzer .
```

2. Run analysis:
```bash
docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output pdf-analyzer python src/main.py /app/data/input.json /app/data/
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