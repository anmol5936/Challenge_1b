from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

@dataclass
class PageContent:
    page_number: int
    text: str
    structure_info: Optional[Dict] = None

@dataclass
class DocumentInfo:
    filename: str
    title: str
    content: str = ""
    pages: List[PageContent] = field(default_factory=list)

@dataclass
class PersonaInfo:
    role: str
    expertise_areas: List[str] = field(default_factory=list)
    focus_keywords: List[str] = field(default_factory=list)

@dataclass
class JobInfo:
    task: str
    requirements: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)

@dataclass
class Section:
    document: str
    title: str
    content: str
    page_number: int
    relevance_score: float = 0.0
    importance_rank: int = 0

@dataclass
class Subsection:
    document: str
    refined_text: str
    page_number: int
    quality_score: float = 0.0

@dataclass
class ChallengeInfo:
    challenge_id: str
    test_case_name: str
    description: str

@dataclass
class AnalysisContext:
    persona: PersonaInfo
    job: JobInfo
    document_collection: List[DocumentInfo]
    challenge_info: Optional[ChallengeInfo] = None

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)

class ProcessingError(Exception):
    def __init__(self, message: str, error_type: str = "ProcessingError"):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)