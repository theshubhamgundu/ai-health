#!/usr/bin/env python3
"""
Demo script to test voice input functionality
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from agents.triage_agent import AroviaTriageAgent

# Load environment variables
load_dotenv()

def demo_voice_triage():
    """Demo voice triage functionality"""
    print("🎤 Arovia Voice Triage Demo")
    print("=" * 40)
    
    try:
        # Initialize agent
        print("Initializing Arovia Agent...")
        agent = AroviaTriageAgent()
        print("✅ Agent initialized successfully!")
        
        # Get supported languages
        languages = agent.get_supported_languages()
        print(f"\n🌐 Supported Languages: {len(languages)}")
        print("Major Indian Languages:")
        major_langs = ["hindi", "english", "bengali", "telugu", "marathi", "tamil", "gujarati", "urdu", "kannada"]
        for lang in major_langs:
            if lang in languages:
                print(f"   - {lang.title()}: {languages[lang]}")
        
        print(f"\n🎤 Voice Input Demo")
        print("This will record audio for 5 seconds and analyze it...")
        print("Press Enter to start recording...")
        input()
        
        # Test voice input (5 seconds)
        print("🎤 Recording for 5 seconds... Speak now!")
        voice_result, triage_result = agent.process_voice_to_triage(
            language="en",  # English
            duration=5.0
        )
        
        print(f"\n📝 Transcription Results:")
        print(f"   - Text: {voice_result.transcribed_text}")
        print(f"   - Language: {voice_result.language}")
        print(f"   - Confidence: {voice_result.confidence:.2f}")
        print(f"   - Processing Time: {voice_result.processing_time:.2f}s")
        
        print(f"\n🏥 Medical Assessment:")
        print(f"   - Urgency Score: {triage_result.urgency_score}/10")
        print(f"   - Triage Category: {triage_result.triage_category}")
        print(f"   - Emergency Detected: {triage_result.emergency_detected}")
        print(f"   - Chief Complaint: {triage_result.chief_complaint}")
        print(f"   - Recommended Specialty: {triage_result.recommended_specialty}")
        
        if triage_result.red_flags:
            print(f"\n🚨 Red Flags Detected:")
            for flag in triage_result.red_flags:
                print(f"   - {flag.flag_type.upper()}: {flag.description}")
        
        if triage_result.symptoms:
            print(f"\n📋 Symptoms Identified:")
            for symptom in triage_result.symptoms:
                print(f"   - {symptom.name} ({symptom.severity})")
        
        print(f"\n✅ Action Required: {triage_result.action_required}")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "gsk_your_groq_api_key_here":
        print("⚠️  WARNING: GROQ_API_KEY not set!")
        print("   Set your Groq API key in the .env file to test AI functionality")
        return
    
    demo_voice_triage()
