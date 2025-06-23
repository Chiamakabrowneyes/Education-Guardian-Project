"""
Location Tool

This module provides a tool for getting and managing user location information.
"""

from typing import Dict, Any, Optional, Union
from google.adk.tools import ToolContext
from ..utils.state_utils import update_interaction_history, update_state

def get_location(
    latitude: Union[float, None] = None,
    longitude: Union[float, None] = None,
    location_name: Union[str, None] = None,
    auto_detect: bool = True,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Get and store user location information.
    
    Args:
        latitude: Latitude coordinate (optional if auto_detect is True)
        longitude: Longitude coordinate (optional if auto_detect is True)
        location_name: Optional name/label for the location
        auto_detect: Whether to attempt automatic location detection
        tool_context: Context for accessing session state
        
    Returns:
        Dict containing the location information
    """
    try:
        # If auto_detect is True, attempt to get location from browser
        if auto_detect:
            # Update interaction history
            update_interaction_history(
                tool_context,
                "location_auto_detect_attempt",
                {"status": "pending"}
            )
            
            # This will be handled by the frontend JavaScript
            return {
                "result": {
                    "action": "auto_detect_location",
                    "message": "Attempting to detect location automatically"
                },
                "stats": {
                    "detection_method": "browser_geolocation",
                    "auto_detect": True
                },
                "additional_info": {
                    "requires_user_permission": True,
                    "data_format": "coordinates"
                }
            }
        
        # Manual location input
        if latitude is None or longitude is None:
            # Update interaction history
            update_interaction_history(
                tool_context,
                "location_input_error",
                {"error": "Missing coordinates"}
            )
            
            return {
                "result": {"error": "Latitude and longitude are required for manual location input"},
                "stats": {"success": False},
                "additional_info": {"error_type": "MissingCoordinates"}
            }
            
        # Create location object
        location = {
            "latitude": latitude,
            "longitude": longitude,
            "name": location_name,
            "detection_method": "manual_input",
            "timestamp": tool_context.state.get("current_time", "")
        }
        
        # Get current locations from state
        locations = tool_context.state.get("locations", [])
        
        # Add new location
        locations.append(location)
        
        # Update state using session service
        update_state(
            tool_context.session_service,
            tool_context.app_name,
            tool_context.user_id,
            tool_context.session_id,
            {
                "locations": locations,
                "user_info": {
                    **tool_context.state.get("user_info", {}),
                    "location": location
                }
            }
        )
        
        # Update interaction history
        update_interaction_history(
            tool_context,
            "location_set",
            {
                "latitude": latitude,
                "longitude": longitude,
                "location_name": location_name,
                "detection_method": "manual_input"
            }
        )
        
        return {
            "result": {
                "action": "set_location",
                "location": location,
                "message": f"Successfully recorded location: {location_name or 'Unnamed location'}"
            },
            "stats": {
                "has_name": bool(location_name),
                "total_locations": len(locations)
            },
            "additional_info": {
                "data_format": "coordinates",
                "detection_method": "manual_input"
            }
        }
    except Exception as e:
        # Update interaction history with error
        update_interaction_history(
            tool_context,
            "location_error",
            {"error": str(e)}
        )
        
        return {
            "result": {"error": f"Failed to process location: {str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)}
        }

# Export the tool
location_tool = get_location
