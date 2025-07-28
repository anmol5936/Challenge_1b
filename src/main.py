#!/usr/bin/env python3

import json
import sys
import os
import traceback
import time
import psutil
from datetime import datetime
from typing import Dict, Any, List

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from models.data_models import (
        DocumentInfo, PersonaInfo, JobInfo, Section, Subsection,
        AnalysisContext, ProcessingError
    )
    from components.input_validator import InputValidator
    from components.pdf_parser import PDFParser
    from components.content_segmenter import ContentSegmenter
    from components.persona_analyzer import PersonaAnalyzer
    from components.section_ranker import SectionRanker
    from components.subsection_refiner import SubsectionRefiner
    from components.output_generator import OutputGenerator
except ImportError:
    # Fallback for direct execution
    from src.models.data_models import (
        DocumentInfo, PersonaInfo, JobInfo, Section, Subsection,
        AnalysisContext, ProcessingError
    )
    from src.components.input_validator import InputValidator
    from src.components.pdf_parser import PDFParser
    from src.components.content_segmenter import ContentSegmenter
    from src.components.persona_analyzer import PersonaAnalyzer
    from src.components.section_ranker import SectionRanker
    from src.components.subsection_refiner import SubsectionRefiner
    from src.components.output_generator import OutputGenerator

class MultiCollectionPDFAnalyzer:
    def __init__(self):
        self.input_validator = InputValidator()
        self.pdf_parser = PDFParser()
        self.content_segmenter = ContentSegmenter()
        self.persona_analyzer = PersonaAnalyzer()
        self.section_ranker = SectionRanker()
        self.subsection_refiner = SubsectionRefiner()
        self.output_generator = OutputGenerator()
        
        # Performance constraints
        self.max_processing_time = 60  # seconds
        self.max_sections_per_document = 10
        self.max_subsections_total = 15
        self.max_memory_mb = 1024  # 1GB memory limit
        
        # Performance monitoring
        self.start_time = None
        self.performance_stats = {}
    
    def process_collection(self, input_json: Dict[str, Any], documents_path: str = "") -> Dict[str, Any]:
        """Main processing pipeline for PDF collection analysis"""
        self.start_time = time.time()
        self.performance_stats = {}
        
        try:
            # Monitor memory usage
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            self.performance_stats['initial_memory_mb'] = initial_memory
            # Step 1: Validate input
            step_start = time.time()
            validation_result = self.input_validator.validate_input(input_json)
            if not validation_result.is_valid:
                error_msg = f"Input validation failed: {'; '.join(validation_result.errors)}"
                return self.output_generator.create_error_output(error_msg, input_json)
            self.performance_stats['validation_time'] = time.time() - step_start
            
            # Step 2: Extract input components
            challenge_info = self.input_validator.extract_challenge_info(input_json)
            documents = self.input_validator.extract_documents(input_json)
            persona = self.input_validator.extract_persona(input_json)
            job = self.input_validator.extract_job_to_be_done(input_json)
            
            print(f"Processing {len(documents)} documents for persona: {persona.role}")
            
            # Step 3: Process PDF documents
            step_start = time.time()
            processed_documents = []
            for doc in documents:
                # Check timeout
                if self._check_timeout():
                    print("Warning: Approaching timeout, processing remaining documents with priority")
                    break
                    
                try:
                    processed_doc = self.pdf_parser.process_document(doc, documents_path)
                    if processed_doc.content:  # Only include documents with content
                        processed_documents.append(processed_doc)
                    else:
                        print(f"Warning: No content extracted from {doc.filename}")
                except Exception as e:
                    print(f"Error processing {doc.filename}: {e}")
                    continue
                    
                # Check memory usage
                if self._check_memory_limit():
                    print("Warning: Approaching memory limit, optimizing processing")
                    break
            
            self.performance_stats['pdf_processing_time'] = time.time() - step_start
            
            if not processed_documents:
                return self.output_generator.create_error_output(
                    "No documents could be processed successfully", input_json
                )
            
            print(f"Successfully processed {len(processed_documents)} documents")
            
            # Step 4: Extract and segment content
            all_sections = []
            for doc in processed_documents:
                try:
                    # Try header-based segmentation first
                    sections = self.content_segmenter.segment_by_headers(doc)
                    
                    # If no sections found, try topic-based segmentation
                    if not sections:
                        sections = self.content_segmenter.segment_by_topics(doc)
                    
                    # Limit sections per document
                    sections = sections[:self.max_sections_per_document]
                    all_sections.extend(sections)
                    
                    print(f"Extracted {len(sections)} sections from {doc.filename}")
                    
                except Exception as e:
                    print(f"Error segmenting content from {doc.filename}: {e}")
                    continue
            
            if not all_sections:
                return self.output_generator.create_error_output(
                    "No content sections could be extracted", input_json
                )
            
            print(f"Total sections extracted: {len(all_sections)}")
            
            # Step 5: Rank sections by relevance and importance
            try:
                ranked_sections = self.section_ranker.rank_sections(all_sections, persona, job)
                
                # Optimize for scoring criteria
                optimized_sections = self.section_ranker.optimize_for_scoring_criteria(ranked_sections)
                
                # Limit to top sections
                top_sections = optimized_sections[:15]  # Top 15 sections max
                
                print(f"Ranked and selected {len(top_sections)} top sections")
                
            except Exception as e:
                print(f"Error ranking sections: {e}")
                top_sections = all_sections[:10]  # Fallback to first 10 sections
            
            # Step 6: Extract and refine subsections
            all_subsections = []
            try:
                # Process top sections for subsection analysis
                for section in top_sections[:8]:  # Limit to top 8 sections for subsection analysis
                    try:
                        subsections = self.subsection_refiner.extract_subsections(section)
                        all_subsections.extend(subsections)
                        
                        # Stop if we have enough subsections
                        if len(all_subsections) >= self.max_subsections_total:
                            break
                            
                    except Exception as e:
                        print(f"Error refining subsections for section '{section.title}': {e}")
                        continue
                
                # Limit total subsections
                all_subsections = all_subsections[:self.max_subsections_total]
                
                print(f"Generated {len(all_subsections)} refined subsections")
                
            except Exception as e:
                print(f"Error processing subsections: {e}")
                all_subsections = []
            
            # Step 7: Generate output
            try:
                timestamp = self.output_generator.generate_timestamp()
                metadata = self.output_generator.generate_metadata(input_json, timestamp)
                
                formatted_sections = self.output_generator.format_extracted_sections(top_sections)
                formatted_subsections = self.output_generator.format_subsection_analysis(all_subsections)
                
                final_output = self.output_generator.create_final_output(
                    metadata, formatted_sections, formatted_subsections
                )
                
                # Validate output format
                if not self.output_generator.validate_output_format(final_output):
                    return self.output_generator.create_error_output(
                        "Generated output format validation failed", input_json
                    )
                
                print("Successfully generated output")
                return final_output
                
            except Exception as e:
                print(f"Error generating output: {e}")
                return self.output_generator.create_error_output(
                    f"Output generation failed: {str(e)}", input_json
                )
        
        except Exception as e:
            print(f"Unexpected error in processing pipeline: {e}")
            print(traceback.format_exc())
            return self.output_generator.create_error_output(
                f"Processing pipeline failed: {str(e)}", input_json
            )
    
    def _check_timeout(self) -> bool:
        """Check if processing is approaching timeout limit"""
        if self.start_time is None:
            return False
        elapsed = time.time() - self.start_time
        return elapsed > (self.max_processing_time * 0.8)  # 80% of max time
    
    def _check_memory_limit(self) -> bool:
        """Check if memory usage is approaching limit"""
        try:
            process = psutil.Process()
            current_memory = process.memory_info().rss / 1024 / 1024  # MB
            return current_memory > (self.max_memory_mb * 0.8)  # 80% of max memory
        except:
            return False
    
    def _get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary statistics"""
        if self.start_time is None:
            return {}
        
        total_time = time.time() - self.start_time
        try:
            process = psutil.Process()
            peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        except:
            peak_memory = 0
        
        summary = {
            'total_processing_time': total_time,
            'peak_memory_mb': peak_memory,
            'within_time_limit': total_time <= self.max_processing_time,
            'within_memory_limit': peak_memory <= self.max_memory_mb
        }
        summary.update(self.performance_stats)
        return summary

def main():
    """Main entry point for the PDF analysis system"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_json_file> [documents_path]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    documents_path = sys.argv[2] if len(sys.argv) > 2 else ""
    
    try:
        # Load input JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        
        # Create analyzer and process
        analyzer = MultiCollectionPDFAnalyzer()
        result = analyzer.process_collection(input_data, documents_path)
        
        # Output result as JSON
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except FileNotFoundError:
        error_output = {
            "metadata": {
                "input_documents": [],
                "persona": {},
                "job_to_be_done": {},
                "processing_timestamp": datetime.now().isoformat(),
                "error": f"Input file not found: {input_file}"
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(1)
        
    except json.JSONDecodeError as e:
        error_output = {
            "metadata": {
                "input_documents": [],
                "persona": {},
                "job_to_be_done": {},
                "processing_timestamp": datetime.now().isoformat(),
                "error": f"Invalid JSON in input file: {str(e)}"
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(1)
        
    except Exception as e:
        error_output = {
            "metadata": {
                "input_documents": [],
                "persona": {},
                "job_to_be_done": {},
                "processing_timestamp": datetime.now().isoformat(),
                "error": f"Unexpected error: {str(e)}"
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()