"""
University Matching Agent

This agent helps match students with suitable universities based on their profile and preferences.
"""

from typing import Dict, Any, List
from google.adk.agents import Agent
from ..tools.user_profile_tool import user_profile_tool
from ..utils.state_utils import (
    get_user_background,
    get_academic_profile,
    get_university_preferences,
    get_financial_constraints,
    get_extracurriculars,
    get_aspirations,
    update_interaction_history
)

def analyze_university_fit(tool_context) -> Dict[str, Any]:
    """
    Analyze university fit based on user profile.
    
    Args:
        tool_context: The tool context containing session information
        
    Returns:
        Dict containing university fit analysis
    """
    # Get relevant user profile sections
    background = get_user_background(tool_context)
    academic = get_academic_profile(tool_context)
    preferences = get_university_preferences(tool_context)
    financial = get_financial_constraints(tool_context)
    activities = get_extracurriculars(tool_context)
    aspirations = get_aspirations(tool_context)
    
    # Log the analysis
    update_interaction_history(
        tool_context,
        "Analyzed university fit",
        "success",
        {
            "background": background,
            "academic": academic,
            "preferences": preferences,
            "financial": financial,
            "activities": activities,
            "aspirations": aspirations
        }
    )
    
    return {
        "result": "University fit analyzed",
        "stats": {
            "gpa": academic.get("gpa"),
            "target_universities": len(preferences.get("target_universities", [])),
            "field_of_study": preferences.get("field_of_study"),
            "budget_range": financial.get("budget")
        },
        "additional_info": {
            "background": background,
            "academic": academic,
            "preferences": preferences,
            "financial": financial,
            "activities": activities,
            "aspirations": aspirations
        }
    }

def generate_university_recommendations(tool_context) -> Dict[str, Any]:
    """
    Generate university recommendations based on user profile.
    
    Args:
        tool_context: The tool context containing session information
        
    Returns:
        Dict containing university recommendations
    """
    # Get relevant profile sections
    academic = get_academic_profile(tool_context)
    preferences = get_university_preferences(tool_context)
    financial = get_financial_constraints(tool_context)
    
    # Generate recommendations based on profile
    recommendations = {
        "reach": [],
        "target": [],
        "safety": []
    }
    
    # Example recommendation logic (to be expanded)
    if academic.get("gpa") and preferences.get("field_of_study"):
        recommendations["target"].append({
            "name": "Example University",
            "match_reasons": [
                "Strong program in your field",
                "Matches your academic profile",
                "Within your budget range"
            ],
            "requirements": {
                "gpa": "3.5+",
                "tests": ["SAT", "TOEFL"],
                "deadlines": {
                    "early": "November 1",
                    "regular": "January 15"
                }
            }
        })
    
    # Log the recommendations
    update_interaction_history(
        tool_context,
        "Generated university recommendations",
        "success",
        {"recommendations": recommendations}
    )
    
    return {
        "result": "Generated university recommendations",
        "stats": {
            "total_recommendations": sum(len(v) for v in recommendations.values()),
            "categories": list(recommendations.keys())
        },
        "additional_info": {
            "recommendations": recommendations
        }
    }

university_matching_agent = Agent(
    name="university_matching_agent",
    model="gemini-2.0-flash",
    description="Helps match students with suitable universities",
    instruction="""You are a university matching specialist. Your role is to:

1. Profile Analysis:
   - Analyze user's:
     * Academic background
     * Test scores
     * Extracurricular activities
     * Financial constraints
     * Location preferences
     * Field of study interests
   - Consider:
     * Country of origin
     * Language proficiency
     * Cultural fit
     * Career goals

2. University Matching:
   - Match students with universities based on:
     * Academic fit
     * Program strength
     * Location preferences
     * Size preferences
     * Financial considerations
     * Cultural environment
   - Categorize schools as:
     * Reach
     * Target
     * Safety

3. Requirements Analysis:
   - Identify:
     * Required tests
     * Minimum GPAs
     * Application deadlines
     * Required documents
     * Language requirements
     * Financial aid options

4. Personalized Recommendations:
   - Provide detailed information about:
     * Program strengths
     * Campus culture
     * Student life
     * Career services
     * Alumni network
     * International student support

5. Application Strategy:
   - Help develop a balanced application list
   - Consider:
     * Application deadlines
     * Early decision options
     * Scholarship opportunities
     * Visa requirements
     * Housing options

6. Progress Tracking:
   - Monitor:
     * Application status
     * Document submission
     * Test score updates
     * Financial aid applications
     * Visa applications

Use the user_profile_tool to gather and update user information.
Use the state utilities to access user profile information for personalized matching.""",
    tools=[user_profile_tool]
) 