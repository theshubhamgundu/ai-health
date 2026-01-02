"""
Whisper-Large integration for speech-to-text with 22 Indic languages support
"""
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Whisper not available: {e}")
    WHISPER_AVAILABLE = False
    whisper = None

import sounddevice as sd
import numpy as np
import tempfile
import os
from typing import Optional, Dict, Any
from models.schemas import VoiceInput
import time


class WhisperClient:
    """Whisper-Large client for multilingual speech recognition"""
    
    # 22 Official Indic Languages supported by Whisper
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
    #def __init__(self, model_size: str = "small"):
    def __init__(self, model_size: str = "large-v3"):
        """
        Initialize Whisper client
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large, large-v2, large-v3)
        """
        self.model_size = model_size
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model"""
        if not WHISPER_AVAILABLE:
            print("Warning: Whisper is not available. Voice input will be disabled.")
            self.model = None
            return
            
        try:
            print(f"Loading Whisper {self.model_size} model...")
            self.model = whisper.load_model(self.model_size)
            print("Whisper model loaded successfully!")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            self.model = None
    
    def record_audio(self, duration: float = 10.0, sample_rate: int = 16000) -> str:
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Audio sample rate
            
        Returns:
            Path to recorded audio file
        """
        try:
            print(f"Recording for {duration} seconds...")
            print("Speak now...")
            
            # Record audio
            audio_data = sd.rec(
                int(duration * sample_rate), 
                samplerate=sample_rate, 
                channels=1, 
                dtype=np.float32
            )
            sd.wait()  # Wait until recording is finished
            
            print("Recording finished!")
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_file.close()
            
            # Convert to the format Whisper expects
            audio_np = audio_data.flatten()
            
            # Save as WAV file
            import soundfile as sf
            sf.write(temp_file.name, audio_np, sample_rate)
            
            return temp_file.name
            
        except Exception as e:
            print(f"Error recording audio: {e}")
            raise
    
    def transcribe_audio(
        self, 
        audio_file_path: str, 
        language: Optional[str] = None,
        initial_prompt: Optional[str] = None
    ) -> VoiceInput:
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (e.g., 'hi' for Hindi, 'en' for English)
            initial_prompt: Optional prompt to guide transcription
            
        Returns:
            VoiceInput object with transcription results
        """
        start_time = time.time()
        
        if not WHISPER_AVAILABLE or self.model is None:
            # Return a mock result when whisper is not available
            return VoiceInput(
                audio_file_path=audio_file_path,
                transcribed_text="[Voice input not available - Whisper not installed]",
                language=language or "en",
                confidence=0.0,
                processing_time=time.time() - start_time
            )
        
        try:
            if not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            # Transcribe with Whisper
            result = self.model.transcribe(
                audio_file_path,
                language=language,
                initial_prompt=initial_prompt,
                word_timestamps=True
            )
            
            processing_time = time.time() - start_time
            
            # Extract language from result
            detected_language = result.get("language", language or "unknown")
            
            # Get confidence from segments
            segments = result.get("segments", [])
            avg_confidence = 0.0
            if segments:
                confidences = [seg.get("avg_logprob", 0) for seg in segments]
                avg_confidence = np.mean(confidences) if confidences else 0.0
                # Convert log probability to confidence (0-1)
                avg_confidence = min(1.0, max(0.0, (avg_confidence + 1) / 2))
            
            return VoiceInput(
                audio_file_path=audio_file_path,
                transcribed_text=result["text"].strip(),
                language=detected_language,
                confidence=float(avg_confidence),
                processing_time=processing_time
            )
            
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            raise
    
    def get_language_name(self, language_code: str) -> str:
        """Get full language name from code"""
        for name, code in self.SUPPORTED_LANGUAGES.items():
            if code == language_code:
                return name.title()
        return language_code.upper()
    
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


# Convenience function for quick transcription
def transcribe_voice_input(
    language: Optional[str] = None,
    duration: float = 10.0,
    #model_size: str = "small",
    model_size: str = "large-v3"
) -> VoiceInput:
    """
    Quick function to record and transcribe voice input
    
    Args:
        language: Language code (e.g., 'hi', 'en')
        duration: Recording duration in seconds
        model_size: Whisper model size
        
    Returns:
        VoiceInput object
    """
    client = WhisperClient(model_size=model_size)
    
    # Record audio
    audio_file = client.record_audio(duration=duration)
    
    try:
        # Transcribe
        result = client.transcribe_audio(audio_file, language=language)
        return result
    finally:
        # Cleanup
        client.cleanup_audio_file(audio_file)


if __name__ == "__main__":
    # Test the Whisper client
    print("Testing Whisper client...")
    
    # Test with different languages
    languages_to_test = ["hi", "en", "te", "ta", "bn"]
    
    for lang in languages_to_test:
        print(f"\nTesting with language: {lang}")
        try:
            result = transcribe_voice_input(language=lang, duration=5.0)
            print(f"Transcribed: {result.transcribed_text}")
            print(f"Confidence: {result.confidence:.2f}")
            print(f"Processing time: {result.processing_time:.2f}s")
        except Exception as e:
            print(f"Error testing {lang}: {e}")
