"""
Test Preparation Agent

This agent provides comprehensive test preparation guidance and strategies.
"""

from typing import Dict, Any, List
from google.adk.agents import Agent
from ..tools.user_profile_tool import user_profile_tool
from ..utils.state_utils import (
    get_academic_profile,
    get_university_preferences,
    get_application_readiness,
    update_interaction_history
)

def analyze_test_requirements(tool_context) -> Dict[str, Any]:
    """
    Analyze test requirements based on user profile.
    
    Args:
        tool_context: The tool context containing session information
        
    Returns:
        Dict containing test requirements analysis
    """
    # Get relevant user profile sections
    academic_profile = get_academic_profile(tool_context)
    university_preferences = get_university_preferences(tool_context)
    application_readiness = get_application_readiness(tool_context)
    
    # Log the analysis
    update_interaction_history(
        tool_context,
        "Analyzed test requirements",
        "success",
        {
            "academic_profile": academic_profile,
            "university_preferences": university_preferences,
            "application_readiness": application_readiness
        }
    )
    
    return {
        "result": "Test requirements analyzed",
        "stats": {
            "tests_required": len(academic_profile.get("standardized_tests", [])),
            "english_proficiency": academic_profile.get("english_proficiency"),
            "target_universities": len(university_preferences.get("target_universities", []))
        },
        "additional_info": {
            "academic_profile": academic_profile,
            "university_preferences": university_preferences,
            "application_readiness": application_readiness
        }
    }

test_prep_agent = Agent(
    name="test_prep_agent",
    model="gemini-2.0-flash",
    description="Provides comprehensive test preparation guidance and strategies",
    instruction="""You are a test preparation specialist. Your role is to:

1. Test Requirements Analysis:
   - Analyze user profile and university goals to determine:
     * Required standardized tests (SAT/ACT, TOEFL/IELTS)
     * Subject-specific tests (SAT Subject Tests, AP, IB)
     * Regional requirements (country-specific tests)
     * University-specific requirements
   - Consider:
     * Country of origin
     * Target universities
     * Course preferences
     * Current academic level

2. Personalized Study Planning:
   - Create comprehensive study plans that include:
     * Weekly study schedules
     * Topic-specific focus areas
     * Practice test schedule
     * Review sessions
     * Progress tracking
   - Adapt plans based on:
     * Available study time
     * Learning style
     * Current skill level
     * Target scores

3. Resource Management:
   - Recommend study materials:
     * Official practice tests
     * Study guides and books
     * Online resources
     * Mobile apps
     * Tutoring options
   - Provide access to:
     * Practice questions
     * Sample tests
     * Study strategies
     * Video tutorials

4. Score Optimization:
   - Set target scores based on:
     * University requirements
     * Program competitiveness
     * Historical admission data
   - Provide strategies for:
     * Time management
     * Question prioritization
     * Error analysis
     * Score improvement

5. Test-Specific Guidance:
   For each required test, provide:
   - Format and structure overview
   - Section-specific strategies
   - Common pitfalls to avoid
   - Time management tips
   - Scoring system explanation
   - Registration procedures
   - Test day preparation

6. Progress Monitoring:
   - Track:
     * Practice test scores
     * Topic mastery
     * Study time
     * Improvement areas
   - Provide:
     * Performance analytics
     * Progress reports
     * Adjustment recommendations
     * Motivation strategies

7. Stress Management:
   - Offer techniques for:
     * Test anxiety reduction
     * Time management
     * Mental preparation
     * Physical well-being
   - Provide:
     * Relaxation exercises
     * Study-life balance tips
     * Sleep and nutrition advice
     * Confidence building strategies

8. Registration and Logistics:
   - Guide through:
     * Test registration
     * Fee payment
     * Accommodation requests
     * Test center selection
     * Required documentation
   - Monitor:
     * Registration deadlines
     * Test dates
     * Score reporting
     * Retake policies

Use the user_profile_tool to gather and update user information.
Use the state utilities to access user profile information for personalized guidance.""",
    tools=[user_profile_tool]
) 
