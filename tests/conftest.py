"""
Pytest configuration and shared fixtures for Arovia test suite
"""
import pytest
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@pytest.fixture(scope="session")
def api_key_available():
    """Check if Groq API key is available for testing"""
    api_key = os.getenv("GROQ_API_KEY")
    return api_key and api_key != "gsk_your_groq_api_key_here"

@pytest.fixture(scope="session")
def skip_if_no_api_key(api_key_available):
    """Skip tests if API key is not available"""
    if not api_key_available:
        pytest.skip("GROQ_API_KEY not available for testing")

@pytest.fixture
def sample_emergency_cases():
    """Sample emergency test cases"""
    return [
        "I have severe chest pain for 30 minutes, radiating to my left arm",
        "I think I'm having a stroke, my face is drooping",
        "I can't breathe and my lips are turning blue",
        "Severe bleeding from a deep cut on my arm",
        "I want to kill myself"
    ]

@pytest.fixture
def sample_urgent_cases():
    """Sample urgent test cases"""
    return [
        "High fever for 3 days with severe headache",
        "Severe abdominal pain for 2 hours",
        "Difficulty breathing with chest tightness",
        "Persistent vomiting for 6 hours"
    ]

@pytest.fixture
def sample_standard_cases():
    """Sample standard test cases"""
    return [
        "Mild headache since this morning",
        "Small cut on my finger",
        "Slight cough and runny nose",
        "Mild stomach ache"
    ]

@pytest.fixture
def multilingual_test_cases():
    """Multilingual test cases"""
    return {
        "hindi": "मुझे तेज सिरदर्द है और बुखार भी है",
        "bengali": "আমার বুকে ব্যথা হচ্ছে",
        "telugu": "నాకు తీవ్రమైన ఛాతీ నొప్పి ఉంది",
        "tamil": "எனக்கு கடுமையான தலைவலி உள்ளது",
        "gujarati": "મને છાતીમાં દુખાવો છે"
    }
