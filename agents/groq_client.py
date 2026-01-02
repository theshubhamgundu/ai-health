"""
Groq Cloud integration with Llama 3.3 70B for medical triage
"""
import os
from typing import Optional, Dict, Any, List
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class GroqClient:
    """Groq Cloud client for Llama 3.3 70B medical reasoning"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq client
        
        Args:
            api_key: Groq API key (if None, will try to get from environment)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)
        
        # Initialize LangChain Groq
        self.llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.1,  # Low temperature for medical accuracy
            max_tokens=2048,
            timeout=30.0
        )
        
        print("Groq client initialized successfully!")
    
    def test_connection(self) -> bool:
        """Test connection to Groq API"""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello, test connection"}],
                model="llama-3.3-70b-versatile",
                max_tokens=10
            )
            return True
        except Exception as e:
            print(f"Groq connection test failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model": "llama-3.3-70b-versatile",
            "provider": "Groq Cloud",
            "max_tokens": 2048,
            "temperature": 0.1,
            "capabilities": [
                "Medical reasoning",
                "Symptom analysis", 
                "Urgency assessment",
                "Red flag detection",
                "Multilingual support"
            ]
        }


class MedicalTriageAgent:
    """LangChain agent for medical triage using Groq/Llama 3.3 70B"""
    
    def __init__(self, groq_client: GroqClient):
        """
        Initialize medical triage agent
        
        Args:
            groq_client: Initialized GroqClient instance
        """
        self.groq_client = groq_client
        self.llm = groq_client.llm
        
        # Emergency keywords for red flag detection
        self.emergency_keywords = {
            "cardiac": [
                "chest pain", "heart attack", "crushing chest pressure",
                "pain radiating to arm", "pain radiating to jaw", 
                "severe palpitations", "heart racing", "cardiac arrest"
            ],
            "neurological": [
                "stroke", "face drooping", "arm weakness", "slurred speech",
                "sudden severe headache", "loss of consciousness", "seizure",
                "paralysis", "numbness", "confusion", "difficulty speaking"
            ],
            "respiratory": [
                "can't breathe", "choking", "severe shortness of breath",
                "blue lips", "gasping for air", "respiratory distress",
                "chest tightness", "wheezing"
            ],
            "trauma": [
                "severe bleeding", "head injury", "broken bone visible",
                "penetrating wound", "unconscious after injury", "major trauma",
                "car accident", "fall from height"
            ],
            "mental_health": [
                "suicide", "want to die", "self-harm", "kill myself",
                "suicidal thoughts", "harm myself"
            ],
            "other": [
                "severe abdominal pain", "pregnancy bleeding", 
                "high fever in infant", "allergic reaction swelling",
                "anaphylaxis", "severe allergic reaction"
            ]
        }
    
    def detect_emergency_keywords(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect emergency keywords in patient input
        
        Args:
            text: Patient input text
            
        Returns:
            List of detected emergency keywords with categories
        """
        text_lower = text.lower()
        detected_flags = []
        
        for category, keywords in self.emergency_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    detected_flags.append({
                        "category": category,
                        "keyword": keyword,
                        "urgency": "immediate" if category in ["cardiac", "neurological", "respiratory"] else "urgent"
                    })
        
        return detected_flags
    
    def create_triage_prompt(self, patient_input: str, detected_flags: List[Dict[str, Any]]) -> str:
        """
        Create medical triage prompt for Llama 3.3 70B
        
        Args:
            patient_input: Patient's symptom description
            detected_flags: Detected emergency keywords
            
        Returns:
            Formatted prompt for medical triage
        """
        emergency_context = ""
        if detected_flags:
            emergency_context = f"""
            ⚠️ EMERGENCY KEYWORDS DETECTED:
            {chr(10).join([f"- {flag['category'].upper()}: {flag['keyword']}" for flag in detected_flags])}
            """
        
        prompt = f"""
You are Arovia, an AI medical triage assistant designed for India's healthcare system. Your role is to analyze patient symptoms and provide structured medical triage assessment.

PATIENT INPUT: "{patient_input}"
{emergency_context}

MEDICAL TRIAGE ASSESSMENT REQUIRED:

Please analyze the patient's symptoms and provide a structured assessment in the following JSON format:

{{
    "chief_complaint": "Primary complaint in patient's own words",
    "symptoms": [
        {{
            "name": "symptom name",
            "severity": "mild|moderate|severe",
            "duration": "time duration if mentioned",
            "associated_symptoms": ["related symptoms"]
        }}
    ],
    "urgency_score": 1-10,
    "red_flags": [
        {{
            "flag_type": "cardiac|neurological|respiratory|trauma|mental_health|other",
            "description": "description of red flag",
            "urgency_level": "immediate|urgent",
            "action_required": "specific action needed"
        }}
    ],
    "potential_risks": [
        {{
            "condition": "potential medical condition",
            "probability": "low|medium|high",
            "specialty_needed": "required medical specialty"
        }}
    ],
    "recommended_specialty": "primary medical specialty needed",
    "triage_category": "immediate|urgent|standard",
    "emergency_detected": true/false,
    "action_required": "immediate action required"
}}

URGENCY SCORING GUIDELINES:
- 1-3: Minor symptoms, self-care possible
- 4-6: Moderate symptoms, see doctor within 24-48 hours  
- 7-8: Urgent symptoms, see doctor within 4-6 hours
- 9-10: Emergency symptoms, immediate medical attention required

RED FLAG CRITERIA:
- Cardiac: chest pain, heart attack symptoms, severe palpitations
- Neurological: stroke symptoms, sudden severe headache, loss of consciousness
- Respiratory: severe breathing difficulty, choking, blue lips
- Trauma: severe bleeding, head injury, major trauma
- Mental Health: suicidal thoughts, self-harm intentions

MEDICAL SAFETY:
- If ANY red flags detected, set urgency_score to 9-10
- If emergency_detected is true, recommend immediate action
- Always prioritize patient safety over convenience
- Consider Indian healthcare context and available resources

Respond ONLY with valid JSON. No additional text or explanations.
"""
        return prompt
    
    def analyze_symptoms(self, patient_input: str) -> Dict[str, Any]:
        """
        Analyze patient symptoms using Llama 3.3 70B
        
        Args:
            patient_input: Patient's symptom description
            
        Returns:
            Structured triage assessment
        """
        try:
            # Detect emergency keywords first
            detected_flags = self.detect_emergency_keywords(patient_input)
            
            # Create medical triage prompt
            prompt = self.create_triage_prompt(patient_input, detected_flags)
            
            # Get response from Llama 3.3 70B
            start_time = time.time()
            response = self.llm.invoke(prompt)
            processing_time = time.time() - start_time
            
            # Parse JSON response
            try:
                # Clean the response content (remove markdown code blocks if present)
                content = response.content.strip()
                if content.startswith("```") and content.endswith("```"):
                    # Remove markdown code blocks
                    lines = content.split('\n')
                    content = '\n'.join(lines[1:-1])  # Remove first and last lines
                elif content.startswith("```json"):
                    # Remove json markdown code blocks
                    lines = content.split('\n')
                    content = '\n'.join(lines[1:-1])  # Remove first and last lines
                
                result = json.loads(content)
                result["processing_time"] = processing_time
                return result
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {response.content}")
                
                # Fallback: return basic assessment
                return {
                    "chief_complaint": patient_input,
                    "urgency_score": 5,
                    "emergency_detected": len(detected_flags) > 0,
                    "error": "Failed to parse AI response",
                    "processing_time": processing_time
                }
                
        except Exception as e:
            print(f"Error in symptom analysis: {e}")
            return {
                "chief_complaint": patient_input,
                "urgency_score": 5,
                "emergency_detected": False,
                "error": str(e),
                "processing_time": 0
            }


class MedicalRelevanceAgent:
    """Agent to check for medical relevance in a given text"""
    
    def __init__(self, groq_client: GroqClient):
        """
        Initialize medical relevance agent
        
        Args:
            groq_client: Initialized GroqClient instance
        """
        self.groq_client = groq_client
        self.llm = groq_client.llm
    
    def create_relevance_prompt(self, text: str) -> str:
        """
        Create prompt to check for medical relevance
        
        Args:
            text: The text to analyze
            
        Returns:
            Formatted prompt for relevance check
        """
        prompt = f"""
You are a medical relevance classification assistant. Your task is to determine if the following text contains any information related to health, symptoms, or medical conditions. The user may be trying to describe a health problem.

TEXT: "{text}"

Is this text medically relevant? Respond with ONLY a JSON object in the following format:

{{
    "is_relevant": true/false,
    "reason": "brief explanation for your decision"
}}

Examples:
- "I have a headache" -> {{"is_relevant": true, "reason": "Mentions a common medical symptom."}}
- "What is the weather today?" -> {{"is_relevant": false, "reason": "This is a general question, not related to health."}}
- "My car is broken" -> {{"is_relevant": false, "reason": "This is about a car, not a person's health."}}
- "I feel sad and tired all the time" -> {{"is_relevant": true, "reason": "Describes symptoms related to mental and physical health."}}

Respond ONLY with the JSON object.
"""
        return prompt
    
    def check_relevance(self, text: str) -> Dict[str, Any]:
        """
        Check if the text is medically relevant
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with relevance information
        """
        try:
            # Create relevance prompt
            prompt = self.create_relevance_prompt(text)
            
            # Get response from Llama 3.3 70B
            response = self.llm.invoke(prompt)
            
            # Parse JSON response
            try:
                content = response.content.strip()
                result = json.loads(content)
                result["raw_response"] = content
                return result
            except json.JSONDecodeError as e:
                print(f"JSON parsing error in relevance check: {e}")
                # Default to relevant to avoid false negatives
                return {"is_relevant": True, "reason": "Error parsing AI response."}
                
        except Exception as e:
            print(f"Error in relevance check: {e}")
            # Default to relevant in case of other errors
            return {"is_relevant": True, "reason": f"An unexpected error occurred: {e}"}


# Convenience function for quick triage
def quick_triage(patient_input: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Quick function to perform medical triage
    
    Args:
        patient_input: Patient's symptom description
        api_key: Groq API key (optional)
        
    Returns:
        Triage assessment result
    """
    try:
        # Initialize Groq client
        groq_client = GroqClient(api_key=api_key)
        
        # Test connection
        if not groq_client.test_connection():
            raise Exception("Failed to connect to Groq API")
        
        # Initialize triage agent
        triage_agent = MedicalTriageAgent(groq_client)
        
        # Analyze symptoms
        result = triage_agent.analyze_symptoms(patient_input)
        
        return result
        
    except Exception as e:
        print(f"Error in quick triage: {e}")
        return {
            "chief_complaint": patient_input,
            "urgency_score": 5,
            "emergency_detected": False,
            "error": str(e),
            "processing_time": 0
        }


if __name__ == "__main__":
    # Test the Groq client and triage agent
    print("Testing Groq client and medical triage agent...")
    
    # Test cases
    test_cases = [
        "I have severe chest pain for 30 minutes, radiating to my left arm",
        "मुझे 3 दिन से बुखार है और खांसी भी हो रही है",  # Hindi: fever and cough for 3 days
        "I have a mild headache since this morning",
        "I can't breathe properly and my lips are turning blue"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Input: {test_input}")
        
        try:
            result = quick_triage(test_input)
            print(f"Urgency Score: {result.get('urgency_score', 'N/A')}")
            print(f"Emergency Detected: {result.get('emergency_detected', 'N/A')}")
            print(f"Processing Time: {result.get('processing_time', 0):.2f}s")
            
            if 'error' in result:
                print(f"Error: {result['error']}")
                
        except Exception as e:
            print(f"Test failed: {e}")
