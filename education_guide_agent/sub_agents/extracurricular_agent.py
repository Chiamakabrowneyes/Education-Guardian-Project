"""
Extracurricular Activities Agent

This agent helps manage and develop extracurricular activities for college applications.
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

def analyze_activity_profile(tool_context) -> Dict[str, Any]:
    """
    Analyze extracurricular activity profile based on user information.
    
    Args:
        tool_context: The tool context containing session information
        
    Returns:
        Dict containing activity profile analysis
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
        "Analyzed activity profile",
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
        "result": "Activity profile analyzed",
        "stats": {
            "current_activities": len(activities.get("activities", [])),
            "hobbies": len(activities.get("hobbies", [])),
            "leadership_interest": activities.get("leadership_interest", False)
        },
        "additional_info": {
            "background": background,
            "academic": academic,
            "universities": universities,
            "activities": activities,
            "aspirations": aspirations
        }
    }

def generate_activity_recommendations(tool_context) -> Dict[str, Any]:
    """
    Generate activity recommendations based on user profile.
    
    Args:
        tool_context: The tool context containing session information
        
    Returns:
        Dict containing activity recommendations
    """
    # Get relevant profile sections
    academic = get_academic_profile(tool_context)
    activities = get_extracurriculars(tool_context)
    aspirations = get_aspirations(tool_context)
    
    # Generate recommendations based on profile
    recommendations = {
        "academic_activities": [],
        "leadership_opportunities": [],
        "community_service": [],
        "personal_development": []
    }
    
    # Academic activities
    if academic.get("field_of_study"):
        recommendations["academic_activities"].append({
            "type": "Research Project",
            "description": "Undertake a research project in your field of interest",
            "benefits": [
                "Develops research skills",
                "Shows academic initiative",
                "Demonstrates subject knowledge",
                "Builds relationships with professors"
            ],
            "implementation": [
                "Identify research topic",
                "Find faculty mentor",
                "Create project timeline",
                "Document findings"
            ]
        })
    
    # Leadership opportunities
    if activities.get("leadership_interest"):
        recommendations["leadership_opportunities"].append({
            "type": "Club Leadership",
            "description": "Take on a leadership role in an existing club or start a new one",
            "benefits": [
                "Develops leadership skills",
                "Shows initiative",
                "Demonstrates organizational abilities",
                "Builds community"
            ],
            "implementation": [
                "Identify club opportunities",
                "Plan leadership approach",
                "Set goals and objectives",
                "Track impact and outcomes"
            ]
        })
    
    # Community service
    recommendations["community_service"].append({
        "type": "Volunteer Program",
        "description": "Participate in or organize a community service project",
        "benefits": [
            "Shows social responsibility",
            "Develops empathy",
            "Builds community connections",
            "Demonstrates commitment"
        ],
        "implementation": [
            "Identify community needs",
            "Find suitable programs",
            "Plan regular involvement",
            "Document impact"
        ]
    })
    
    # Personal development
    if activities.get("hobbies"):
        recommendations["personal_development"].append({
            "type": "Skill Development",
            "description": "Develop skills related to your hobbies and interests",
            "benefits": [
                "Shows dedication",
                "Demonstrates growth",
                "Adds unique perspective",
                "Builds expertise"
            ],
            "implementation": [
                "Set skill goals",
                "Find learning resources",
                "Practice regularly",
                "Track progress"
            ]
        })
    
    # Log the recommendations
    update_interaction_history(
        tool_context,
        "Generated activity recommendations",
        "success",
        {"recommendations": recommendations}
    )
    
    return {
        "result": "Generated activity recommendations",
        "stats": {
            "total_recommendations": sum(len(v) for v in recommendations.values()),
            "categories": list(recommendations.keys())
        },
        "additional_info": {
            "recommendations": recommendations
        }
    }

extracurricular_agent = Agent(
    name="extracurricular_agent",
    model="gemini-2.0-flash",
    description="Helps manage and develop extracurricular activities",
    instruction="""You are an extracurricular activities specialist. Your role is to:

1. Activity Analysis:
   - Analyze current activities:
     * Types of involvement
     * Time commitment
     * Leadership roles
     * Impact and achievements
   - Consider:
     * Academic interests
     * Career goals
     * Personal strengths
     * Available opportunities

2. Activity Planning:
   - Help develop a balanced activity portfolio:
     * Academic activities
     * Leadership roles
     * Community service
     * Personal interests
   - Consider:
     * Time management
     * Skill development
     * Impact potential
     * University preferences

3. Leadership Development:
   - Identify opportunities for:
     * Club leadership
     * Project management
     * Team coordination
     * Initiative taking
   - Guide through:
     * Role selection
     * Goal setting
     * Implementation
     * Impact tracking

4. Community Engagement:
   - Help find and develop:
     * Volunteer opportunities
     * Service projects
     * Community initiatives
     * Social impact activities
   - Focus on:
     * Meaningful contribution
     * Sustainable involvement
     * Measurable impact
     * Personal growth

5. Skill Building:
   - Guide development of:
     * Technical skills
     * Soft skills
     * Leadership abilities
     * Specialized knowledge
   - Through:
     * Workshops
     * Online courses
     * Mentorship
     * Practice opportunities

6. Progress Tracking:
   - Monitor:
     * Activity involvement
     * Achievement progress
     * Skill development
     * Impact metrics
   - Maintain:
     * Activity logs
     * Achievement records
     * Skill assessments
     * Impact documentation

Use the user_profile_tool to gather and update user information.
Use the state utilities to access user profile information for personalized guidance.""",
    tools=[user_profile_tool]
) 