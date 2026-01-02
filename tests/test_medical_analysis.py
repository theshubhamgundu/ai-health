"""
Test suite for Medical Analysis and Triage Logic
"""
import pytest
from agents.triage_agent import AroviaTriageAgent
from models.schemas import TriageResult, Symptom, RedFlag, PotentialRisk
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TestMedicalAnalysis:
    """Test cases for medical analysis functionality"""
    
    @pytest.fixture
    def agent(self):
        """Initialize triage agent for testing"""
        return AroviaTriageAgent()
    
    def test_urgency_scoring(self, agent):
        """Test urgency scoring system"""
        # Test emergency case
        emergency_result = agent.analyze_symptoms_from_text(
            "Severe chest pain for 30 minutes, radiating to left arm"
        )
        assert emergency_result.urgency_score >= 8
        
        # Test urgent case
        urgent_result = agent.analyze_symptoms_from_text(
            "High fever for 3 days with severe headache"
        )
        assert 5 <= urgent_result.urgency_score <= 8
        
        # Test standard case
        standard_result = agent.analyze_symptoms_from_text(
            "Mild headache since this morning"
        )
        assert standard_result.urgency_score <= 5
    
    def test_symptom_extraction(self, agent):
        """Test symptom extraction and categorization"""
        result = agent.analyze_symptoms_from_text(
            "I have severe chest pain for 30 minutes with shortness of breath"
        )
        
        assert len(result.symptoms) > 0
        assert any("chest pain" in symptom.name.lower() for symptom in result.symptoms)
        assert any("breath" in symptom.name.lower() for symptom in result.symptoms)
    
    def test_red_flag_detection(self, agent):
        """Test red flag detection system"""
        result = agent.analyze_symptoms_from_text(
            "Severe chest pain radiating to left arm and jaw"
        )
        
        assert len(result.red_flags) > 0
        assert any(flag.flag_type == "cardiac" for flag in result.red_flags)
        assert any(flag.urgency_level == "immediate" for flag in result.red_flags)
    
    def test_specialty_recommendation(self, agent):
        """Test medical specialty recommendations"""
        # Cardiac case
        cardiac_result = agent.analyze_symptoms_from_text(
            "Chest pain and palpitations"
        )
        assert "cardio" in cardiac_result.recommended_specialty.lower()
        
        # Neurological case
        neuro_result = agent.analyze_symptoms_from_text(
            "Severe headache with vision problems"
        )
        assert "neuro" in neuro_result.recommended_specialty.lower()
    
    def test_triage_categorization(self, agent):
        """Test triage category assignment"""
        # Immediate case
        immediate_result = agent.analyze_symptoms_from_text(
            "Severe chest pain with difficulty breathing"
        )
        assert immediate_result.triage_category == "immediate"
        
        # Urgent case
        urgent_result = agent.analyze_symptoms_from_text(
            "High fever for 2 days with body aches"
        )
        assert urgent_result.triage_category in ["urgent", "immediate"]
        
        # Standard case
        standard_result = agent.analyze_symptoms_from_text(
            "Mild cough and runny nose"
        )
        assert standard_result.triage_category == "standard"
    
    def test_action_recommendations(self, agent):
        """Test action recommendations"""
        # Emergency case
        emergency_result = agent.analyze_symptoms_from_text(
            "Severe chest pain and shortness of breath"
        )
        assert "emergency" in emergency_result.action_required.lower()
        assert "immediate" in emergency_result.action_required.lower()
        
        # Standard case
        standard_result = agent.analyze_symptoms_from_text(
            "Mild headache"
        )
        assert "consult" in standard_result.action_required.lower()
    
    def test_multilingual_medical_analysis(self, agent):
        """Test medical analysis with different languages"""
        # Hindi input
        hindi_result = agent.analyze_symptoms_from_text(
            "मुझे तेज सिरदर्द है और बुखार भी है"
        )
        assert hindi_result.urgency_score > 0
        assert hindi_result.chief_complaint is not None
        
        # Bengali input
        bengali_result = agent.analyze_symptoms_from_text(
            "আমার বুকে ব্যথা হচ্ছে"
        )
        assert bengali_result.urgency_score > 0
        assert bengali_result.chief_complaint is not None
