"""
User Profile Tool

This tool manages user profile information for the education guide agent.
"""

from typing import Dict, Any, Optional, Union, List
from google.adk.tools import ToolContext
from ..utils.state_utils import update_interaction_history, update_state, get_session_state

def update_user_profile(
    tool_context: ToolContext,
    gpa: Optional[float] = None,
    gpa_scale: Optional[str] = None,
    academic_history: Optional[Dict[str, Any]] = None,
    university_preferences: Optional[Dict[str, Any]] = None,
    hobbies: Optional[List[str]] = None,
    country: Optional[str] = None,
    field_of_study: Optional[str] = None,
    financial_needs: Optional[Dict[str, Any]] = None,
    test_scores: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Update user profile information.
    
    Args:
        tool_context: The tool context containing session information
        gpa: User's GPA
        gpa_scale: Scale used for GPA (e.g., '4.0', '5.0', '100')
        academic_history: Dictionary containing academic history
        university_preferences: Dictionary containing university preferences
        hobbies: List of user's hobbies and interests
        country: User's country of origin
        field_of_study: User's intended field of study
        financial_needs: Dictionary containing financial information
        test_scores: Dictionary containing standardized test scores
        
    Returns:
        Dict containing the result of the profile update
    """
    if not tool_context:
        return {"error": "Tool context is required"}
    
    try:
        # Get current state
        state = get_session_state(tool_context)
        
        # Initialize user profile if not present
        if "user_profile" not in state:
            state["user_profile"] = {}
        
        # Update only provided fields
        if gpa is not None:
            state["user_profile"]["gpa"] = gpa
        if gpa_scale is not None:
            state["user_profile"]["gpa_scale"] = gpa_scale
        if academic_history is not None:
            state["user_profile"]["academic_history"] = academic_history
        if university_preferences is not None:
            state["user_profile"]["university_preferences"] = university_preferences
        if hobbies is not None:
            state["user_profile"]["hobbies"] = hobbies
        if country is not None:
            state["user_profile"]["country"] = country
        if field_of_study is not None:
            state["user_profile"]["field_of_study"] = field_of_study
        if financial_needs is not None:
            state["user_profile"]["financial_needs"] = financial_needs
        if test_scores is not None:
            state["user_profile"]["test_scores"] = test_scores
        
        # Update state
        update_state(tool_context, state)
        
        return {
            "result": "User profile updated successfully",
            "profile": state["user_profile"]
        }
        
    except Exception as e:
        return {
            "error": f"Failed to update user profile: {str(e)}",
            "details": {
                "gpa": gpa,
                "gpa_scale": gpa_scale,
                "academic_history": academic_history,
                "university_preferences": university_preferences,
                "hobbies": hobbies,
                "country": country,
                "field_of_study": field_of_study,
                "financial_needs": financial_needs,
                "test_scores": test_scores
            }
        }

# Export the tool function directly
user_profile_tool = update_user_profile 