import json
from typing import Dict, Any, List
from src.models.data_models import (
    ValidationResult, ChallengeInfo, DocumentInfo, 
    PersonaInfo, JobInfo, ProcessingError
)

class InputValidator:
    def __init__(self):
        self.required_fields = {
            'challenge_info': ['challenge_id', 'test_case_name', 'description'],
            'documents': ['filename', 'title'],
            'persona': ['role'],
            'job_to_be_done': ['task']
        }
    
    def validate_input(self, json_data: Dict[str, Any]) -> ValidationResult:
        """Validate JSON input structure and required fields"""
        errors = []
        
        # Check top-level required fields
        required_top_level = ['challenge_info', 'documents', 'persona', 'job_to_be_done']
        for field in required_top_level:
            if field not in json_data:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return ValidationResult(is_valid=False, errors=errors)
        
        # Validate challenge_info structure
        challenge_info = json_data.get('challenge_info', {})
        for field in self.required_fields['challenge_info']:
            if field not in challenge_info:
                errors.append(f"Missing required field in challenge_info: {field}")
        
        # Validate documents array
        documents = json_data.get('documents', [])
        if not isinstance(documents, list) or len(documents) == 0:
            errors.append("Documents must be a non-empty array")
        else:
            for i, doc in enumerate(documents):
                for field in self.required_fields['documents']:
                    if field not in doc:
                        errors.append(f"Missing required field in document {i}: {field}")
        
        # Validate persona structure
        persona = json_data.get('persona', {})
        for field in self.required_fields['persona']:
            if field not in persona:
                errors.append(f"Missing required field in persona: {field}")
        
        # Validate job_to_be_done structure
        job = json_data.get('job_to_be_done', {})
        for field in self.required_fields['job_to_be_done']:
            if field not in job:
                errors.append(f"Missing required field in job_to_be_done: {field}")
        
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
    
    def extract_challenge_info(self, json_data: Dict[str, Any]) -> ChallengeInfo:
        """Extract challenge information from JSON input"""
        challenge_data = json_data['challenge_info']
        return ChallengeInfo(
            challenge_id=challenge_data['challenge_id'],
            test_case_name=challenge_data['test_case_name'],
            description=challenge_data['description']
        )
    
    def extract_documents(self, json_data: Dict[str, Any]) -> List[DocumentInfo]:
        """Extract document information from JSON input"""
        documents = []
        for doc_data in json_data['documents']:
            documents.append(DocumentInfo(
                filename=doc_data['filename'],
                title=doc_data['title']
            ))
        return documents
    
    def extract_persona(self, json_data: Dict[str, Any]) -> PersonaInfo:
        """Extract persona information from JSON input"""
        persona_data = json_data['persona']
        
        # Extract focus keywords from role description
        role = persona_data['role']
        focus_keywords = self._extract_keywords_from_role(role)
        
        return PersonaInfo(
            role=role,
            expertise_areas=persona_data.get('expertise_areas', []),
            focus_keywords=focus_keywords
        )
    
    def extract_job_to_be_done(self, json_data: Dict[str, Any]) -> JobInfo:
        """Extract job-to-be-done information from JSON input"""
        job_data = json_data['job_to_be_done']
        
        task = job_data['task']
        requirements = self._extract_requirements_from_task(task)
        
        return JobInfo(
            task=task,
            requirements=requirements,
            success_criteria=job_data.get('success_criteria', [])
        )
    
    def _extract_keywords_from_role(self, role: str) -> List[str]:
        """Extract focus keywords from persona role description"""
        keywords = []
        
        # Travel-related keywords
        travel_keywords = ['travel', 'trip', 'vacation', 'tourism', 'destination', 'hotel', 'restaurant', 'activity']
        # HR-related keywords  
        hr_keywords = ['HR', 'human resources', 'form', 'document', 'employee', 'management', 'workflow']
        # Culinary keywords
        culinary_keywords = ['chef', 'cooking', 'recipe', 'menu', 'food', 'catering', 'kitchen', 'culinary']
        
        role_lower = role.lower()
        
        for keyword in travel_keywords + hr_keywords + culinary_keywords:
            if keyword.lower() in role_lower:
                keywords.append(keyword)
        
        return keywords
    
    def _extract_requirements_from_task(self, task: str) -> List[str]:
        """Extract requirements from task description"""
        requirements = []
        
        # Extract common requirement patterns
        task_lower = task.lower()
        
        if 'plan' in task_lower:
            requirements.append('planning')
        if 'group' in task_lower:
            requirements.append('group coordination')
        if 'manage' in task_lower:
            requirements.append('management')
        if 'create' in task_lower:
            requirements.append('creation')
        if 'organize' in task_lower:
            requirements.append('organization')
        
        return requirements