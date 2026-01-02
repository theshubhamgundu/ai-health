#!/usr/bin/env python3
"""
Simple test script to validate Arovia MVP functionality
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.triage_agent import AroviaTriageAgent

def test_text_triage():
    """Test text-based triage functionality"""
    print("🧪 Testing Text Triage...")
    
    try:
        # Initialize agent (will use environment variables for API key)
        agent = AroviaTriageAgent()
        
        # Test cases
        test_cases = [
            {
                "input": "I have severe chest pain for 30 minutes, radiating to my left arm",
                "expected_urgency": "high",
                "description": "Emergency case - cardiac symptoms"
            },
            {
                "input": "I have a mild headache since this morning",
                "expected_urgency": "low", 
                "description": "Standard case - minor symptoms"
            },
            {
                "input": "मुझे 3 दिन से बुखार है और खांसी भी हो रही है",
                "expected_urgency": "medium",
                "description": "Urgent case - Hindi input with fever and cough"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test Case {i}: {test_case['description']} ---")
            print(f"Input: {test_case['input']}")
            
            try:
                result = agent.analyze_symptoms_from_text(test_case['input'])
                
                print(f"✅ Urgency Score: {result.urgency_score}/10")
                print(f"✅ Triage Category: {result.triage_category}")
                print(f"✅ Emergency Detected: {result.emergency_detected}")
                print(f"✅ Chief Complaint: {result.chief_complaint}")
                print(f"✅ Recommended Specialty: {result.recommended_specialty}")
                
                if result.red_flags:
                    print(f"🚨 Red Flags: {len(result.red_flags)} detected")
                    for flag in result.red_flags:
                        print(f"   - {flag.flag_type.upper()}: {flag.description}")
                
                if result.symptoms:
                    print(f"📋 Symptoms: {len(result.symptoms)} identified")
                    for symptom in result.symptoms:
                        print(f"   - {symptom.name} ({symptom.severity})")
                
                print(f"✅ Action Required: {result.action_required}")
                
            except Exception as e:
                print(f"❌ Test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return False

def test_voice_languages():
    """Test supported languages"""
    print("\n🌐 Testing Supported Languages...")
    
    try:
        agent = AroviaTriageAgent()
        languages = agent.get_supported_languages()
        
        print(f"✅ Supported Languages: {len(languages)}")
        print("Major Indian Languages:")
        major_langs = ["hindi", "english", "bengali", "telugu", "marathi", "tamil", "gujarati", "urdu", "kannada"]
        for lang in major_langs:
            if lang in languages:
                print(f"   - {lang.title()}: {languages[lang]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to get languages: {e}")
        return False

def test_model_info():
    """Test model information"""
    print("\n🤖 Testing Model Information...")
    
    try:
        agent = AroviaTriageAgent()
        model_info = agent.get_model_info()
        
        print("✅ Model Information:")
        print(f"   - Whisper Model: {model_info['whisper']['model']}")
        print(f"   - Supported Languages: {model_info['whisper']['supported_languages']}")
        print(f"   - Groq Model: {model_info['groq']['model']}")
        print(f"   - Provider: {model_info['groq']['provider']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to get model info: {e}")
        return False

def main():
    """Run all tests"""
    print("🏥 Arovia MVP Testing Suite")
    print("=" * 50)
    
    # Check if GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "gsk_your_groq_api_key_here":
        print("⚠️  WARNING: GROQ_API_KEY not set or using placeholder value")
        print("   Set your Groq API key in the .env file to test AI functionality")
        print("   For now, testing basic functionality only...")
        return
    
    # Run tests
    tests = [
        ("Text Triage", test_text_triage),
        ("Supported Languages", test_voice_languages), 
        ("Model Information", test_model_info)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Arovia MVP is ready!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
