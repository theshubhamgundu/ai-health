"""
Test script for Arovia triage system
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.triage_agent import AroviaTriageAgent
from models.schemas import TriageResult


def test_text_triage():
    """Test triage with text input"""
    print("=== Testing Text Triage ===")
    
    # Test cases
    test_cases = [
        {
            "input": "I have severe chest pain for 30 minutes, radiating to my left arm and I'm feeling short of breath",
            "expected_urgency": "high",
            "description": "Emergency cardiac case"
        },
        {
            "input": "मुझे 3 दिन से बुखार है और खांसी भी हो रही है। सांस लेने में थोड़ी तकलीफ हो रही है।",
            "expected_urgency": "medium", 
            "description": "Urgent respiratory case (Hindi)"
        },
        {
            "input": "I have a mild headache since this morning. No other symptoms.",
            "expected_urgency": "low",
            "description": "Standard case"
        },
        {
            "input": "I can't breathe properly and my lips are turning blue",
            "expected_urgency": "high",
            "description": "Emergency respiratory case"
        }
    ]
    
    try:
        # Initialize agent
        agent = AroviaTriageAgent()
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test Case {i}: {test_case['description']} ---")
            print(f"Input: {test_case['input']}")
            
            # Analyze symptoms
            result = agent.analyze_symptoms_from_text(test_case['input'])
            
            print(f"Chief Complaint: {result.chief_complaint}")
            print(f"Urgency Score: {result.urgency_score}/10")
            print(f"Emergency Detected: {result.emergency_detected}")
            print(f"Triage Category: {result.triage_category}")
            print(f"Recommended Specialty: {result.recommended_specialty}")
            print(f"Action Required: {result.action_required}")
            
            if result.red_flags:
                print("Red Flags:")
                for flag in result.red_flags:
                    print(f"  - {flag.flag_type.upper()}: {flag.description}")
            
            if result.potential_risks:
                print("Potential Risks:")
                for risk in result.potential_risks:
                    print(f"  - {risk.condition} ({risk.probability} probability)")
            
            print(f"Symptoms: {len(result.symptoms)} identified")
            for symptom in result.symptoms:
                print(f"  - {symptom.name} ({symptom.severity})")
            
            print("-" * 50)
            
    except Exception as e:
        print(f"Error in text triage test: {e}")


def test_voice_triage():
    """Test triage with voice input (interactive)"""
    print("\n=== Testing Voice Triage ===")
    print("This will record audio and transcribe it...")
    
    try:
        # Initialize agent
        agent = AroviaTriageAgent()
        
        # Show supported languages
        languages = agent.get_supported_languages()
        print(f"Supported languages: {list(languages.keys())[:10]}...")  # Show first 10
        
        # Test with English
        print("\nTesting with English (5 seconds recording)...")
        voice_result, triage_result = agent.process_voice_to_triage(
            language="en",
            duration=5.0
        )
        
        print(f"Transcribed: {voice_result.transcribed_text}")
        print(f"Language: {voice_result.language}")
        print(f"Confidence: {voice_result.confidence:.2f}")
        print(f"Processing Time: {voice_result.processing_time:.2f}s")
        print(f"Urgency Score: {triage_result.urgency_score}/10")
        print(f"Emergency Detected: {triage_result.emergency_detected}")
        
    except Exception as e:
        print(f"Error in voice triage test: {e}")


def test_model_info():
    """Test model information"""
    print("\n=== Model Information ===")
    
    try:
        agent = AroviaTriageAgent()
        model_info = agent.get_model_info()
        
        print("Whisper Model:")
        print(f"  Model: {model_info['whisper']['model']}")
        print(f"  Supported Languages: {model_info['whisper']['supported_languages']}")
        
        print("\nGroq Model:")
        for key, value in model_info['groq'].items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"Error getting model info: {e}")


def main():
    """Main test function"""
    print("🏥 Arovia Triage System Test")
    print("=" * 50)
    
    # Check if API key is available
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  GROQ_API_KEY not found in environment variables")
        print("Please set your Groq API key:")
        print("export GROQ_API_KEY=your_api_key_here")
        return
    
    # Test model info first
    test_model_info()
    
    # Test text triage
    test_text_triage()
    
    # Ask user if they want to test voice input
    print("\n" + "=" * 50)
    user_input = input("Do you want to test voice input? (y/n): ").lower().strip()
    
    if user_input == 'y':
        test_voice_triage()
    else:
        print("Skipping voice test.")
    
    print("\n✅ Test completed!")


if __name__ == "__main__":
    main()
