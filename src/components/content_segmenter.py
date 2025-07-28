import re
from typing import List, Tuple, Optional
from src.models.data_models import Section, DocumentInfo, PageContent

class ContentSegmenter:
    def __init__(self):
        # Header patterns for different document types
        self.header_patterns = [
            r'^#{1,6}\s+(.+)$',  # Markdown headers
            r'^[A-Z][A-Z\s]+$',  # ALL CAPS headers
            r'^\d+\.?\s+([A-Z].+)$',  # Numbered sections
            r'^[A-Z][a-z\s]+:$',  # Title case with colon
            r'^\*\*(.+)\*\*$',  # Bold markdown
        ]
        
        self.section_keywords = {
            'travel': ['destination', 'hotel', 'restaurant', 'activity', 'transportation', 'itinerary'],
            'hr': ['employee', 'form', 'policy', 'procedure', 'workflow', 'document'],
            'culinary': ['recipe', 'ingredient', 'preparation', 'cooking', 'menu', 'dietary']
        }
    
    def segment_by_headers(self, document: DocumentInfo) -> List[Section]:
        """Segment document content by identifying headers"""
        sections = []
        current_section = None
        current_content = []
        current_page = 1
        
        lines = document.content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a header
            header_match = self._is_header(line)
            
            if header_match:
                # Save previous section
                if current_section and current_content:
                    sections.append(Section(
                        document=document.filename,
                        title=current_section,
                        content='\n'.join(current_content),
                        page_number=current_page
                    ))
                
                # Start new section
                current_section = header_match
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
                else:
                    # If no section started yet, start with first substantial line
                    if len(line) > 10:
                        current_section = line[:50] + "..." if len(line) > 50 else line
                        current_content = [line]
                
                # Update page number based on content
                current_page = self._estimate_page_number(document, len('\n'.join(current_content)))
        
        # Add final section
        if current_section and current_content:
            sections.append(Section(
                document=document.filename,
                title=current_section,
                content='\n'.join(current_content),
                page_number=current_page
            ))
        
        # If no headers found, create sections by content breaks
        if not sections:
            sections = self._segment_by_content_breaks(document)
        
        return sections
    
    def segment_by_topics(self, document: DocumentInfo) -> List[Section]:
        """Segment document by topic similarity (simplified approach)"""
        # For performance, use simpler topic segmentation
        paragraphs = document.content.split('\n\n')
        sections = []
        
        current_section_content = []
        current_topic = "General Content"
        section_counter = 1
        
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph.strip()) > 50:  # Substantial content
                # Detect topic changes based on keywords
                new_topic = self._detect_topic(paragraph)
                
                if new_topic != current_topic and current_section_content:
                    # Create section for previous topic
                    sections.append(Section(
                        document=document.filename,
                        title=f"{current_topic} {section_counter}",
                        content='\n\n'.join(current_section_content),
                        page_number=self._estimate_page_number(document, i * 100)
                    ))
                    current_section_content = []
                    section_counter += 1
                
                current_topic = new_topic
                current_section_content.append(paragraph)
        
        # Add final section
        if current_section_content:
            sections.append(Section(
                document=document.filename,
                title=f"{current_topic} {section_counter}",
                content='\n\n'.join(current_section_content),
                page_number=self._estimate_page_number(document, len(paragraphs) * 100)
            ))
        
        return sections
    
    def identify_section_boundaries(self, text: str) -> List[Tuple[int, str]]:
        """Identify section boundaries in text"""
        boundaries = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            header = self._is_header(line.strip())
            if header:
                boundaries.append((i, header))
        
        return boundaries
    
    def extract_section_titles(self, sections: List[Section]) -> List[str]:
        """Extract and normalize section titles"""
        return [section.title for section in sections]
    
    def _is_header(self, line: str) -> Optional[str]:
        """Check if a line is a header and return the header text"""
        for pattern in self.header_patterns:
            match = re.match(pattern, line)
            if match:
                if match.groups():
                    return match.group(1).strip()
                else:
                    return line.strip()
        
        # Additional heuristics for headers
        if len(line) < 100 and line.isupper():
            return line.strip()
        
        if len(line) < 80 and ':' in line and not line.endswith('.'):
            return line.strip()
        
        # Check for standalone lines that look like headers (short, title case)
        words = line.split()
        if (len(words) <= 6 and len(line) <= 80 and 
            all(word[0].isupper() or word.lower() in ['and', 'or', 'the', 'of', 'for', 'in', 'to'] 
                for word in words if word) and
            not line.endswith('.') and not line.endswith(',') and
            len(line) > 5):
            return line.strip()
        
        return None
    
    def _segment_by_content_breaks(self, document: DocumentInfo) -> List[Section]:
        """Create sections based on natural content breaks"""
        sections = []
        paragraphs = [p.strip() for p in document.content.split('\n\n') if p.strip()]
        
        # Group paragraphs into sections of reasonable size
        section_size = max(3, len(paragraphs) // 5)  # At least 3 paragraphs per section
        
        for i in range(0, len(paragraphs), section_size):
            section_paragraphs = paragraphs[i:i + section_size]
            
            # Generate title from first paragraph
            title = self._generate_section_title(section_paragraphs[0])
            
            sections.append(Section(
                document=document.filename,
                title=title,
                content='\n\n'.join(section_paragraphs),
                page_number=self._estimate_page_number(document, i * 200)
            ))
        
        return sections
    
    def _generate_section_title(self, first_paragraph: str) -> str:
        """Generate a section title from the first paragraph"""
        # Take first sentence and truncate to reasonable length
        first_sentence = first_paragraph.split('.')[0]
        if len(first_sentence) > 60:
            first_sentence = first_sentence[:60] + "..."
        
        return first_sentence.strip()
    
    def _detect_topic(self, paragraph: str) -> str:
        """Detect topic of paragraph based on keywords"""
        paragraph_lower = paragraph.lower()
        
        for topic, keywords in self.section_keywords.items():
            keyword_count = sum(1 for keyword in keywords if keyword in paragraph_lower)
            if keyword_count >= 2:
                return topic.title()
        
        return "General Content"
    
    def _estimate_page_number(self, document: DocumentInfo, char_position: int) -> int:
        """Estimate page number based on character position"""
        if not document.pages:
            return 1
        
        total_chars = len(document.content)
        if total_chars == 0:
            return 1
        
        page_ratio = char_position / total_chars
        estimated_page = int(page_ratio * len(document.pages)) + 1
        
        return min(estimated_page, len(document.pages))