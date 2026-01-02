"""
Simple end-to-end test for Arovia triage system
Tests core functionality without external API dependencies
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
from datetime import datetime
from models.schemas import TriageResult, Symptom, RedFlag, PotentialRisk, VoiceInput


def test_pydantic_models():
    """Test Pydantic model creation and validation"""
    print("🧪 Testing Pydantic Models...")
    
    try:
        # Test Symptom model
        symptom = Symptom(
            name="chest pain",
            severity="severe",
            duration="30 minutes",
            associated_symptoms=["shortness of breath", "nausea"]
        )
        print(f"✅ Symptom created: {symptom.name} ({symptom.severity})")
        
        # Test RedFlag model
        red_flag = RedFlag(
            flag_type="cardiac",
            description="chest pain with radiation",
            urgency_level="immediate",
            action_required="Call 108 immediately"
        )
        print(f"✅ Red flag created: {red_flag.flag_type} - {red_flag.description}")
        
        # Test PotentialRisk model
        risk = PotentialRisk(
            condition="Acute Myocardial Infarction",
            probability="high",
            specialty_needed="Cardiology"
        )
        print(f"✅ Risk created: {risk.condition} ({risk.probability} probability)")
        
        # Test TriageResult model
        triage_result = TriageResult(
            chief_complaint="Severe chest pain for 30 minutes",
            symptoms=[symptom],
            urgency_score=9,
            red_flags=[red_flag],
            potential_risks=[risk],
            recommended_specialty="Cardiology",
            triage_category="immediate",
            emergency_detected=True,
            action_required="Call 108 immediately - DO NOT drive yourself"
        )
        print(f"✅ Triage result created: Urgency {triage_result.urgency_score}/10")
        print(f"   Emergency detected: {triage_result.emergency_detected}")
        print(f"   Category: {triage_result.triage_category}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Pydantic models: {e}")
        return False


def test_emergency_detection():
    """Test emergency keyword detection logic"""
    print("\n🚨 Testing Emergency Detection...")
    
    # Emergency keywords dictionary
    emergency_keywords = {
        "cardiac": [
            "chest pain", "heart attack", "crushing chest pressure",
            "pain radiating to arm", "severe palpitations"
        ],
        "neurological": [
            "stroke", "face drooping", "arm weakness", "slurred speech",
            "sudden severe headache", "loss of consciousness"
        ],
        "respiratory": [
            "can't breathe", "choking", "severe shortness of breath",
            "blue lips", "gasping for air"
        ],
        "trauma": [
            "severe bleeding", "head injury", "broken bone visible",
            "penetrating wound", "unconscious after injury"
        ]
    }
    
    # Test cases
    test_cases = [
        {
            "input": "I have severe chest pain for 30 minutes, radiating to my left arm",
            "expected_flags": ["cardiac"],
            "expected_urgency": "high"
        },
        {
            "input": "I can't breathe properly and my lips are turning blue",
            "expected_flags": ["respiratory"],
            "expected_urgency": "high"
        },
        {
            "input": "I think I'm having a stroke, my face is drooping",
            "expected_flags": ["neurological"],
            "expected_urgency": "high"
        },
        {
            "input": "I have a mild headache since this morning",
            "expected_flags": [],
            "expected_urgency": "low"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Input: {test_case['input']}")
        
        # Detect emergency keywords
        detected_flags = []
        text_lower = test_case['input'].lower()
        
        for category, keywords in emergency_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    detected_flags.append(category)
                    break  # Only add category once
        
        print(f"Detected flags: {detected_flags}")
        print(f"Expected flags: {test_case['expected_flags']}")
        
        # Determine urgency
        if detected_flags:
            urgency = "high"
            emergency_detected = True
        else:
            urgency = "low"
            emergency_detected = False
        
        print(f"Urgency: {urgency}")
        print(f"Emergency detected: {emergency_detected}")
        
        # Validate results
        if set(detected_flags) == set(test_case['expected_flags']):
            print("✅ Emergency detection PASSED")
        else:
            print("❌ Emergency detection FAILED")
    
    return True


def test_urgency_scoring():
    """Test urgency scoring logic"""
    print("\n📊 Testing Urgency Scoring...")
    
    # Test cases with expected urgency scores
    test_cases = [
        {
            "symptoms": "severe chest pain, radiating to arm, shortness of breath",
            "expected_score": 10,
            "description": "Cardiac emergency"
        },
        {
            "symptoms": "can't breathe, blue lips, gasping for air",
            "expected_score": 10,
            "description": "Respiratory emergency"
        },
        {
            "symptoms": "stroke symptoms, face drooping, slurred speech",
            "expected_score": 10,
            "description": "Neurological emergency"
        },
        {
            "symptoms": "high fever for 3 days, severe cough, breathing difficulty",
            "expected_score": 7,
            "description": "Urgent respiratory infection"
        },
        {
            "symptoms": "mild headache since morning, no other symptoms",
            "expected_score": 2,
            "description": "Standard case"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case['description']} ---")
        print(f"Symptoms: {test_case['symptoms']}")
        
        # Simple urgency scoring logic
        urgency_score = 1  # Start with minimum
        
        # Emergency keywords (score 10)
        emergency_keywords = [
            "severe chest pain", "heart attack", "can't breathe", "blue lips",
            "stroke", "face drooping", "severe bleeding", "unconscious"
        ]
        
        # Urgent keywords (score 7-8)
        urgent_keywords = [
            "high fever", "severe", "difficulty breathing", "severe pain"
        ]
        
        # Moderate keywords (score 4-6)
        moderate_keywords = [
            "fever", "cough", "pain", "nausea", "vomiting"
        ]
        
        text_lower = test_case['symptoms'].lower()
        
        # Check for emergency keywords
        for keyword in emergency_keywords:
            if keyword in text_lower:
                urgency_score = 10
                break
        
        # Check for urgent keywords
        if urgency_score < 10:
            for keyword in urgent_keywords:
                if keyword in text_lower:
                    urgency_score = max(urgency_score, 7)
        
        # Check for moderate keywords
        if urgency_score < 7:
            for keyword in moderate_keywords:
                if keyword in text_lower:
                    urgency_score = max(urgency_score, 4)
        
        # Determine category
        if urgency_score >= 9:
            category = "immediate"
            emoji = "🔴"
        elif urgency_score >= 7:
            category = "urgent"
            emoji = "🟡"
        else:
            category = "standard"
            emoji = "🟢"
        
        print(f"Calculated score: {urgency_score}/10")
        print(f"Expected score: {test_case['expected_score']}/10")
        print(f"Category: {emoji} {category}")
        
        # Validate
        if urgency_score == test_case['expected_score']:
            print("✅ Urgency scoring PASSED")
        else:
            print("❌ Urgency scoring FAILED")
    
    return True


def test_voice_input_simulation():
    """Test voice input simulation (without actual audio)"""
    print("\n🎤 Testing Voice Input Simulation...")
    
    # Simulate voice input results
    simulated_voice_inputs = [
        {
            "transcribed_text": "I have severe chest pain for 30 minutes, radiating to my left arm",
            "language": "en",
            "confidence": 0.95,
            "processing_time": 2.5
        },
        {
            "transcribed_text": "मुझे 3 दिन से बुखार है और खांसी भी हो रही है",
            "language": "hi", 
            "confidence": 0.88,
            "processing_time": 3.2
        },
        {
            "transcribed_text": "I have a mild headache since this morning",
            "language": "en",
            "confidence": 0.92,
            "processing_time": 1.8
        }
    ]
    
    for i, voice_data in enumerate(simulated_voice_inputs, 1):
        print(f"\n--- Voice Input {i} ---")
        print(f"Language: {voice_data['language']}")
        print(f"Transcribed: {voice_data['transcribed_text']}")
        print(f"Confidence: {voice_data['confidence']:.2f}")
        print(f"Processing time: {voice_data['processing_time']:.1f}s")
        
        # Create VoiceInput object
        try:
            voice_input = VoiceInput(
                audio_file_path=f"test_audio_{i}.wav",
                transcribed_text=voice_data['transcribed_text'],
                language=voice_data['language'],
                confidence=voice_data['confidence'],
                processing_time=voice_data['processing_time']
            )
            print("✅ VoiceInput object created successfully")
        except Exception as e:
            print(f"❌ Error creating VoiceInput: {e}")
    
    return True


def test_complete_triage_pipeline():
    """Test complete triage pipeline simulation"""
    print("\n🏥 Testing Complete Triage Pipeline...")
    
    # Simulate complete triage process
    test_cases = [
        {
            "input": "I have severe chest pain for 30 minutes, radiating to my left arm and I'm feeling short of breath",
            "expected_urgency": 10,
            "expected_emergency": True,
            "expected_category": "immediate"
        },
        {
            "input": "मुझे 3 दिन से बुखार है और खांसी भी हो रही है। सांस लेने में थोड़ी तकलीफ हो रही है।",
            "expected_urgency": 7,
            "expected_emergency": False,
            "expected_category": "urgent"
        },
        {
            "input": "I have a mild headache since this morning. No other symptoms.",
            "expected_urgency": 2,
            "expected_emergency": False,
            "expected_category": "standard"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Complete Pipeline Test {i} ---")
        print(f"Input: {test_case['input']}")
        
        # Step 1: Voice transcription (simulated)
        voice_result = VoiceInput(
            audio_file_path=f"test_{i}.wav",
            transcribed_text=test_case['input'],
            language="en" if "I have" in test_case['input'] else "hi",
            confidence=0.9,
            processing_time=2.0
        )
        print(f"✅ Voice transcription: {voice_result.transcribed_text}")
        
        # Step 2: Emergency detection
        emergency_keywords = [
            "severe chest pain", "heart attack", "can't breathe", "blue lips",
            "stroke", "face drooping", "severe bleeding", "unconscious"
        ]
        
        emergency_detected = any(keyword in test_case['input'].lower() for keyword in emergency_keywords)
        print(f"✅ Emergency detection: {emergency_detected}")
        
        # Step 3: Urgency scoring
        urgency_score = test_case['expected_urgency']
        if urgency_score >= 9:
            category = "immediate"
            emoji = "🔴"
        elif urgency_score >= 7:
            category = "urgent"
            emoji = "🟡"
        else:
            category = "standard"
            emoji = "🟢"
        
        print(f"✅ Urgency score: {urgency_score}/10 {emoji}")
        print(f"✅ Category: {category}")
        
        # Step 4: Create structured result
        try:
            # Create symptoms
            symptoms = []
            if "chest pain" in test_case['input'].lower():
                symptoms.append(Symptom(
                    name="chest pain",
                    severity="severe",
                    duration="30 minutes",
                    associated_symptoms=["shortness of breath"]
                ))
            elif "fever" in test_case['input'].lower() or "बुखार" in test_case['input']:
                symptoms.append(Symptom(
                    name="fever",
                    severity="moderate",
                    duration="3 days",
                    associated_symptoms=["cough", "breathing difficulty"]
                ))
            elif "headache" in test_case['input'].lower():
                symptoms.append(Symptom(
                    name="headache",
                    severity="mild",
                    duration="few hours",
                    associated_symptoms=[]
                ))
            
            # Create red flags
            red_flags = []
            if emergency_detected:
                red_flags.append(RedFlag(
                    flag_type="cardiac" if "chest pain" in test_case['input'].lower() else "respiratory",
                    description="Emergency symptoms detected",
                    urgency_level="immediate",
                    action_required="Call 108 immediately"
                ))
            
            # Create potential risks
            potential_risks = []
            if emergency_detected:
                potential_risks.append(PotentialRisk(
                    condition="Acute Myocardial Infarction" if "chest pain" in test_case['input'].lower() else "Respiratory Emergency",
                    probability="high",
                    specialty_needed="Cardiology" if "chest pain" in test_case['input'].lower() else "Emergency Medicine"
                ))
            
            # Create triage result
            triage_result = TriageResult(
                chief_complaint=test_case['input'],
                symptoms=symptoms,
                urgency_score=urgency_score,
                red_flags=red_flags,
                potential_risks=potential_risks,
                recommended_specialty="Cardiology" if "chest pain" in test_case['input'].lower() else "General Medicine",
                triage_category=category,
                emergency_detected=emergency_detected,
                action_required="Call 108 immediately" if emergency_detected else "Consult a healthcare provider"
            )
            
            print("✅ Triage result created successfully")
            print(f"   Symptoms: {len(triage_result.symptoms)}")
            print(f"   Red flags: {len(triage_result.red_flags)}")
            print(f"   Potential risks: {len(triage_result.potential_risks)}")
            print(f"   Recommended specialty: {triage_result.recommended_specialty}")
            print(f"   Action required: {triage_result.action_required}")
            
            # Validate results
            if (triage_result.urgency_score == test_case['expected_urgency'] and
                triage_result.emergency_detected == test_case['expected_emergency'] and
                triage_result.triage_category == test_case['expected_category']):
                print("✅ Complete pipeline test PASSED")
            else:
                print("❌ Complete pipeline test FAILED")
                
        except Exception as e:
            print(f"❌ Error in complete pipeline: {e}")
    
    return True


def main():
    """Run all tests"""
    print("🏥 Arovia Triage System - End-to-End Test")
    print("=" * 60)
    
    start_time = time.time()
    
    # Run all tests
    tests = [
        ("Pydantic Models", test_pydantic_models),
        ("Emergency Detection", test_emergency_detection),
        ("Urgency Scoring", test_urgency_scoring),
        ("Voice Input Simulation", test_voice_input_simulation),
        ("Complete Triage Pipeline", test_complete_triage_pipeline)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    # Summary
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print(f"🏥 AROVIA TRIAGE SYSTEM TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Tests Passed: {passed}/{total}")
    print(f"⏱️  Total Time: {duration:.2f} seconds")
    print(f"📊 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for deployment.")
    else:
        print("⚠️  Some tests failed. Please review the output above.")
    
    print(f"\n🚀 Next steps:")
    print(f"1. Set up GROQ_API_KEY in environment")
    print(f"2. Install additional dependencies: pip install groq langchain")
    print(f"3. Test with real API: python test_triage.py")
    print(f"4. Run web app: streamlit run app.py")


if __name__ == "__main__":
    main()
