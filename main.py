"""
Main entry point for the Education Guide Agent.
"""

import uuid
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from .utils.state_utils import initialize_state
from .agent import root_agent

# Create session service
session_service = InMemorySessionService()

# Constants
APP_NAME = "Education-Guardian-Agent-Project"
USER_ID = "user" 
SESSION_ID = str(uuid.uuid4())

def main():
    # Initialize session with default state
    initial_state = initialize_state()
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state
    )
    
    print(f"Created new session: {SESSION_ID}")
    
    # Create runner with session service
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    # Start the agent
    print("\nEducation Guide Agent is ready!")
    print("Type 'quit' to exit")
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            break
            
        # Run the agent
        for event in runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=user_input
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    print(f"\nAgent: {event.content.parts[0].text}")
                    
        # Display current state after each interaction
        session = session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
        print("\nCurrent State:")
        for key, value in session.state.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main() 