"""
Web application for the Education Guide Agent.
"""

import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils.state_utils import initialize_state
from agent import root_agent

# Create FastAPI app
app = FastAPI(title="Education Guide Agent")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create session service
session_service = InMemorySessionService()

# Constants
APP_NAME = "education_guide"
USER_ID = "user"  # In a real app, this would come from user authentication

@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {"message": "Education Guide API is running"}

@app.post("/api/location")
async def receive_location(location_data: dict):
    """Endpoint to receive location data from the browser."""
    try:
        # Get or create session
        sessions = session_service.list_sessions(
            app_name=APP_NAME,
            user_id=USER_ID
        )
        
        if not sessions.sessions:
            # Create new session with initial state
            session_id = str(uuid.uuid4())
            initial_state = initialize_state()
            session = session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_id,
                state=initial_state
            )
        else:
            # Use existing session
            session = sessions.sessions[0]
            session_id = session.id
        
        # Update location in state
        locations = session.state.get("locations", [])
        locations.append(location_data)
        session.state["locations"] = locations
        
        # Update session
        session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
            state=session.state
        )
        
        return {"status": "success", "message": "Location data received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    await websocket.accept()
    
    try:
        # Get or create session
        sessions = session_service.list_sessions(
            app_name=APP_NAME,
            user_id=USER_ID
        )
        
        if not sessions.sessions:
            # Create new session with initial state
            session_id = str(uuid.uuid4())
            initial_state = initialize_state()
            session = session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_id,
                state=initial_state
            )
        else:
            # Use existing session
            session = sessions.sessions[0]
            session_id = session.id
        
        # Create runner
        runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=session_service
        )
        
        # Send welcome message
        await websocket.send_json({
            "type": "system",
            "message": "Welcome to the Education Guide! How can I help you today?"
        })
        
        while True:
            try:
                # Receive message
                data = await websocket.receive_text()
                
                # Run agent
                for event in runner.run(
                    user_id=USER_ID,
                    session_id=session_id,
                    new_message=data
                ):
                    if event.is_final_response():
                        if event.content and event.content.parts:
                            await websocket.send_json({
                                "type": "agent",
                                "message": event.content.parts[0].text
                            })
                
                # Send updated state
                session = session_service.get_session(
                    app_name=APP_NAME,
                    user_id=USER_ID,
                    session_id=session_id
                )
                await websocket.send_json({
                    "type": "state",
                    "state": session.state
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 