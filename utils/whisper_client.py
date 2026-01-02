"""
Whisper-Large integration via Groq Cloud for speech-to-text
"""
import os
import tempfile
from typing import Optional, Dict, Any
from models.schemas import VoiceInput
import time
from groq import Groq

class WhisperClient:
    """Groq-based Whisper client for multilingual speech recognition"""
    
    # 22 Official Indic Languages supported by Groq/Whisper
    SUPPORTED_LANGUAGES = {
        "hindi": "hi",
        "english": "en", 
        "bengali": "bn",
        "telugu": "te",
        "marathi": "mr",
        "tamil": "ta",
        "gujarati": "gu",
        "urdu": "ur",
        "kannada": "kn",
        "odia": "or",
        "malayalam": "ml",
        "punjabi": "pa",
        "assamese": "as",
        "nepali": "ne",
        "sanskrit": "sa",
        "konkani": "gom",
        "manipuri": "mni",
        "bodo": "brx",
        "dogri": "doi",
        "kashmiri": "ks",
        "maithili": "mai",
        "santali": "sat"
    }

    def __init__(self, model_size: str = "whisper-large-v3"):
        """
        Initialize Groq Whisper client
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model_name = "whisper-large-v3" # Groq uses this specific name
    
    def transcribe_audio(
        self, 
        audio_file_path: str, 
        language: Optional[str] = None,
        initial_prompt: Optional[str] = None
    ) -> VoiceInput:
        """
        Transcribe audio file using Groq Cloud
        """
        start_time = time.time()
        
        if not self.client:
            return VoiceInput(
                audio_file_path=audio_file_path,
                transcribed_text="[Error: GROQ_API_KEY not found]",
                language=language or "en",
                confidence=0.0,
                processing_time=time.time() - start_time
            )
        
        try:
            with open(audio_file_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(os.path.basename(audio_file_path), file.read()),
                    model=self.model_name,
                    prompt=initial_prompt,
                    response_format="json",
                    language=language
                )
            
            processing_time = time.time() - start_time
            
            return VoiceInput(
                audio_file_path=audio_file_path,
                transcribed_text=transcription.text.strip(),
                language=language or "unknown",
                confidence=1.0, # Groq doesn't provide per-word confidence in simple JSON format
                processing_time=processing_time
            )
            
        except Exception as e:
            print(f"Error transcribing audio with Groq: {e}")
            raise

    def get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported languages"""
        return self.SUPPORTED_LANGUAGES.copy()

    def cleanup_audio_file(self, audio_file_path: str):
        """Clean up temporary audio file"""
        try:
            if os.path.exists(audio_file_path):
                os.unlink(audio_file_path)
        except Exception as e:
            print(f"Warning: Could not delete audio file {audio_file_path}: {e}")

def transcribe_voice_input(
    language: Optional[str] = None,
    duration: float = 10.0,
    model_size: str = "whisper-large-v3"
) -> VoiceInput:
    """Mock for local recording since it won't work on Vercel"""
    raise NotImplementedError("Direct recording is not supported on Vercel. Please upload a file via the API.")
