import json
from datetime import datetime
from typing import Dict, List, Any
from src.models.data_models import Section, Subsection

class OutputGenerator:
    def __init__(self):
        self.timestamp_format = "%Y-%m-%dT%H:%M:%S.%f"
    
    def generate_metadata(self, input_data: Dict[str, Any], timestamp: str) -> Dict[str, Any]:
        """Generate metadata section for output"""
        metadata = {
            "input_documents": [
                {"filename": doc["filename"], "title": doc["title"]} 
                for doc in input_data.get("documents", [])
            ],
            "persona": input_data.get("persona", {}),
            "job_to_be_done": input_data.get("job_to_be_done", {}),
            "processing_timestamp": timestamp
        }
        return metadata
    
    def format_extracted_sections(self, ranked_sections: List[Section]) -> List[Dict[str, Any]]:
        """Format extracted sections for output"""
        formatted_sections = []
        
        for section in ranked_sections:
            formatted_section = {
                "document": section.document,
                "section_title": section.title,
                "importance_rank": section.importance_rank,
                "page_number": section.page_number
            }
            formatted_sections.append(formatted_section)
        
        return formatted_sections
    
    def format_subsection_analysis(self, refined_subsections: List[Subsection]) -> List[Dict[str, Any]]:
        """Format subsection analysis for output"""
        formatted_subsections = []
        
        for subsection in refined_subsections:
            formatted_subsection = {
                "document": subsection.document,
                "refined_text": subsection.refined_text,
                "page_number": subsection.page_number
            }
            formatted_subsections.append(formatted_subsection)
        
        return formatted_subsections
    
    def create_final_output(self, metadata: Dict[str, Any], sections: List[Dict[str, Any]], 
                          subsections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create final JSON output"""
        output = {
            "metadata": metadata,
            "extracted_sections": sections,
            "subsection_analysis": subsections
        }
        return output
    
    def generate_timestamp(self) -> str:
        """Generate ISO format timestamp"""
        now = datetime.now()
        return now.strftime(self.timestamp_format)
    
    def validate_output_format(self, output: Dict[str, Any]) -> bool:
        """Validate output format against requirements"""
        required_keys = ["metadata", "extracted_sections", "subsection_analysis"]
        
        # Check top-level keys
        for key in required_keys:
            if key not in output:
                return False
        
        # Check metadata structure
        metadata = output["metadata"]
        metadata_required = ["input_documents", "persona", "job_to_be_done", "processing_timestamp"]
        for key in metadata_required:
            if key not in metadata:
                return False
        
        # Check extracted_sections structure
        sections = output["extracted_sections"]
        if not isinstance(sections, list):
            return False
        
        for section in sections:
            section_required = ["document", "section_title", "importance_rank", "page_number"]
            for key in section_required:
                if key not in section:
                    return False
        
        # Check subsection_analysis structure
        subsections = output["subsection_analysis"]
        if not isinstance(subsections, list):
            return False
        
        for subsection in subsections:
            subsection_required = ["document", "refined_text", "page_number"]
            for key in subsection_required:
                if key not in subsection:
                    return False
        
        return True
    
    def save_output_to_file(self, output: Dict[str, Any], filename: str) -> bool:
        """Save output to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving output to {filename}: {e}")
            return False
    
    def create_error_output(self, error_message: str, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create error output format"""
        timestamp = self.generate_timestamp()
        
        error_output = {
            "metadata": {
                "input_documents": input_data.get("documents", []) if input_data else [],
                "persona": input_data.get("persona", {}) if input_data else {},
                "job_to_be_done": input_data.get("job_to_be_done", {}) if input_data else {},
                "processing_timestamp": timestamp,
                "error": error_message
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }
        
        return error_output