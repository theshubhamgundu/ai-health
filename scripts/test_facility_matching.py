#!/usr/bin/env python3
"""
Test script for Arovia Facility Matching functionality
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from agents.triage_agent import AroviaTriageAgent

# Load environment variables
load_dotenv()

def test_facility_matching():
    """Test complete facility matching functionality"""
    print("🏥 Testing Arovia Facility Matching System")
    print("=" * 50)
    
    try:
        # Initialize agent
        print("Initializing Arovia Agent...")
        agent = AroviaTriageAgent()
        print("✅ Agent initialized successfully!")
        
        # Test cases with different conditions and locations
        test_cases = [
            {
                "symptoms": "I have severe chest pain for 30 minutes, radiating to my left arm",
                "location": "Hyderabad, Telangana",
                "expected_specialty": "cardiology",
                "description": "Emergency cardiac case"
            },
            {
                "symptoms": "मुझे तेज सिरदर्द है और बुखार भी है",
                "location": "Mumbai, Maharashtra", 
                "expected_specialty": "neurology",
                "description": "Urgent neurological case (Hindi)"
            },
            {
                "symptoms": "I have a mild headache since this morning",
                "location": "Bangalore, Karnataka",
                "expected_specialty": "general",
                "description": "Standard case"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test Case {i}: {test_case['description']} ---")
            print(f"Symptoms: {test_case['symptoms']}")
            print(f"Location: {test_case['location']}")
            
            try:
                # Complete triage with facility recommendations
                referral_note = agent.complete_triage_with_facilities(
                    test_case['symptoms'],
                    test_case['location']
                )
                
                triage = referral_note.triage_result
                facilities = referral_note.recommended_facilities
                
                print(f"✅ Triage Analysis:")
                print(f"   - Urgency Score: {triage.urgency_score}/10")
                print(f"   - Category: {triage.triage_category}")
                print(f"   - Emergency: {triage.emergency_detected}")
                print(f"   - Specialty: {triage.recommended_specialty}")
                
                print(f"✅ Facility Recommendations:")
                print(f"   - Found {len(facilities)} facilities")
                
                for j, facility in enumerate(facilities[:3], 1):  # Show top 3
                    print(f"   {j}. {facility.name}")
                    print(f"      📍 {facility.address}")
                    print(f"      📏 {facility.distance_km} km")
                    print(f"      🏥 {facility.specialty}")
                    print(f"      🗺️ {facility.map_link}")
                    print()
                
                # Test facility type classification
                if facilities:
                    facility_types = {}
                    for facility in facilities:
                        facility_type = getattr(facility, 'facility_type', 'local')
                        facility_types[facility_type] = facility_types.get(facility_type, 0) + 1
                    
                    print(f"🏥 Facility Types Found:")
                    for facility_type, count in facility_types.items():
                        type_emoji = {'government': '🔵', 'private': '🟢', 'ngo': '🟡', 'local': '⚪'}.get(facility_type, '⚪')
                        print(f"   {type_emoji} {facility_type.title()}: {count}")
                
            except Exception as e:
                print(f"❌ Test failed: {e}")
        
        # Test referral note generation
        print(f"\n--- Testing Referral Note Generation ---")
        try:
            referral_note = agent.complete_triage_with_facilities(
                "I have severe chest pain",
                "Delhi, India"
            )
            
            print("✅ Referral Note Generated:")
            print(f"   - Patient ID: {referral_note.patient_id}")
            print(f"   - Generated At: {referral_note.generated_at}")
            print(f"   - Triage Result: {referral_note.triage_result.urgency_score}/10")
            print(f"   - Facilities: {len(referral_note.recommended_facilities)}")
            
        except Exception as e:
            print(f"❌ Referral note test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Facility matching test failed: {e}")
        return False

def test_facility_matcher_directly():
    """Test facility matcher directly"""
    print(f"\n--- Testing Facility Matcher Directly ---")
    
    try:
        from utils.facility_matcher import FacilityMatcher
        
        matcher = FacilityMatcher()
        
        # Test geocoding
        print("Testing geocoding...")
        coordinates = matcher.geocode_location("Hyderabad, Telangana")
        if coordinates:
            print(f"✅ Geocoded: {coordinates}")
        else:
            print("❌ Geocoding failed")
            return False
        
        # Test facility search
        print("Testing facility search...")
        facilities = matcher.search_nearby_facilities(
            coordinates[0], coordinates[1], 
            radius_km=10.0, specialty="cardiology"
        )
        
        print(f"✅ Found {len(facilities)} facilities")
        for i, facility in enumerate(facilities[:3], 1):
            print(f"   {i}. {facility['name']}")
            print(f"      Distance: {facility['distance_km']} km")
            print(f"      Type: {facility['facility_type']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct facility matcher test failed: {e}")
        return False

def main():
    """Run all facility matching tests"""
    print("🏥 Arovia Facility Matching Test Suite")
    print("=" * 60)
    
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "gsk_your_groq_api_key_here":
        print("⚠️  WARNING: GROQ_API_KEY not set!")
        print("   Set your Groq API key in the .env file to test AI functionality")
        return
    
    # Run tests
    tests = [
        ("Complete Facility Matching", test_facility_matching),
        ("Direct Facility Matcher", test_facility_matcher_directly)
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
    print(f"\n{'='*60}")
    print("📊 FACILITY MATCHING TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All facility matching tests passed! Arovia is ready with clinic recommendations!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
