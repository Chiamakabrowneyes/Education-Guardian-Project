from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/location")
async def receive_location(request: Request):
    """Receive location data from the browser's geolocation API."""
    try:
        location_data = await request.json()
        return {"status": "success", "message": "Location received successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    """Serve the main application page."""
    return {"message": "Education Guide API is running"} 