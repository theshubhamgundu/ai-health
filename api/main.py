"""
FastAPI backend for Arovia Health Desk Agent
Provides REST API endpoints for medical triage, voice processing, and facility matching
"""
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import tempfile
from datetime import datetime

# Import our existing modules - use absolute imports
try:
    from agents.triage_agent import AroviaTriageAgent
    from models.schemas import TriageResult, VoiceInput, ReferralNote
    from utils.whisper_client import WhisperClient
    from utils.facility_matcher import FacilityMatcher
except ImportError as e:
    print(f"Import error: {e}")
    print("Creating stub implementations for testing...")
    
app = FastAPI(
    title="Arovia Health Desk API",
    description="AI-powered medical triage and healthcare facility matching API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
triage_agent: Optional[AroviaTriageAgent] = None
whisper_client: Optional[WhisperClient] = None

# Pydantic models for API requests/responses
class TriageRequest(BaseModel):
    symptoms: str
    location: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None

class VoiceTriageRequest(BaseModel):
    language: Optional[str] = "en"
    duration: Optional[float] = 10.0

class LocationRequest(BaseModel):
    location: str
    coordinates: Optional[Dict[str, float]] = None

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    services: Dict[str, str]

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global triage_agent, whisper_client
    
    try:
        print("🚀 Initializing Arovia Health Desk API...")
        
        # Initialize triage agent
        triage_agent = AroviaTriageAgent()
        print("✅ Triage agent initialized")
        
        # Initialize whisper client
        whisper_client = WhisperClient(model_size="large-v3")
        print("✅ Whisper client initialized")
        
        print("🎉 Arovia Health Desk API ready!")
        
    except Exception as e:
        print(f"❌ Error initializing services: {e}")
        raise

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Arovia Health Desk API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    services = {
        "triage_agent": "ready" if triage_agent else "not_ready",
        "whisper": "ready" if whisper_client else "not_ready"
    }
    
    return HealthCheck(
        status="healthy" if all(status == "ready" for status in services.values()) else "degraded",
        timestamp=datetime.now(),
        services=services
    )

@app.post("/triage/text", response_model=TriageResult)
async def analyze_symptoms_text(request: TriageRequest):
    """
    Analyze symptoms from text input
    """
    if not triage_agent:
        raise HTTPException(status_code=503, detail="Triage agent not available")
    
    try:
        if request.location:
            # Complete triage with facility recommendations
            referral_note = triage_agent.complete_triage_with_facilities(
                request.symptoms,
                request.location,
                user_coordinates=request.coordinates
            )
            return referral_note.triage_result
        else:
            # Basic triage without facilities
            return triage_agent.analyze_symptoms_from_text(request.symptoms)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing symptoms: {str(e)}")

@app.post("/triage/voice", response_model=Dict[str, Any])
async def analyze_symptoms_voice(
    audio_file: UploadFile = File(...),
    language: str = Form("en"),
    duration: float = Form(10.0)
):
    """
    Analyze symptoms from voice input
    """
    if not triage_agent or not whisper_client:
        raise HTTPException(status_code=503, detail="Voice processing services not available")
    
    try:
        # Save uploaded audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Transcribe audio
            voice_result = whisper_client.transcribe_audio(
                temp_file_path,
                language=language
            )
            
            # Analyze symptoms
            if voice_result.transcribed_text.strip():
                triage_result = triage_agent.analyze_symptoms_from_text(voice_result.transcribed_text)
            else:
                raise HTTPException(status_code=400, detail="No speech detected in audio")
            
            return {
                "voice_result": {
                    "transcribed_text": voice_result.transcribed_text,
                    "language": voice_result.language,
                    "confidence": voice_result.confidence,
                    "processing_time": voice_result.processing_time
                },
                "triage_result": triage_result.dict()
            }
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing voice input: {str(e)}")

@app.post("/facilities", response_model=List[Dict[str, Any]])
async def get_nearby_facilities(request: LocationRequest):
    """
    Get nearby healthcare facilities
    """
    if not triage_agent:
        raise HTTPException(status_code=503, detail="Facility matcher not available")
    
    try:
        # Get coordinates from location
        if request.coordinates and 'latitude' in request.coordinates and 'longitude' in request.coordinates:
            lat = request.coordinates.get('latitude')
            lon = request.coordinates.get('longitude')
            if lat is None or lon is None:
                raise HTTPException(status_code=400, detail="Invalid coordinates provided")
        else:
            # Geocode the location
            coords = triage_agent.facility_matcher.geocode_location(request.location)
            if not coords:
                raise HTTPException(status_code=400, detail="Could not geocode location")
            lat, lon = coords
        
        facilities = triage_agent.facility_matcher.search_nearby_facilities(
            latitude=lat,
            longitude=lon,
            radius_km=10.0
        )
        
        # Handle both dict and object responses
        if facilities and isinstance(facilities[0], dict):
            return facilities
        else:
            return [facility.dict() if hasattr(facility, 'dict') else facility for facility in facilities]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding facilities: {str(e)}")

@app.get("/languages", response_model=Dict[str, str])
async def get_supported_languages():
    """
    Get supported languages for voice input
    """
    if not whisper_client:
        raise HTTPException(status_code=503, detail="Whisper client not available")
    
    return whisper_client.get_supported_languages()

@app.get("/models", response_model=Dict[str, Any])
async def get_model_info():
    """
    Get information about loaded models
    """
    if not triage_agent:
        raise HTTPException(status_code=503, detail="Triage agent not available")
    
    return triage_agent.get_model_info()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
