"""
Recommendation Letter Agent

This agent helps manage and coordinate recommendation letters for college applications.
"""

from typing import Dict, Any, List
from google.adk.agents import Agent
from ..tools.user_profile_tool import user_profile_tool
from ..utils.state_utils import (
    get_academic_profile,
    get_university_preferences,
    get_application_readiness,
    get_extracurriculars,
    update_interaction_history
)
import google.adk as adk
import os

adk.configure(api_key=os.getenv("api_key"))
def analyze_recommendation_needs(tool_context) -> Dict[str, Any]:
    """
    Analyze recommendation letter requirements based on user profile.
    
    Args:
        tool_context: The tool context containing session information
        
    Returns:
        Dict containing recommendation needs analysis
    """
    # Get relevant user profile sections
    academic = get_academic_profile(tool_context)
    universities = get_university_preferences(tool_context)
    readiness = get_application_readiness(tool_context)
    activities = get_extracurriculars(tool_context)
    
    # Log the analysis
    update_interaction_history(
        tool_context,
        "Analyzed recommendation needs",
        "success",
        {
            "academic": academic,
            "universities": universities,
            "readiness": readiness,
            "activities": activities
        }
    )
    
    return {
        "result": "Recommendation needs analyzed",
        "stats": {
            "target_universities": len(universities.get("target_universities", [])),
            "recommenders_available": readiness.get("recommenders_available", 0),
            "extracurricular_count": len(activities.get("activities", []))
        },
        "additional_info": {
            "academic": academic,
            "universities": universities,
            "readiness": readiness,
            "activities": activities
        }
    }

def generate_recommender_guidance(tool_context) -> Dict[str, Any]:
    """
    Generate guidance for recommenders based on user profile.
    
    Args:
        tool_context: The tool context containing session information
        
    Returns:
        Dict containing recommender guidance
    """
    # Get relevant profile sections
    academic = get_academic_profile(tool_context)
    activities = get_extracurriculars(tool_context)
    universities = get_university_preferences(tool_context)
    
    # Generate guidance based on profile
    guidance = {
        "academic_recommenders": [],
        "activity_recommenders": [],
        "general_guidance": []
    }
    
    # Academic recommender guidance
    if academic.get("gpa") and academic.get("school_type"):
        guidance["academic_recommenders"].append({
            "type": "Teacher",
            "focus_areas": [
                "Academic performance",
                "Class participation",
                "Intellectual curiosity",
                "Work ethic"
            ],
            "key_points": [
                "Highlight specific achievements",
                "Provide concrete examples",
                "Discuss growth and improvement",
                "Address academic challenges overcome"
            ]
        })
    
    # Activity recommender guidance
    if activities.get("activities"):
        guidance["activity_recommenders"].append({
            "type": "Activity Supervisor",
            "focus_areas": [
                "Leadership skills",
                "Teamwork abilities",
                "Initiative and creativity",
                "Impact and contribution"
            ],
            "key_points": [
                "Describe specific projects",
                "Highlight leadership roles",
                "Discuss impact on others",
                "Show personal growth"
            ]
        })
    
    # General guidance
    guidance["general_guidance"] = [
        "Provide specific examples",
        "Use concrete details",
        "Highlight unique qualities",
        "Address university requirements",
        "Maintain professional tone",
        "Focus on recent experiences"
    ]
    
    # Log the guidance generation
    update_interaction_history(
        tool_context,
        "Generated recommender guidance",
        "success",
        {"guidance": guidance}
    )
    
    return {
        "result": "Generated recommender guidance",
        "stats": {
            "total_recommender_types": len(guidance["academic_recommenders"]) + len(guidance["activity_recommenders"]),
            "guidance_points": len(guidance["general_guidance"])
        },
        "additional_info": {
            "guidance": guidance
        }
    }

recommendation_agent = Agent(
    name="recommendation_agent",
    model="gemini-2.0-flash",
    description="Helps manage and coordinate recommendation letters",
    instruction="""You are a recommendation letter specialist. Your role is to:

1. Requirements Analysis:
   - Analyze:
     * University requirements
     * Number of letters needed
     * Types of recommenders required
     * Submission deadlines
     * Format requirements
   - Consider:
     * Academic vs. activity letters
     * Subject-specific requirements
     * Language requirements
     * Cultural context

2. Recommender Selection:
   - Help identify appropriate recommenders:
     * Academic teachers
     * Activity supervisors
     * Community leaders
     * Professional mentors
   - Consider:
     * Relationship strength
     * Writing ability
     * Knowledge of student
     * Availability

3. Request Management:
   - Guide through:
     * Initial requests
     * Follow-up communications
     * Deadline reminders
     * Submission tracking
   - Provide:
     * Request templates
     * Follow-up scripts
     * Thank you notes
     * Status updates

4. Content Guidance:
   - Help recommenders with:
     * Key points to address
     * Specific examples to include
     * Format and structure
     * Language and tone
   - Ensure:
     * Comprehensive coverage
     * Personal insights
     * Specific examples
     * Professional tone

5. Quality Assurance:
   - Review recommendations for:
     * Completeness
     * Specificity
     * Professionalism
     * Cultural sensitivity
   - Provide:
     * Feedback for improvement
     * Revision suggestions
     * Best practices
     * Examples

6. Submission Tracking:
   - Monitor:
     * Request status
     * Submission deadlines
     * Confirmation receipts
     * Follow-up needs
   - Maintain:
     * Status records
     * Communication logs
     * Deadline calendar
     * Action items

Use the user_profile_tool to gather and update user information.
Use the state utilities to access user profile information for personalized guidance.""",
    tools=[user_profile_tool]
) 