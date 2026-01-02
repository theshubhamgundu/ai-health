
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from utils.facility_matcher import FacilityMatcher
from models.schemas import TriageResult

@pytest.fixture
def facility_matcher():
    """Initialize the facility matcher for testing"""
    return FacilityMatcher()

def test_find_facilities_for_condition(facility_matcher):
    """Test finding facilities for a given condition and location."""
    facilities = facility_matcher.find_facilities_for_condition(
        "Delhi", "Cardiology", 10
    )
    assert len(facilities) > 0
    for facility in facilities:
        assert "Cardiology" in facility.services

def test_search_nearby_facilities(facility_matcher):
    """Test searching for nearby facilities using coordinates."""
    # Coordinates for Delhi
    lat, lon = 28.7041, 77.1025
    facilities = facility_matcher.search_nearby_facilities(lat, lon, 10, "emergency")
    assert len(facilities) > 0
    for facility in facilities:
        assert "emergency" in facility.services or "trauma" in facility.services
