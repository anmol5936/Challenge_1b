import fitz  # PyMuPDF
import os
from typing import List, Optional
from src.models.data_models import PageContent, DocumentInfo, ProcessingError

class PDFParser:
    def __init__(self):
        self.max_pages_per_doc = 50  # Limit for performance
    
    def extract_text_with_pages(self, pdf_path: str) -> List[PageContent]:
        """Extract text content from PDF with page number tracking"""
        pages = []
        
        try:
            if not os.path.exists(pdf_path):
                raise ProcessingError(f"PDF file not found: {pdf_path}", "FileNotFound")
            
            doc = fitz.open(pdf_path)
            
            for page_num in range(min(len(doc), self.max_pages_per_doc)):
                page = doc[page_num]
                text = page.get_text()
                
                if text.strip():  # Only add pages with content
                    pages.append(PageContent(
                        page_number=page_num + 1,
                        text=text.strip(),
                        structure_info={'blocks': page.get_text("dict")['blocks'][:5]}  # Limit structure info
                    ))
            
            doc.close()
            
        except Exception as e:
            raise ProcessingError(f"Error parsing PDF {pdf_path}: {str(e)}", "PDFParsingError")
        
        return pages
    
    def extract_document_structure(self, pdf_path: str) -> dict:
        """Extract basic document structure information"""
        try:
            doc = fitz.open(pdf_path)
            structure = {
                'page_count': len(doc),
                'title': doc.metadata.get('title', ''),
                'author': doc.metadata.get('author', ''),
                'subject': doc.metadata.get('subject', '')
            }
            doc.close()
            return structure
        except Exception as e:
            return {'error': str(e)}
    
    def handle_parsing_errors(self, pdf_path: str) -> dict:
        """Handle and log PDF parsing errors"""
        return {
            'error_type': 'PDFParsingError',
            'file': pdf_path,
            'status': 'failed',
            'message': f'Could not parse PDF: {pdf_path}'
        }
    
    def process_document(self, document_info: DocumentInfo, base_path: str = "") -> DocumentInfo:
        """Process a single document and populate its content"""
        pdf_path = os.path.join(base_path, document_info.filename)
        
        try:
            pages = self.extract_text_with_pages(pdf_path)
            document_info.pages = pages
            document_info.content = '\n\n'.join([page.text for page in pages])
            
        except ProcessingError as e:
            print(f"Warning: {e.message}")
            # Continue with empty content
            document_info.pages = []
            document_info.content = ""
        
        return document_info