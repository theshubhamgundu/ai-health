"""
Test suite for Arovia Triage Agent
"""
import pytest
import os
from dotenv import load_dotenv
from agents.triage_agent import AroviaTriageAgent
from models.schemas import TriageResult

# Load environment variables
load_dotenv()

class TestTriageAgent:
    """Test cases for Arovia Triage Agent"""
    
    @pytest.fixture
    def agent(self):
        """Initialize triage agent for testing"""
        return AroviaTriageAgent()
    
    def test_agent_initialization(self, agent):
        """Test agent initialization"""
        assert agent is not None
        assert agent.whisper_client is not None
        assert agent.groq_client is not None
        assert agent.medical_agent is not None
    
    def test_emergency_detection(self, agent):
        """Test emergency case detection"""
        result = agent.analyze_symptoms_from_text(
            "I have severe chest pain for 30 minutes, radiating to my left arm"
        )
        
        assert result.urgency_score >= 8
        assert result.emergency_detected is True
        assert result.triage_category == "immediate"
        assert len(result.red_flags) > 0
    
    def test_standard_case(self, agent):
        """Test standard case assessment"""
        result = agent.analyze_symptoms_from_text(
            "I have a mild headache since this morning"
        )
        
        assert result.urgency_score <= 5
        assert result.emergency_detected is False
        assert result.triage_category in ["standard", "urgent"]
    
    def test_multilingual_support(self, agent):
        """Test multilingual input support"""
        # Test Hindi input
        result = agent.analyze_symptoms_from_text(
            "मुझे 3 दिन से बुखार है और खांसी भी हो रही है"
        )
        
        assert result.chief_complaint is not None
        assert result.urgency_score > 0
        assert result.recommended_specialty is not None
    
    def test_supported_languages(self, agent):
        """Test supported languages"""
        languages = agent.get_supported_languages()
        
        assert len(languages) >= 20  # Should support 22+ languages
        assert "hindi" in languages
        assert "english" in languages
        assert "bengali" in languages
        assert "telugu" in languages
    
    def test_model_info(self, agent):
        """Test model information retrieval"""
        model_info = agent.get_model_info()
        
        assert "whisper" in model_info
        assert "groq" in model_info
        assert model_info["whisper"]["model"] == "large-v3"
        assert "llama" in model_info["groq"]["model"].lower()
