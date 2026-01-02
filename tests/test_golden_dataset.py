
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from agents.triage_agent import AroviaTriageAgent

@pytest.fixture
def agent():
    """Initialize triage agent for testing"""
    return AroviaTriageAgent()

@pytest.fixture
def golden_dataset():
    """Load the golden dataset from file"""
    with open("golden_dataset.json", "r") as f:
        return json.load(f)

def test_golden_dataset(agent, golden_dataset):
    """Test the agent against the golden dataset"""
    for case in golden_dataset:
        input_text = case["input"]
        expected_urgency = case["expected_urgency"]
        expected_category = case["expected_category"]
        expected_specialty = case["expected_specialty"]

        triage_result, _ = agent.analyze_symptoms_from_text(input_text)

        assert triage_result.urgency_score == expected_urgency
        assert triage_result.triage_category == expected_category
        assert triage_result.recommended_specialty == expected_specialty
