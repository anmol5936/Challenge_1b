from typing import List, Tuple
from src.models.data_models import Section, PersonaInfo, JobInfo, AnalysisContext
from src.components.persona_analyzer import PersonaAnalyzer

class SectionRanker:
    def __init__(self):
        self.persona_analyzer = PersonaAnalyzer()
        
        # Scoring weights for different factors
        self.weights = {
            'relevance': 0.5,
            'uniqueness': 0.2,
            'completeness': 0.2,
            'length': 0.1
        }
    
    def rank_sections(self, sections: List[Section], persona: PersonaInfo, job: JobInfo) -> List[Section]:
        """Rank sections by importance and relevance"""
        if not sections:
            return []
        
        # Calculate scores for each section
        scored_sections = []
        for section in sections:
            score = self.calculate_importance_score(section, persona, job)
            section.relevance_score = score
            scored_sections.append((section, score))
        
        # Sort by score (highest first)
        scored_sections.sort(key=lambda x: x[1], reverse=True)
        
        # Assign importance ranks
        ranked_sections = []
        for rank, (section, score) in enumerate(scored_sections, 1):
            section.importance_rank = rank
            ranked_sections.append(section)
        
        return ranked_sections
    
    def calculate_importance_score(self, section: Section, persona: PersonaInfo, job: JobInfo) -> float:
        """Calculate importance score for a section"""
        # Calculate component scores
        relevance_score = self.persona_analyzer.calculate_combined_relevance(
            section.content, persona, job
        )
        
        uniqueness_score = self._calculate_uniqueness_score(section)
        completeness_score = self._calculate_completeness_score(section)
        length_score = self._calculate_length_score(section)
        
        # Apply weights and combine
        total_score = (
            relevance_score * self.weights['relevance'] +
            uniqueness_score * self.weights['uniqueness'] +
            completeness_score * self.weights['completeness'] +
            length_score * self.weights['length']
        )
        
        return total_score
    
    def apply_ranking_algorithm(self, scores: List[float]) -> List[int]:
        """Apply ranking algorithm to scores"""
        # Create list of (score, original_index) pairs
        score_index_pairs = [(score, i) for i, score in enumerate(scores)]
        
        # Sort by score (highest first)
        score_index_pairs.sort(key=lambda x: x[0], reverse=True)
        
        # Create ranking array
        rankings = [0] * len(scores)
        for rank, (score, original_index) in enumerate(score_index_pairs, 1):
            rankings[original_index] = rank
        
        return rankings
    
    def optimize_for_scoring_criteria(self, ranked_sections: List[Section]) -> List[Section]:
        """Optimize section ranking for competition scoring criteria"""
        # Ensure we have good coverage across different content types
        optimized_sections = []
        
        # Group sections by content type
        content_groups = self._group_sections_by_content_type(ranked_sections)
        
        # Ensure balanced representation
        for content_type, sections in content_groups.items():
            # Take top sections from each content type
            top_sections = sorted(sections, key=lambda x: x.relevance_score, reverse=True)[:3]
            optimized_sections.extend(top_sections)
        
        # Add remaining high-scoring sections
        remaining_sections = [s for s in ranked_sections if s not in optimized_sections]
        remaining_sections.sort(key=lambda x: x.relevance_score, reverse=True)
        optimized_sections.extend(remaining_sections[:5])
        
        # Re-rank the optimized list
        for rank, section in enumerate(optimized_sections, 1):
            section.importance_rank = rank
        
        return optimized_sections
    
    def _calculate_uniqueness_score(self, section: Section) -> float:
        """Calculate uniqueness score based on content diversity"""
        content = section.content.lower()
        
        # Count unique significant words (4+ characters)
        words = [word for word in content.split() if len(word) >= 4]
        unique_words = set(words)
        
        if not words:
            return 0.0
        
        uniqueness_ratio = len(unique_words) / len(words)
        return min(1.0, uniqueness_ratio * 2)  # Scale and cap at 1.0
    
    def _calculate_completeness_score(self, section: Section) -> float:
        """Calculate completeness score based on content structure"""
        content = section.content
        
        # Check for various completeness indicators
        score = 0.0
        
        # Has substantial content
        if len(content) > 200:
            score += 0.3
        
        # Has structured information (lists, numbers, etc.)
        if any(char in content for char in ['•', '-', '1.', '2.', ':']):
            score += 0.2
        
        # Has specific details (numbers, names, etc.)
        import re
        if re.search(r'\d+', content):
            score += 0.2
        
        # Has proper sentences
        sentence_count = len([s for s in content.split('.') if len(s.strip()) > 10])
        if sentence_count >= 3:
            score += 0.3
        
        return min(1.0, score)
    
    def _calculate_length_score(self, section: Section) -> float:
        """Calculate score based on content length"""
        content_length = len(section.content)
        
        # Optimal length range: 200-800 characters
        if 200 <= content_length <= 800:
            return 1.0
        elif content_length < 200:
            return content_length / 200
        else:
            # Penalize very long sections
            return max(0.5, 800 / content_length)
    
    def _group_sections_by_content_type(self, sections: List[Section]) -> dict:
        """Group sections by inferred content type"""
        groups = {
            'procedural': [],
            'descriptive': [],
            'informational': [],
            'other': []
        }
        
        for section in sections:
            content_lower = section.content.lower()
            
            # Procedural content (how-to, steps, instructions)
            if any(word in content_lower for word in ['step', 'process', 'procedure', 'how to', 'method']):
                groups['procedural'].append(section)
            # Descriptive content (descriptions, features, characteristics)
            elif any(word in content_lower for word in ['description', 'feature', 'characteristic', 'overview']):
                groups['descriptive'].append(section)
            # Informational content (facts, data, specifications)
            elif any(word in content_lower for word in ['information', 'data', 'fact', 'detail', 'specification']):
                groups['informational'].append(section)
            else:
                groups['other'].append(section)
        
        # Remove empty groups
        return {k: v for k, v in groups.items() if v}