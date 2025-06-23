"""
State Management Utilities

This module provides utility functions for managing session state.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from google.adk.tools import ToolContext

def initialize_state() -> Dict[str, Any]:
    """Initialize the session state with default values."""
    return {
        "user_info": {
            "name": None,
            "grade_level": None,
            "location": None
        },
        "goals": [],
        "progress": {
            "test_prep": {},
            "essays": {},
            "extracurriculars": {},
            "recommendation_letters": {}
        },
        "interaction_history": [],
        "university_preferences": [],
        "session_data": {
            "user_profile": {
                "background": {},
                "academic": {},
                "university_preferences": {},
                "financial_constraints": {},
                "application_readiness": {},
                "extracurriculars": {},
                "aspirations": {}
            }
        }
    }

def update_state(
    session_service,
    app_name: str,
    user_id: str,
    session_id: str,
    updates: Dict[str, Any]
) -> None:
    """Update specific fields in the session state."""
    try:
        # Get current session
        session = session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )

        # Create updated state
        updated_state = session.state.copy()
        
        # Update the state with new values
        for key, value in updates.items():
            if isinstance(value, dict) and key in updated_state:
                updated_state[key].update(value)
            else:
                updated_state[key] = value

        # Create a new session with updated state
        session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=updated_state
        )
    except Exception as e:
        print(f"Error updating state: {e}")
        # Fallback to local state management
        return updates

def add_to_interaction_history(
    session_service,
    app_name: str,
    user_id: str,
    session_id: str,
    entry: Dict[str, Any]
) -> None:
    """Add an entry to the interaction history."""
    try:
        # Get current session
        session = session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )

        # Get current interaction history
        interaction_history = session.state.get("interaction_history", [])

        # Add timestamp if not present
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add the entry
        interaction_history.append(entry)

        # Update state
        update_state(
            session_service,
            app_name,
            user_id,
            session_id,
            {"interaction_history": interaction_history}
        )
    except Exception as e:
        print(f"Error adding to interaction history: {e}")
        # Fallback to local state management
        return {"interaction_history": [entry]}

def display_state(
    session_service,
    app_name: str,
    user_id: str,
    session_id: str,
    label: str = "Current State"
) -> None:
    """Display the current session state in a formatted way."""
    try:
        session = session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )

        print(f"\n{'-' * 10} {label} {'-' * 10}")

        # Display user info
        user_info = session.state.get("user_info", {})
        print("👤 User Information:")
        for key, value in user_info.items():
            if value:
                print(f"  {key}: {value}")

        # Display goals
        goals = session.state.get("goals", [])
        if goals:
            print("\n🎯 Goals:")
            for idx, goal in enumerate(goals, 1):
                print(f"  {idx}. {goal}")

        # Display progress
        progress = session.state.get("progress", {})
        if any(progress.values()):
            print("\n📊 Progress:")
            for category, data in progress.items():
                if data:
                    print(f"  {category}:")
                    for key, value in data.items():
                        print(f"    - {key}: {value}")

        # Display university preferences
        universities = session.state.get("university_preferences", [])
        if universities:
            print("\n🏫 University Preferences:")
            for idx, uni in enumerate(universities, 1):
                print(f"  {idx}. {uni}")

        print("-" * (22 + len(label)))
    except Exception as e:
        print(f"Error displaying state: {e}")

def update_interaction_history(
    context: Union[ToolContext, Dict[str, Any]],
    action: str,
    data: Dict[str, Any]
) -> None:
    """
    Update the interaction history in the context.
    
    Args:
        context: The tool context or context dictionary
        action: The action performed
        data: The data associated with the action
    """
    try:
        session_state = get_session_state(context)
        history = session_state.get("interaction_history", [])
        history.append({
            "action": action,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        if isinstance(context, ToolContext):
            context.state["session_data"] = session_state
        else:
            context["session_data"] = session_state
    except Exception as e:
        print(f"Error updating interaction history: {e}")
        # Fallback to local state management
        if isinstance(context, dict):
            context["session_data"] = {
                "interaction_history": [{
                    "action": action,
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }]
            }

def get_session_state(context: Union[ToolContext, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get the session state from the context.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        Dict containing session state
    """
    try:
        if isinstance(context, ToolContext):
            return context.state.get("session_data", {})
        return context.get("session_data", {})
    except Exception as e:
        print(f"Error getting session state: {e}")
        return {}

def get_user_profile(context: Union[ToolContext, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get the user profile from the context.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        Dict containing user profile
    """
    try:
        session_state = get_session_state(context)
        return session_state.get("user_profile", {})
    except Exception as e:
        print(f"Error getting user profile: {e}")
        return {}

def get_user_background(context: Union[ToolContext, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get the user background from the context.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        Dict containing user background
    """
    try:
        profile = get_user_profile(context)
        return profile.get("background", {})
    except Exception as e:
        print(f"Error getting user background: {e}")
        return {}

def get_academic_profile(context: Union[ToolContext, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get the academic profile from the context.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        Dict containing academic profile
    """
    try:
        profile = get_user_profile(context)
        return profile.get("academic", {})
    except Exception as e:
        print(f"Error getting academic profile: {e}")
        return {}

def get_university_preferences(context: Union[ToolContext, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get the university preferences from the context.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        Dict containing university preferences
    """
    try:
        profile = get_user_profile(context)
        return profile.get("university_preferences", {})
    except Exception as e:
        print(f"Error getting university preferences: {e}")
        return {}

def get_financial_constraints(context: Union[ToolContext, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get the financial constraints from the context.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        Dict containing financial constraints
    """
    try:
        profile = get_user_profile(context)
        return profile.get("financial_constraints", {})
    except Exception as e:
        print(f"Error getting financial constraints: {e}")
        return {}

def get_application_readiness(context: Union[ToolContext, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get the application readiness from the context.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        Dict containing application readiness
    """
    try:
        profile = get_user_profile(context)
        return profile.get("application_readiness", {})
    except Exception as e:
        print(f"Error getting application readiness: {e}")
        return {}

def get_extracurriculars(context: Union[ToolContext, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get the extracurricular activities from the context.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        Dict containing extracurricular activities
    """
    try:
        profile = get_user_profile(context)
        return profile.get("extracurriculars", {})
    except Exception as e:
        print(f"Error getting extracurriculars: {e}")
        return {}

def get_aspirations(context: Union[ToolContext, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get the aspirations from the context.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        Dict containing aspirations
    """
    try:
        profile = get_user_profile(context)
        return profile.get("aspirations", {})
    except Exception as e:
        print(f"Error getting aspirations: {e}")
        return {}

def get_user_info(context: Union[ToolContext, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get user information from state.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        Dictionary containing user information
    """
    try:
        if isinstance(context, ToolContext):
            return context.state.get("user_info", {})
        return context.get("user_info", {})
    except Exception as e:
        print(f"Error getting user info: {e}")
        return {}

def update_user_info(
    context: Union[ToolContext, Dict[str, Any]],
    updates: Dict[str, Any]
) -> None:
    """
    Update user information in state.
    
    Args:
        context: The tool context or context dictionary
        updates: Dictionary of user information to update
    """
    try:
        # Get current user info
        user_info = get_user_info(context)
        
        # Update with new information
        user_info.update(updates)
        
        # Update state
        if isinstance(context, ToolContext):
            context.state["user_info"] = user_info
        else:
            context["user_info"] = user_info
        
    except Exception as e:
        print(f"Error updating user info: {e}")
        # Fallback to local state management
        if isinstance(context, dict):
            context["user_info"] = updates

def get_goals(context: Union[ToolContext, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get all goals from state.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        List of goal dictionaries
    """
    try:
        if isinstance(context, ToolContext):
            return context.state.get("goals", [])
        return context.get("goals", [])
    except Exception as e:
        print(f"Error getting goals: {e}")
        return []

def get_locations(context: Union[ToolContext, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get all locations from state.
    
    Args:
        context: The tool context or context dictionary
        
    Returns:
        List of location dictionaries
    """
    try:
        if isinstance(context, ToolContext):
            return context.state.get("locations", [])
        return context.get("locations", [])
    except Exception as e:
        print(f"Error getting locations: {e}")
        return [] 