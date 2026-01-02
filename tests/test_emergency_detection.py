"""
Test suite for Emergency Detection System
"""
import pytest
from agents.triage_agent import AroviaTriageAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TestEmergencyDetection:
    """Test cases for emergency detection functionality"""
    
    @pytest.fixture
    def agent(self):
        """Initialize triage agent for testing"""
        return AroviaTriageAgent()
    
    def test_cardiac_emergency(self, agent):
        """Test cardiac emergency detection"""
        test_cases = [
            "I have severe chest pain for 30 minutes",
            "Heart attack symptoms with crushing chest pressure",
            "Severe chest pain radiating to my left arm and jaw",
            "I think I'm having a heart attack"
        ]
        
        for case in test_cases:
            result = agent.analyze_symptoms_from_text(case)
            assert result.urgency_score >= 8
            assert result.emergency_detected is True
            assert result.triage_category == "immediate"
    
    def test_neurological_emergency(self, agent):
        """Test neurological emergency detection"""
        test_cases = [
            "I think I'm having a stroke, my face is drooping",
            "Sudden severe headache with loss of consciousness",
            "I can't move my left arm and my speech is slurred",
            "I had a seizure and lost consciousness"
        ]
        
        for case in test_cases:
            result = agent.analyze_symptoms_from_text(case)
            assert result.urgency_score >= 8
            assert result.emergency_detected is True
            assert result.triage_category == "immediate"
    
    def test_respiratory_emergency(self, agent):
        """Test respiratory emergency detection"""
        test_cases = [
            "I can't breathe and my lips are turning blue",
            "Severe shortness of breath, gasping for air",
            "I'm choking and can't get any air",
            "Respiratory distress with chest tightness"
        ]
        
        for case in test_cases:
            result = agent.analyze_symptoms_from_text(case)
            assert result.urgency_score >= 8
            assert result.emergency_detected is True
            assert result.triage_category == "immediate"
    
    def test_trauma_emergency(self, agent):
        """Test trauma emergency detection"""
        test_cases = [
            "Severe bleeding from a deep cut",
            "Head injury with loss of consciousness",
            "Broken bone visible through skin",
            "Major car accident with multiple injuries"
        ]
        
        for case in test_cases:
            result = agent.analyze_symptoms_from_text(case)
            assert result.urgency_score >= 8
            assert result.emergency_detected is True
            assert result.triage_category == "immediate"
    
    def test_mental_health_emergency(self, agent):
        """Test mental health emergency detection"""
        test_cases = [
            "I want to kill myself",
            "I'm having suicidal thoughts",
            "I want to harm myself",
            "I don't want to live anymore"
        ]
        
        for case in test_cases:
            result = agent.analyze_symptoms_from_text(case)
            assert result.urgency_score >= 8
            assert result.emergency_detected is True
            assert result.triage_category == "immediate"
    
    def test_non_emergency_cases(self, agent):
        """Test that non-emergency cases are not flagged as emergencies"""
        test_cases = [
            "I have a mild headache",
            "Small cut on my finger",
            "Mild fever for one day",
            "Slight cough and runny nose"
        ]
        
        for case in test_cases:
            result = agent.analyze_symptoms_from_text(case)
            assert result.urgency_score <= 6
            assert result.emergency_detected is False
            assert result.triage_category in ["standard", "urgent"]
