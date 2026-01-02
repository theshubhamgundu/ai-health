"""
Main triage agent combining Whisper, Groq, and medical reasoning
"""
import os
import time
from typing import Optional, Dict, Any, List, Tuple
from dotenv import load_dotenv
from models.schemas import (TriageResult, VoiceInput, Symptom, RedFlag, 
                            PotentialRisk, FacilityInfo, ReferralNote)
from utils.whisper_client import WhisperClient
from utils.facility_matcher import FacilityMatcher
from agents.groq_client import GroqClient, MedicalTriageAgent, MedicalRelevanceAgent

# Load environment variables from .env file
load_dotenv()


class AroviaTriageAgent:
    """Main Arovia triage agent combining voice input, AI reasoning, and medical assessment"""
    
    #def __init__(self, groq_api_key: Optional[str] = None, whisper_model: str = "small"):
    def __init__(self, groq_api_key: Optional[str] = None, whisper_model: str = "large-v3"):
        """
        Initialize Arovia triage agent
        
        Args:
            groq_api_key: Groq API key
            whisper_model: Whisper model size
        """
        # Initialize components
        self.whisper_client = WhisperClient(model_size=whisper_model)
        self.groq_client = GroqClient(api_key=groq_api_key)
        self.medical_agent = MedicalTriageAgent(self.groq_client)
        self.relevance_agent = MedicalRelevanceAgent(self.groq_client)
        self.facility_matcher = FacilityMatcher()
        
        print("Arovia Triage Agent initialized successfully!")
    
    def process_voice_input(
        self, 
        language: Optional[str] = None,
        duration: float = 10.0,
        initial_prompt: Optional[str] = None
    ) -> VoiceInput:
        """
        Process voice input through Whisper
        
        Args:
            language: Language code (e.g., 'hi', 'en')
            duration: Recording duration in seconds
            initial_prompt: Optional prompt to guide transcription
            
        Returns:
            VoiceInput object with transcription results
        """
        try:
            # Record audio
            audio_file = self.whisper_client.record_audio(duration=duration)
            
            # Transcribe audio
            voice_result = self.whisper_client.transcribe_audio(
                audio_file, 
                language=language,
                initial_prompt=initial_prompt
            )
            
            # Cleanup audio file
            self.whisper_client.cleanup_audio_file(audio_file)
            
            return voice_result
            
        except Exception as e:
            print(f"Error processing voice input: {e}")
            raise
    
    def analyze_symptoms_from_text(self, text: str) -> TriageResult:
        """
        Analyze symptoms from text input using medical triage agent
        
        Args:
            text: Patient symptom description
            
        Returns:
            TriageResult with structured assessment
        """
        try:
            # Get AI analysis
            ai_result = self.medical_agent.analyze_symptoms(text)
            
            # Convert to structured TriageResult
            triage_result = self._convert_to_triage_result(ai_result, text)
            
            return triage_result, ai_result.get("processing_time", 0)
            
        except Exception as e:
            print(f"Error analyzing symptoms: {e}")
            # Return basic result with error
            return TriageResult(
                chief_complaint=text,
                symptoms=[],
                urgency_score=5,
                red_flags=[],
                potential_risks=[],
                recommended_specialty="General Medicine",
                triage_category="standard",
                emergency_detected=False,
                action_required="Consult a healthcare provider",
                timestamp=time.time(),
                error=str(e)
            ), 0
    
    def process_voice_to_triage(
        self,
        language: Optional[str] = None,
        duration: float = 10.0,
        initial_prompt: Optional[str] = None
    ) -> tuple[VoiceInput, TriageResult]:
        """
        Complete pipeline: Voice input -> Transcription -> Medical triage
        
        Args:
            language: Language code for transcription
            duration: Recording duration in seconds
            initial_prompt: Optional prompt for transcription
            
        Returns:
            Tuple of (VoiceInput, TriageResult)
        """
        try:
            # Process voice input
            voice_result = self.process_voice_input(
                language=language,
                duration=duration,
                initial_prompt=initial_prompt
            )
            
            # Guardrail: Check for medical relevance
            if not self._is_relevant(voice_result.transcribed_text):
                raise ValueError("Input does not appear to be medically relevant.")
            
            # Analyze symptoms
            triage_result, _ = self.analyze_symptoms_from_text(voice_result.transcribed_text)
            
            return voice_result, triage_result
            
        except Exception as e:
            print(f"Error in voice-to-triage pipeline: {e}")
            raise
    
    def _is_relevant(self, text: str) -> bool:
        """
        Check if the text is medically relevant using the relevance agent.
        
        Args:
            text: The text to analyze.
            
        Returns:
            True if the text is medically relevant, False otherwise.
        """
        try:
            relevance_result = self.relevance_agent.check_relevance(text)
            return relevance_result.get("is_relevant", True)
        except Exception as e:
            print(f"Error checking medical relevance: {e}")
            # Default to assuming relevance to avoid blocking valid cases
            return True

    def _convert_to_triage_result(self, ai_result: Dict[str, Any], original_text: str) -> TriageResult:
        """
        Convert AI analysis result to structured TriageResult
        
        Args:
            ai_result: Raw AI analysis result
            original_text: Original patient input
            
        Returns:
            Structured TriageResult
        """
        try:
            # Extract symptoms
            symptoms: List[Symptom] = []
            if "symptoms" in ai_result:
                for symptom_data in ai_result["symptoms"]:
                    symptom = Symptom(
                        name=symptom_data.get("name", ""),
                        severity=symptom_data.get("severity", "mild"),
                        duration=symptom_data.get("duration"),
                        associated_symptoms=symptom_data.get("associated_symptoms", [])
                    )
                    symptoms.append(symptom)
            
            # Extract red flags
            red_flags: List[RedFlag] = []
            if "red_flags" in ai_result:
                for flag_data in ai_result["red_flags"]:
                    red_flag = RedFlag(
                        flag_type=flag_data.get("flag_type", "other"),
                        description=flag_data.get("description", ""),
                        urgency_level=flag_data.get("urgency_level", "urgent"),
                        action_required=flag_data.get("action_required", "")
                    )
                    red_flags.append(red_flag)
            
            # Extract potential risks
            potential_risks: List[PotentialRisk] = []
            if "potential_risks" in ai_result:
                for risk_data in ai_result["potential_risks"]:
                    risk = PotentialRisk(
                        condition=risk_data.get("condition", ""),
                        probability=risk_data.get("probability", "low"),
                        specialty_needed=risk_data.get("specialty_needed", "")
                    )
                    potential_risks.append(risk)
            
            # Determine triage category based on urgency score
            urgency_score = ai_result.get("urgency_score", 5)
            if urgency_score >= 9:
                triage_category = "immediate"
            elif urgency_score >= 7:
                triage_category = "urgent"
            else:
                triage_category = "standard"
            
            return TriageResult(
                chief_complaint=ai_result.get("chief_complaint", original_text),
                symptoms=symptoms,
                urgency_score=urgency_score,
                red_flags=red_flags,
                potential_risks=potential_risks,
                recommended_specialty=ai_result.get("recommended_specialty", "General Medicine"),
                triage_category=triage_category,
                emergency_detected=ai_result.get("emergency_detected", False),
                action_required=ai_result.get("action_required", "Consult a healthcare provider"),
                error=ai_result.get("error")
            )
            
        except Exception as e:
            print(f"Error converting AI result: {e}")
            # Return basic result
            return TriageResult(
                chief_complaint=original_text,
                symptoms=[],
                urgency_score=5,
                red_flags=[],
                potential_risks=[],
                recommended_specialty="General Medicine",
                triage_category="standard",
                emergency_detected=False,
                action_required="Consult a healthcare provider",
                error=f"Error parsing AI response: {e}"
            )
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get supported languages for voice input"""
        return self.whisper_client.get_supported_languages()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the AI models being used"""
        return {
            "whisper": {
                "model": self.whisper_client.model_size,
                "supported_languages": len(self.whisper_client.SUPPORTED_LANGUAGES)
            },
            "groq": self.groq_client.get_model_info()
        }
    
    def find_recommended_facilities(
        self,
        triage_result: TriageResult,
        user_location: str,
        radius_km: float = 10.0,
        user_coordinates: Optional[Tuple[float, float]] = None
    ) -> List[FacilityInfo]:
        """
        Find recommended facilities based on triage result
        
        Args:
            triage_result: Triage assessment result
            user_location: User's location
            radius_km: Search radius in kilometers
            user_coordinates: Optional user coordinates (lat, lon)
            
        Returns:
            List of recommended facilities
        """
        try:
            # Determine specialty from triage result
            specialty = triage_result.recommended_specialty.lower()
            
            # Adjust search radius based on urgency
            if triage_result.urgency_score >= 8:
                radius_km = min(radius_km, 5.0)  # Closer facilities for emergencies
            elif triage_result.urgency_score >= 6:
                radius_km = min(radius_km, 8.0)  # Moderate distance for urgent cases
            
            # Find facilities using coordinates if available
            if user_coordinates:
                lat, lon = user_coordinates
                facilities_data = self.facility_matcher.search_nearby_facilities(
                    lat, lon, radius_km, specialty
                )
            else:
                # Fallback to location string
                facilities_data = self.facility_matcher.find_facilities_for_condition(
                    user_location, specialty, radius_km
                )
            
            # Convert to FacilityInfo objects
            facilities = []
            for facility_data in facilities_data:
                # Handle both dict and FacilityInfo objects
                if isinstance(facility_data, dict):
                    facility = FacilityInfo(
                        name=facility_data["name"],
                        address=facility_data["address"],
                        distance_km=facility_data["distance_km"],
                        specialty=facility_data["specialty_match"],
                        services=facility_data["services"],
                        contact=facility_data.get("contact"),
                        map_link=facility_data["map_link"]
                    )
                else:
                    # Already a FacilityInfo object
                    facility = facility_data
                facilities.append(facility)
            
            # Sort by distance and filter by urgency
            facilities.sort(key=lambda x: x.distance_km)
            
            # For emergencies, prioritize emergency facilities
            if triage_result.emergency_detected:
                emergency_facilities = [
                    f for f in facilities 
                    if "emergency" in f.services or "trauma" in f.services
                ]
                if emergency_facilities:
                    return emergency_facilities[:3]
            
            return facilities[:5]  # Return top 5 facilities
            
        except Exception as e:
            print(f"Error finding facilities: {e}")
            return []
    
    def generate_referral_note(
        self,
        triage_result: TriageResult,
        user_location: str,
        patient_id: Optional[str] = None,
        user_coordinates: Optional[Tuple[float, float]] = None
    ) -> ReferralNote:
        """
        Generate complete referral note with facility recommendations
        
        Args:
            triage_result: Triage assessment result
            user_location: User's location
            patient_id: Optional patient identifier
            user_coordinates: Optional user coordinates (lat, lon)
            
        Returns:
            Complete referral note
        """
        try:
            # Find recommended facilities
            recommended_facilities = self.find_recommended_facilities(
                triage_result, user_location, user_coordinates=user_coordinates
            )
            
            # Create referral note
            referral_note = ReferralNote(
                patient_id=patient_id,
                triage_result=triage_result,
                recommended_facilities=recommended_facilities
            )
            
            return referral_note
            
        except Exception as e:
            print(f"Error generating referral note: {e}")
            # Return basic referral note
            return ReferralNote(
                patient_id=patient_id,
                triage_result=triage_result,
                recommended_facilities=[]
            )
    
    def complete_triage_with_facilities(
        self,
        text: str,
        user_location: str,
        patient_id: Optional[str] = None,
        user_coordinates: Optional[Tuple[float, float]] = None
    ) -> ReferralNote:
        """
        Complete triage pipeline with facility recommendations
        
        Args:
            text: Patient symptom description
            user_location: User's location
            patient_id: Optional patient identifier
            user_coordinates: Optional user coordinates (lat, lon)
            
        Returns:
            Complete referral note with facility recommendations
        """
        try:
            # Analyze symptoms
            triage_result, _ = self.analyze_symptoms_from_text(text)
            
            # Generate referral note with facilities
            referral_note = self.generate_referral_note(
                triage_result, user_location, patient_id, user_coordinates
            )
            
            return referral_note
            
        except Exception as e:
            print(f"Error in complete triage: {e}")
            raise


# Convenience function for quick triage
def quick_voice_triage(
    language: Optional[str] = None,
    duration: float = 10.0,
    groq_api_key: Optional[str] = None
) -> tuple[VoiceInput, TriageResult]:
    """
    Quick function to perform voice-to-triage pipeline
    
    Args:
        language: Language code for transcription
        duration: Recording duration in seconds
        groq_api_key: Groq API key
        
    Returns:
        Tuple of (VoiceInput, TriageResult)
    """
    try:
        # Initialize agent
        agent = AroviaTriageAgent(groq_api_key=groq_api_key)
        
        # Process voice to triage
        voice_result, triage_result = agent.process_voice_to_triage(
            language=language,
            duration=duration
        )
        
        return voice_result, triage_result
        
    except Exception as e:
        print(f"Error in quick voice triage: {e}")
        raise


if __name__ == "__main__":
    # Test the complete triage agent
    print("Testing Arovia Triage Agent...")
    
    # Test with different languages
    test_languages = ["hi", "en", "te", "ta"]
    
    for lang in test_languages:
        print(f"\n--- Testing with language: {lang} ---")
        try:
            voice_result, triage_result = quick_voice_triage(
                language=lang,
                duration=5.0
            )
            
            print(f"Transcribed: {voice_result.transcribed_text}")
            print(f"Language: {voice_result.language}")
            print(f"Confidence: {voice_result.confidence:.2f}")
            print(f"Urgency Score: {triage_result.urgency_score}")
            print(f"Emergency Detected: {triage_result.emergency_detected}")
            print(f"Triage Category: {triage_result.triage_category}")

        except Exception as e:
            print(f"Test failed for {lang}: {e}")
