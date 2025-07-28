from typing import List, Dict, Any
import re
import numpy as np
from src.models.data_models import PersonaInfo, JobInfo, Section

# Try to import sentence transformers, fall back to basic analysis if not available
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except (ImportError, ValueError) as e:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print(f"Warning: sentence-transformers not available ({e}), using basic keyword analysis")

class PersonaAnalyzer:
    def __init__(self):
        # Initialize sentence transformer model if available
        self.model = None
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                # Use a lightweight model that fits within 1GB constraint
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                print("Loaded sentence transformer model: all-MiniLM-L6-v2")
            except Exception as e:
                print(f"Failed to load sentence transformer: {e}")
                self.model = None
        
        # Domain-specific keyword weights
        self.domain_keywords = {
            'travel': {
                'high': ['destination', 'hotel', 'restaurant', 'activity', 'beach', 'city', 'tour', 'accommodation'],
                'medium': ['travel', 'trip', 'vacation', 'visit', 'location', 'transportation', 'guide'],
                'low': ['place', 'area', 'time', 'day', 'experience', 'local']
            },
            'hr': {
                'high': ['form', 'employee', 'document', 'workflow', 'signature', 'field', 'fillable'],
                'medium': ['HR', 'human resources', 'policy', 'procedure', 'management', 'corporate'],
                'low': ['staff', 'personnel', 'organization', 'company', 'business']
            },
            'culinary': {
                'high': ['recipe', 'ingredient', 'cooking', 'chef', 'menu', 'food', 'kitchen', 'dietary'],
                'medium': ['preparation', 'cuisine', 'dish', 'meal', 'catering', 'restaurant'],
                'low': ['taste', 'flavor', 'eating', 'dining', 'service']
            }
        }
        
        # Job-specific keywords
        self.job_keywords = {
            'planning': ['plan', 'organize', 'schedule', 'coordinate', 'arrange'],
            'management': ['manage', 'oversee', 'supervise', 'control', 'handle'],
            'creation': ['create', 'develop', 'design', 'build', 'generate'],
            'analysis': ['analyze', 'evaluate', 'assess', 'review', 'examine']
        }
    
    def analyze_persona_relevance(self, content: str, persona: PersonaInfo) -> float:
        """Analyze content relevance based on persona characteristics"""
        content_lower = content.lower()
        role_lower = persona.role.lower()
        
        # Use semantic similarity if available
        if self.model is not None:
            semantic_score = self._calculate_semantic_similarity(content, persona.role)
        else:
            semantic_score = 0.0
        
        # Determine primary domain from persona role
        primary_domain = self._identify_primary_domain(role_lower)
        
        # Calculate domain-specific keyword relevance
        domain_score = self._calculate_domain_keyword_score(content_lower, primary_domain)
        
        # Calculate role-specific relevance
        role_score = self._calculate_role_relevance(content_lower, role_lower)
        
        # Calculate expertise area relevance
        expertise_score = self._calculate_expertise_relevance(content_lower, persona.expertise_areas)
        
        # Combine scores with weights (prioritize semantic similarity if available)
        if self.model is not None:
            total_score = (
                semantic_score * 0.4 +
                domain_score * 0.3 +
                role_score * 0.2 +
                expertise_score * 0.1
            )
        else:
            total_score = (
                domain_score * 0.5 +
                role_score * 0.3 +
                expertise_score * 0.2
            )
        
        return min(1.0, total_score)
    
    def analyze_job_relevance(self, content: str, job: JobInfo) -> float:
        """Analyze content relevance based on job requirements"""
        content_lower = content.lower()
        task_lower = job.task.lower()
        
        # Use semantic similarity if available
        if self.model is not None:
            semantic_score = self._calculate_semantic_similarity(content, job.task)
        else:
            semantic_score = 0.0
        
        # Calculate task keyword relevance
        task_score = self._calculate_task_relevance(content_lower, task_lower)
        
        # Calculate requirements relevance
        requirements_score = self._calculate_requirements_relevance(content_lower, job.requirements)
        
        # Combine scores (prioritize semantic similarity if available)
        if self.model is not None:
            total_score = (
                semantic_score * 0.5 +
                task_score * 0.3 +
                requirements_score * 0.2
            )
        else:
            total_score = (task_score * 0.7 + requirements_score * 0.3)
        
        return min(1.0, total_score)
    
    def extract_persona_keywords(self, persona: PersonaInfo) -> List[str]:
        """Extract relevant keywords from persona information"""
        keywords = []
        
        # Add focus keywords
        keywords.extend(persona.focus_keywords)
        
        # Extract keywords from role
        role_keywords = self._extract_keywords_from_text(persona.role)
        keywords.extend(role_keywords)
        
        # Add expertise area keywords
        for area in persona.expertise_areas:
            area_keywords = self._extract_keywords_from_text(area)
            keywords.extend(area_keywords)
        
        return list(set(keywords))  # Remove duplicates
    
    def calculate_combined_relevance(self, content: str, persona: PersonaInfo, job: JobInfo) -> float:
        """Calculate combined relevance score for persona and job"""
        persona_relevance = self.analyze_persona_relevance(content, persona)
        job_relevance = self.analyze_job_relevance(content, job)
        
        # Weight persona and job relevance
        combined_score = (persona_relevance * 0.6 + job_relevance * 0.4)
        
        return combined_score
    
    def _identify_primary_domain(self, role: str) -> str:
        """Identify primary domain from persona role"""
        if any(keyword in role for keyword in ['travel', 'trip', 'vacation', 'tour']):
            return 'travel'
        elif any(keyword in role for keyword in ['hr', 'human resources', 'employee', 'form']):
            return 'hr'
        elif any(keyword in role for keyword in ['chef', 'cook', 'culinary', 'kitchen', 'food']):
            return 'culinary'
        else:
            return 'general'
    
    def _calculate_domain_keyword_score(self, content: str, domain: str) -> float:
        """Calculate relevance score based on domain-specific keywords"""
        if domain not in self.domain_keywords:
            return 0.0
        
        domain_keywords = self.domain_keywords[domain]
        total_score = 0.0
        total_words = len(content.split())
        
        if total_words == 0:
            return 0.0
        
        # Count keyword occurrences with different weights
        for weight, keywords in [('high', domain_keywords['high']), 
                                ('medium', domain_keywords['medium']), 
                                ('low', domain_keywords['low'])]:
            weight_multiplier = {'high': 3.0, 'medium': 2.0, 'low': 1.0}[weight]
            
            for keyword in keywords:
                count = content.count(keyword)
                total_score += (count / total_words) * weight_multiplier
        
        return min(1.0, total_score * 10)  # Scale up and cap at 1.0
    
    def _calculate_role_relevance(self, content: str, role: str) -> float:
        """Calculate relevance based on role-specific terms"""
        role_words = role.split()
        content_words = content.split()
        
        if not role_words or not content_words:
            return 0.0
        
        # Simple term frequency approach
        matches = 0
        for role_word in role_words:
            if len(role_word) > 3:  # Skip short words
                matches += content.count(role_word.lower())
        
        return min(1.0, matches / len(content_words) * 50)
    
    def _calculate_expertise_relevance(self, content: str, expertise_areas: List[str]) -> float:
        """Calculate relevance based on expertise areas"""
        if not expertise_areas:
            return 0.0
        
        total_score = 0.0
        for area in expertise_areas:
            area_words = area.lower().split()
            for word in area_words:
                if len(word) > 3:
                    total_score += content.count(word)
        
        content_length = len(content.split())
        if content_length == 0:
            return 0.0
        
        return min(1.0, total_score / content_length * 20)
    
    def _calculate_task_relevance(self, content: str, task: str) -> float:
        """Calculate relevance based on task description"""
        task_words = [word.lower() for word in task.split() if len(word) > 3]
        
        if not task_words:
            return 0.0
        
        matches = 0
        for word in task_words:
            matches += content.count(word)
        
        content_length = len(content.split())
        if content_length == 0:
            return 0.0
        
        return min(1.0, matches / content_length * 30)
    
    def _calculate_requirements_relevance(self, content: str, requirements: List[str]) -> float:
        """Calculate relevance based on job requirements"""
        if not requirements:
            return 0.0
        
        total_score = 0.0
        for requirement in requirements:
            if requirement in self.job_keywords:
                keywords = self.job_keywords[requirement]
                for keyword in keywords:
                    total_score += content.count(keyword)
        
        content_length = len(content.split())
        if content_length == 0:
            return 0.0
        
        return min(1.0, total_score / content_length * 25)
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        # Remove common stop words and extract meaningful terms
        words = re.findall(r'\b\w{4,}\b', text.lower())  # Words with 4+ characters
        
        stop_words = {'with', 'that', 'this', 'they', 'them', 'from', 'have', 'been', 'were', 'will'}
        keywords = [word for word in words if word not in stop_words]
        
        return keywords[:10]  # Limit to top 10 keywords
    
    def _calculate_semantic_similarity(self, content: str, reference_text: str) -> float:
        """Calculate semantic similarity using sentence transformers"""
        if self.model is None:
            return 0.0
        
        try:
            # Split content into sentences for better analysis
            content_sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
            
            if not content_sentences:
                return 0.0
            
            # Limit to top 5 sentences to avoid performance issues
            content_sentences = content_sentences[:5]
            
            # Encode reference text and content sentences
            reference_embedding = self.model.encode([reference_text])
            content_embeddings = self.model.encode(content_sentences)
            
            # Calculate cosine similarities
            similarities = []
            for content_embedding in content_embeddings:
                # Reshape for cosine similarity calculation
                ref_emb = reference_embedding[0].reshape(1, -1)
                cont_emb = content_embedding.reshape(1, -1)
                
                # Calculate cosine similarity
                dot_product = np.dot(ref_emb, cont_emb.T)[0][0]
                norm_ref = np.linalg.norm(ref_emb)
                norm_cont = np.linalg.norm(cont_emb)
                
                if norm_ref > 0 and norm_cont > 0:
                    similarity = dot_product / (norm_ref * norm_cont)
                    similarities.append(similarity)
            
            if similarities:
                # Return the maximum similarity score
                return max(similarities)
            else:
                return 0.0
                
        except Exception as e:
            print(f"Error calculating semantic similarity: {e}")
            return 0.0