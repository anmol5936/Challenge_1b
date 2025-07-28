#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.data_models import DocumentInfo, PersonaInfo, JobInfo, PageContent
from components.content_segmenter import ContentSegmenter
from components.persona_analyzer import PersonaAnalyzer
from components.section_ranker import SectionRanker
from components.subsection_refiner import SubsectionRefiner

def test_components():
    print("Testing PDF Analysis System Components")
    print("=" * 50)
    
    # Create sample document
    sample_content = """
    Travel Planning Guide
    
    Destination Overview
    Barcelona is a vibrant city in Spain known for its architecture, beaches, and culture. 
    The city offers numerous attractions for groups of friends looking for adventure.
    
    Accommodation Options
    For groups of 10 people, consider booking multiple rooms at Hotel Barcelona Center.
    The hotel offers group discounts and is located near major attractions.
    Alternatively, vacation rentals through Airbnb can provide more space and kitchen facilities.
    
    Activities and Attractions
    Visit the famous Sagrada Familia basilica designed by Antoni Gaudí.
    Explore Park Güell for stunning city views and unique architecture.
    Spend time at Barceloneta Beach for swimming and beach volleyball.
    Take a walking tour of the Gothic Quarter to learn about the city's history.
    
    Dining Recommendations
    Try traditional tapas at Bar del Pla in the Gothic Quarter.
    For group dining, make reservations at Restaurant 7 Portes, which can accommodate large parties.
    Don't miss trying paella at La Pepica, a restaurant with over 100 years of history.
    
    Transportation
    The Barcelona Metro system is efficient for getting around the city.
    Consider purchasing a T-10 ticket for multiple rides at a discounted rate.
    For airport transfers, book a private shuttle service for your group of 10.
    """
    
    document = DocumentInfo(
        filename="barcelona_guide.pdf",
        title="Barcelona Travel Guide",
        content=sample_content,
        pages=[PageContent(page_number=1, text=sample_content)]
    )
    
    # Create sample persona and job
    persona = PersonaInfo(
        role="Travel planning specialist helping a group of 10 college friends plan their 4-day trip",
        expertise_areas=["travel", "group coordination"],
        focus_keywords=["travel", "trip", "group", "friends", "accommodation", "activities"]
    )
    
    job = JobInfo(
        task="Plan a comprehensive 4-day itinerary for a group of 10 college friends, including accommodations, activities, and dining options",
        requirements=["planning", "group coordination"],
        success_criteria=["complete itinerary", "group-friendly options"]
    )
    
    print(f"Document: {document.title}")
    print(f"Content length: {len(document.content)} characters")
    print(f"Persona: {persona.role}")
    print(f"Task: {job.task[:100]}...")
    print()
    
    # Test content segmentation
    print("1. Testing Content Segmentation...")
    segmenter = ContentSegmenter()
    sections = segmenter.segment_by_headers(document)
    print(f"   Found {len(sections)} sections:")
    for i, section in enumerate(sections, 1):
        print(f"   {i}. {section.title} (Page {section.page_number})")
    print()
    
    # Test persona analysis
    print("2. Testing Persona Analysis...")
    analyzer = PersonaAnalyzer()
    for section in sections[:3]:  # Test first 3 sections
        relevance = analyzer.calculate_combined_relevance(section.content, persona, job)
        print(f"   '{section.title}': Relevance = {relevance:.3f}")
    print()
    
    # Test section ranking
    print("3. Testing Section Ranking...")
    ranker = SectionRanker()
    ranked_sections = ranker.rank_sections(sections, persona, job)
    print(f"   Ranked {len(ranked_sections)} sections:")
    for section in ranked_sections[:5]:  # Show top 5
        print(f"   Rank {section.importance_rank}: {section.title} (Score: {section.relevance_score:.3f})")
    print()
    
    # Test subsection refinement
    print("4. Testing Subsection Refinement...")
    refiner = SubsectionRefiner()
    if ranked_sections:
        top_section = ranked_sections[0]
        subsections = refiner.extract_subsections(top_section)
        print(f"   Generated {len(subsections)} subsections from '{top_section.title}':")
        for i, subsection in enumerate(subsections, 1):
            print(f"   {i}. Quality: {subsection.quality_score:.3f}")
            print(f"      Text: {subsection.refined_text[:100]}...")
    print()
    
    print("All components tested successfully!")

if __name__ == "__main__":
    test_components()