#!/usr/bin/env python3
"""
Test client for Arovia Health Desk API
"""
import requests
import json
import time
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()['status']}")
            print(f"   Services: {response.json()['services']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_text_triage():
    """Test text-based triage"""
    print("\n🔍 Testing text triage...")
    try:
        data = {
            "symptoms": "I have severe chest pain for 30 minutes, radiating to my left arm",
            "location": "Hyderabad, Telangana"
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/text", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Text triage successful")
            print(f"   Urgency Score: {result['urgency_score']}/10")
            print(f"   Chief Complaint: {result['chief_complaint']}")
            print(f"   Emergency Detected: {result['emergency_detected']}")
        else:
            print(f"❌ Text triage failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Text triage error: {e}")

def test_facilities():
    """Test facility search"""
    print("\n🔍 Testing facility search...")
    try:
        data = {
            "location": "Hyderabad, Telangana"
        }
        
        response = requests.post(f"{API_BASE_URL}/facilities", json=data)
        if response.status_code == 200:
            facilities = response.json()
            print(f"✅ Found {len(facilities)} facilities")
            for i, facility in enumerate(facilities[:3], 1):
                print(f"   {i}. {facility['name']} - {facility['distance_km']}km")
        else:
            print(f"❌ Facility search failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Facility search error: {e}")

def test_languages():
    """Test supported languages"""
    print("\n🔍 Testing supported languages...")
    try:
        response = requests.get(f"{API_BASE_URL}/languages")
        if response.status_code == 200:
            languages = response.json()
            print(f"✅ Found {len(languages)} supported languages")
            print("   Major languages:", list(languages.keys())[:10])
        else:
            print(f"❌ Language check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Language check error: {e}")

def test_model_info():
    """Test model information"""
    print("\n🔍 Testing model info...")
    try:
        response = requests.get(f"{API_BASE_URL}/models")
        if response.status_code == 200:
            models = response.json()
            print("✅ Model info retrieved")
            print(f"   Groq Model: {models.get('groq', {}).get('model', 'Unknown')}")
            print(f"   Whisper Model: {models.get('whisper', {}).get('model', 'Unknown')}")
        else:
            print(f"❌ Model info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Model info error: {e}")

def main():
    """Run all API tests"""
    print("🧪 Arovia Health Desk API Test Suite")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for API to be ready...")
    time.sleep(2)
    
    # Run tests
    test_health_check()
    test_text_triage()
    test_facilities()
    test_languages()
    test_model_info()
    
    print("\n🎉 API testing completed!")
    print(f"📚 API Documentation: {API_BASE_URL}/docs")

if __name__ == "__main__":
    main()
