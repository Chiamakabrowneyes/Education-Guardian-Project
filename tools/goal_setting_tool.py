"""
Goal Setting Tool

This tool helps establish and track goals for the college application process.
"""

from typing import Dict, Any, List, Optional
from google.adk.tools import ToolContext
from ..utils.state_utils import update_state, get_session_state
from datetime import datetime

def get_session_state(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Get the current session state.
    
    Args:
        tool_context: The tool context containing session information
        
    Returns:
        Dict containing the current session state
    """
    return tool_context.session.state

def set_goal(
    tool_context: ToolContext,
    goal_type: str,
    description: str,
    deadline: str,
    priority: str,
    preliminary_questions: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Set a new goal for the user.
    
    Args:
        tool_context: The tool context containing session information
        goal_type: Type of goal (e.g., 'academic', 'test_prep', 'essay', 'application')
        description: Detailed description of the goal
        deadline: Target completion date
        priority: Priority level ('high', 'medium', 'low')
        preliminary_questions: Optional responses to preliminary questions
        
    Returns:
        Dict containing the result of the goal setting operation
    """
    if not tool_context:
        return {"error": "Tool context is required"}
    
    try:
        # Get current state
        state = get_session_state(tool_context)
        
        # Initialize goals if not present
        if "goals" not in state:
            state["goals"] = []
        
        # Create new goal
        new_goal = {
            "type": goal_type,
            "description": description,
            "deadline": deadline,
            "priority": priority,
            "status": "pending",
            "milestones": [],
            "created_at": str(datetime.now())
        }
        
        # Add goal to state
        state["goals"].append(new_goal)
        
        # Update user profile with preliminary information if provided
        if preliminary_questions:
            if "user_profile" not in state:
                state["user_profile"] = {}
            
            # Update user profile sections
            for section, data in preliminary_questions.items():
                state["user_profile"][section] = data
        
        # Update state
        update_state(tool_context, state)
        
        return {
            "result": "Goal set successfully",
            "goal": new_goal,
            "stats": {
                "total_goals": len(state["goals"]),
                "goals_by_type": {
                    goal["type"]: len([g for g in state["goals"] if g["type"] == goal["type"]])
                    for goal in state["goals"]
                }
            }
        }
        
    except Exception as e:
        return {
            "error": f"Failed to set goal: {str(e)}",
            "details": {
                "goal_type": goal_type,
                "description": description,
                "deadline": deadline,
                "priority": priority
            }
        }

# Export the tool function directly
goal_setting_tool = set_goal 