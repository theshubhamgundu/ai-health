"""
Test suite for Voice Input Functionality
"""
import pytest
from agents.triage_agent import AroviaTriageAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TestVoiceInput:
    """Test cases for voice input functionality"""
    
    @pytest.fixture
    def agent(self):
        """Initialize triage agent for testing"""
        return AroviaTriageAgent()
    
    def test_supported_languages(self, agent):
        """Test supported languages for voice input"""
        languages = agent.get_supported_languages()
        
        # Test major Indian languages
        expected_languages = [
            "hindi", "english", "bengali", "telugu", "marathi", 
            "tamil", "gujarati", "urdu", "kannada"
        ]
        
        for lang in expected_languages:
            assert lang in languages
            assert languages[lang] is not None
    
    def test_language_codes(self, agent):
        """Test language codes are valid"""
        languages = agent.get_supported_languages()
        
        # Test that language codes are 2-3 characters
        for lang_name, lang_code in languages.items():
            assert len(lang_code) >= 2
            assert len(lang_code) <= 3
            assert lang_code.isalpha()
    
    def test_whisper_client_initialization(self, agent):
        """Test Whisper client initialization"""
        whisper_client = agent.whisper_client
        
        assert whisper_client is not None
        assert whisper_client.model_size == "large-v3"
        assert len(whisper_client.SUPPORTED_LANGUAGES) >= 20
    
    def test_model_info(self, agent):
        """Test model information for voice processing"""
        model_info = agent.get_model_info()
        
        assert "whisper" in model_info
        assert model_info["whisper"]["model"] == "large-v3"
        assert model_info["whisper"]["supported_languages"] >= 20
    
    @pytest.mark.skip(reason="Requires actual audio recording - manual test only")
    def test_voice_recording(self, agent):
        """Test voice recording functionality (manual test)"""
        # This test requires actual audio recording
        # Should be run manually with real audio input
        pass
    
    @pytest.mark.skip(reason="Requires actual audio recording - manual test only")
    def test_voice_to_triage_pipeline(self, agent):
        """Test complete voice-to-triage pipeline (manual test)"""
        # This test requires actual audio recording
        # Should be run manually with real audio input
        pass
