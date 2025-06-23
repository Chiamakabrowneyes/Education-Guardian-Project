"""
Essay Mentor Agent

This agent provides comprehensive essay writing assistance and guidance.
"""

from typing import Dict, Any, List
from google.adk.agents import Agent
from ..tools.user_profile_tool import user_profile_tool
from ..utils.state_utils import (
    get_user_background,
    get_academic_profile,
    get_university_preferences,
    get_extracurriculars,
    get_aspirations,
    update_interaction_history
)
import google.adk as adk
import os

adk.configure(api_key=os.getenv("api_key"))
def analyze_essay_requirements(tool_context) -> Dict[str, Any]:
    """
    Analyze essay requirements and user profile for personalized guidance.
    
    Args:
        tool_context: The tool context containing session information
        
    Returns:
        Dict containing essay requirements analysis
    """
    # Get relevant user profile sections
    background = get_user_background(tool_context)
    academic = get_academic_profile(tool_context)
    universities = get_university_preferences(tool_context)
    activities = get_extracurriculars(tool_context)
    aspirations = get_aspirations(tool_context)
    
    # Log the analysis
    update_interaction_history(
        tool_context,
        "Analyzed essay requirements",
        "success",
        {
            "background": background,
            "academic": academic,
            "universities": universities,
            "activities": activities,
            "aspirations": aspirations
        }
    )
    
    return {
        "result": "Essay requirements analyzed",
        "stats": {
            "target_universities": len(universities.get("target_universities", [])),
            "extracurricular_count": len(activities.get("activities", [])),
            "english_proficiency": academic.get("english_proficiency")
        },
        "additional_info": {
            "background": background,
            "academic": academic,
            "universities": universities,
            "activities": activities,
            "aspirations": aspirations
        }
    }

def generate_essay_topics(tool_context) -> Dict[str, Any]:
    """
    Generate personalized essay topics based on user profile.
    
    Args:
        tool_context: The tool context containing session information
        
    Returns:
        Dict containing suggested essay topics
    """
    # Get relevant profile sections
    background = get_user_background(tool_context)
    activities = get_extracurriculars(tool_context)
    aspirations = get_aspirations(tool_context)
    
    # Generate topics based on user's background and experiences
    topics = []
    
    # Personal background topics
    if background.get("travel_experience"):
        topics.append({
            "category": "Personal Growth",
            "topic": "Cultural Adaptation",
            "description": "How your travel experiences shaped your perspective",
            "relevance": "Shows adaptability and global awareness"
        })
    
    # Academic topics
    if background.get("education_challenges"):
        topics.append({
            "category": "Overcoming Challenges",
            "topic": "Educational Journey",
            "description": "How you overcame educational challenges",
            "relevance": "Demonstrates resilience and determination"
        })
    
    # Extracurricular topics
    if activities.get("activities"):
        topics.append({
            "category": "Leadership",
            "topic": "Activity Impact",
            "description": "How your extracurricular activities influenced your growth",
            "relevance": "Shows leadership and community involvement"
        })
    
    # Career aspirations
    if aspirations.get("dream_career"):
        topics.append({
            "category": "Future Goals",
            "topic": "Career Vision",
            "description": "How your experiences shaped your career goals",
            "relevance": "Shows long-term planning and motivation"
        })
    
    # Log the topic generation
    update_interaction_history(
        tool_context,
        "Generated essay topics",
        "success",
        {"topics": topics}
    )
    
    return {
        "result": "Generated personalized essay topics",
        "stats": {
            "total_topics": len(topics),
            "categories": list(set(t["category"] for t in topics))
        },
        "additional_info": {
            "topics": topics
        }
    }

essay_mentor_agent = Agent(
    name="essay_mentor_agent",
    model="gemini-2.0-flash",
    description="Provides comprehensive essay writing assistance and guidance",
    instruction="""You are an essay writing mentor specializing in college application essays. Your role is to:

1. Essay Planning and Strategy:
   - Analyze user profile to identify compelling stories and experiences
   - Help select appropriate essay topics that:
     * Showcase unique qualities
     * Demonstrate growth and learning
     * Align with university values
     * Complement other application materials
   - Create a comprehensive essay plan for all required essays

2. Personal Statement Guidance:
   - Help craft a compelling personal statement that:
     * Tells a unique story
     * Shows personality and voice
     * Demonstrates self-reflection
     * Highlights key achievements
   - Provide structure and organization advice
   - Guide the writing process step by step

3. Supplemental Essays:
   - Help with university-specific essays
   - Guide responses to "Why this school?" prompts
   - Assist with activity and achievement descriptions
   - Help craft responses to unique prompts

4. Writing Process Support:
   - Provide detailed feedback on:
     * Content and message
     * Structure and flow
     * Voice and tone
     * Grammar and style
   - Guide revisions and improvements
   - Help meet word limits
   - Ensure clarity and impact

5. Essay Portfolio Management:
   - Track all required essays
   - Monitor deadlines
   - Ensure consistency across essays
   - Maintain quality standards
   - Coordinate with other application components

6. Best Practices:
   - Guide on:
     * Brainstorming techniques
     * Outlining methods
     * Drafting strategies
     * Revision processes
     * Proofreading tips
   - Share successful essay examples
   - Provide writing resources
   - Offer stress management tips

Use the user_profile_tool to gather and update user information.
Use the state utilities to access user profile information for personalized guidance.""",
    tools=[user_profile_tool]
) 