# 🏥 AI Health - Arovia Health Desk Agent

> Intelligent triage assistant revolutionizing first-point healthcare access in India

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)](https://github.com/langchain-ai/langchain)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-purple.svg)](https://groq.com)
[![Status](https://img.shields.io/badge/Status-Live%20Demo-success.svg)](https://ai-health-kappa.vercel.app/)

---

### 👨‍💻 Developed By
**Shubham Gundu**
- **GitHub:** [github.com/theshubhamgundu](https://github.com/theshubhamgundu)
- **Repo:** [github.com/theshubhamgundu/ai-health](https://github.com/theshubhamgundu/ai-health)
- **Live Demo:** [ai-health-kappa.vercel.app](https://ai-health-kappa.vercel.app/)

---

## 🌟 What is Arovia?

**Arovia** is an AI-powered Health Desk Agent designed to be the intelligent first point of contact in India's overburdened public health system. Named after the fusion of "AI" and "Rovia" (Sanskrit for healing), Arovia combines cutting-edge language models with medical protocols to provide safe, accurate, and accessible health triage.

### The Problem We're Solving

India faces a critical healthcare access crisis:
- 🏥 Doctor-to-patient ratio: **1:1,445** (WHO recommends 1:1,000)
- ⏰ Average wait time: **2-4 hours** for basic consultations
- 🚨 Non-clinical front-desk staff making critical triage decisions
- 🗺️ Patients arriving at facilities that can't treat their condition
- 📊 10+ minutes average door-to-triage time at Primary Health Centers

**Arovia bridges this gap** by providing instant, intelligent triage that:
1. Identifies emergency symptoms requiring immediate care
2. Assesses urgency levels with medical accuracy
3. Matches patients to appropriate nearby facilities
4. Generates structured referral notes for healthcare providers

---

## ✨ Key Features

### 🎯 Intelligent Symptom Triage
- Natural language understanding of patient symptoms
- Context-aware follow-up questions
- Urgency scoring (1-10 scale) using validated medical protocols
- Identification of potential conditions and risks

### 🚨 Emergency Detection System
- Real-time red flag identification for life-threatening conditions
- Immediate escalation protocols for cardiac, neurological, and trauma cases
- Built-in safety rails to prevent misdiagnosis

### 🗣️ Multilingual Voice Interface
- Speech-to-text using Whisper-Large model
- Support for Hindi, English, and other Indic languages
- Accessible for low-literacy populations

### 📍 Smart Facility Matching
- Real-time geolocation using OpenStreetMap
- Search for nearby clinics within customizable radius
- Filter by specialty and service availability
- Distance calculation and map links

### 📋 Structured Referral Notes
- Medical-compliant documentation format
- Comprehensive symptom summary
- Urgency assessment and red flags
- Recommended facilities with contact information
- Downloadable for easy handoff to healthcare providers

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        AROVIA INTERFACE                          │
│                   Streamlit Web Application                       │
│         [💬 Text Input]  OR  [🎤 Voice Recording]                │
└─────────────────────────┬────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                    VOICE PROCESSING LAYER                         │
│                                                                   │
│  ╔══════════════════════════════════════════════════════════╗   │
│  ║          Whisper-Large Speech Recognition                ║   │
│  ║  • Transcribes patient voice input to text              ║   │
│  ║  • Supports Hindi, English, Telugu, Tamil               ║   │
│  ║  • Handles accents and background noise                 ║   │
│  ╚══════════════════════════════════════════════════════════╝   │
└─────────────────────────┬────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                   AROVIA INTELLIGENCE CORE                        │
│                     Powered by LangChain                          │
│                                                                   │
│  ╔══════════════════════════════════════════════════════════╗   │
│  ║              Llama 3.3 70B (Groq Cloud)                  ║   │
│  ║                                                           ║   │
│  ║  🧠 Medical Reasoning Engine:                            ║   │
│  ║     ├─ Extract: Chief complaint & symptoms               ║   │
│  ║     ├─ Analyze: Severity, duration, progression          ║   │
│  ║     ├─ Score: Urgency level (1-10)                       ║   │
│  ║     ├─ Identify: Red flag symptoms                       ║   │
│  ║     └─ Assess: Potential conditions & risks              ║   │
│  ║                                                           ║   │
│  ║  📝 Structured Output (Pydantic Model):                  ║   │
│  ║     {                                                     ║   │
│  ║       "chief_complaint": "...",                          ║   │
│  ║       "symptoms": [...],                                 ║   │
│  ║       "urgency_score": 8,                                ║   │
│  ║       "red_flags": [...],                                ║   │
│  ║       "potential_risks": [...],                          ║   │
│  ║       "recommended_specialty": "..."                     ║   │
│  ║     }                                                     ║   │
│  ╚══════════════════════════════════════════════════════════╝   │
│                          │                                        │
│              ┌───────────┴───────────┐                           │
│              │                       │                            │
│              ▼                       ▼                            │
│   ┏━━━━━━━━━━━━━━━┓       ┏━━━━━━━━━━━━━━━┓                     │
│   ┃  🚨 RED FLAG  ┃       ┃   ✅ NORMAL   ┃                     │
│   ┃   DETECTOR    ┃       ┃    TRIAGE     ┃                     │
│   ┗━━━━━┯━━━━━━━━━┛       ┗━━━━━┯━━━━━━━━━┛                     │
│         │                        │                               │
│         │ Emergency Keywords     │                               │
│         ▼                        │                               │
│   ┌─────────────┐               │                               │
│   │  IMMEDIATE  │               │                               │
│   │ ESCALATION  │               │                               │
│   │   ⚠️ 108    │               │                               │
│   └─────────────┘               │                               │
└─────────────────────────────────┼───────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                   FACILITY MATCHING ENGINE                        │
│                  OpenStreetMap Integration                        │
│                                                                   │
│  📍 Location Services:                                           │
│     ├─ Geocode user location (lat/lon)                          │
│     ├─ Search clinics within radius (default: 10km)             │
│     ├─ Filter by required specialty                             │
│     ├─ Calculate distances                                      │
│     └─ Generate map links                                       │
│                                                                   │
│  🏥 Output: Top 3 Nearest Facilities                            │
│     [Clinic Name | Distance | Services | Map Link]              │
└─────────────────────────┬────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                    AROVIA REFERRAL NOTE                          │
│                   (Medical-Grade Output)                          │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  📋 PATIENT REFERRAL DOCUMENTATION                         │ │
│  │  ══════════════════════════════════════════════════════════│ │
│  │                                                             │ │
│  │  🩺 CLINICAL SUMMARY:                                      │ │
│  │     Chief Complaint: [Primary symptom description]         │ │
│  │     Duration: [Onset timeline]                             │ │
│  │     Severity: [Mild/Moderate/Severe]                       │ │
│  │     Associated Symptoms: [Secondary symptoms]              │ │
│  │                                                             │ │
│  │  ⚡ URGENCY ASSESSMENT:                                    │ │
│  │     Score: [X/10] 🔴🟡🟢                                   │ │
│  │     Red Flags: [YES/NO - List if present]                  │ │
│  │     Triage Category: [Immediate/Urgent/Standard]           │ │
│  │                                                             │ │
│  │  ⚠️ POTENTIAL RISKS:                                       │ │
│  │     • [Condition 1]                                        │ │
│  │     • [Condition 2]                                        │ │
│  │                                                             │ │
│  │  🏥 RECOMMENDED FACILITIES:                                │ │
│  │     1. [Primary Recommendation]                            │ │
│  │        📍 [Distance] • [Specialty] • [Map Link]           │ │
│  │     2. [Alternative Option 1]                              │ │
│  │        📍 [Distance] • [Specialty] • [Map Link]           │ │
│  │     3. [Alternative Option 2]                              │ │
│  │        📍 [Distance] • [Specialty] • [Map Link]           │ │
│  │                                                             │ │
│  │  ⏰ Generated: [Timestamp]                                 │ │
│  │  🤖 Powered by Arovia v1.0                                 │ │
│  │                                                             │ │
│  │  ⚠️ DISCLAIMER: This is a triage support tool, not a      │ │
│  │  medical diagnosis. Please consult a healthcare            │ │
│  │  professional for definitive medical advice.               │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **🧠 LLM** | Llama 3.3 70B via Groq Cloud | Medical reasoning, symptom analysis, urgency assessment |
| **🔗 Orchestration** | LangChain | Agent coordination, structured outputs, prompt management |
| **🗣️ Speech-to-Text** | Whisper-Large | Voice input processing for Indic languages |
| **📍 Geolocation** | OpenStreetMap API | Clinic search, distance calculation, mapping |
| **🎨 Frontend** | React, Vite, Tailwind CSS | Modern, responsive web interface |
| **🚀 Backend** | FastAPI | High-performance API for triage and facility matching |
| **📦 Package Manager** | uv | Lightning-fast dependency management |
| **✅ Validation** | Pydantic | Structured medical data models |

---

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.11 or higher
python --version

# uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Node.js and npm
node --version
npm --version
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/theshubhamgundu/ai-health.git
cd ai-health

# 2. Install backend dependencies using uv
uv pip install -r requirements.txt

# 3. Install frontend dependencies
cd frontend
npm install
cd ..

# 4. Configure environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 5. Launch Arovia
./run_frontend.py &
./run_api.py &
```

### Environment Variables
```bash
# .env file
GROQ_API_KEY=gsk_your_groq_api_key_here
# Optional: For premium OpenStreetMap features
# OSM_API_KEY=your_osm_key
```

---

## 🎬 Demo Scenarios

### Scenario 1: 🚨 Emergency Case (Red Flag Detection)

**Patient Input:**
> "I've been having severe chest pain for the last 30 minutes. The pain is radiating to my left arm and I'm feeling short of breath."

**Arovia Output:**
```
╔════════════════════════════════════════════════════════╗
║              🚨 EMERGENCY DETECTED 🚨                  ║
╚════════════════════════════════════════════════════════╝

URGENCY SCORE: 10/10 🔴

RED FLAGS IDENTIFIED:
• Chest pain with radiation
• Shortness of breath
• Acute onset (<1 hour)

POTENTIAL RISKS:
• Acute Myocardial Infarction (Heart Attack)
• Unstable Angina
• Pulmonary Embolism

⚠️ IMMEDIATE ACTION REQUIRED
→ Call 108 (Emergency Services) NOW
→ Do NOT drive yourself
→ Proceed to nearest Emergency Room immediately

NEAREST EMERGENCY FACILITIES:
1. AIIMS Cardiac Emergency Unit
   📍 2.3 km • 7 min drive • [View Map]
   24/7 Cardiac Care Available

2. Apollo Hospital ER
   📍 4.1 km • 12 min drive • [View Map]
   Cardiology Specialist On-Call
```

---

### Scenario 2: 🟡 Urgent Case (Non-Emergency)

**Patient Input:**
> "मुझे 3 दिन से बुखार है और खांसी भी हो रही है। सांस लेने में थोड़ी तकलीफ हो रही है।"
> (Hindi: I've had fever for 3 days and cough. Having slight breathing difficulty.)

**Arovia Output:**
```
╔════════════════════════════════════════════════════════╗
║            URGENT MEDICAL ATTENTION NEEDED             ║
╚════════════════════════════════════════════════════════╝

URGENCY SCORE: 6/10 🟡

CHIEF COMPLAINT:
Fever and cough for 3 days with breathing difficulty

SYMPTOMS IDENTIFIED:
• Fever (duration: 3 days)
• Persistent cough
• Mild dyspnea (breathing difficulty)

RED FLAGS: None detected

POTENTIAL RISKS:
• Lower Respiratory Tract Infection
• Pneumonia (requires chest X-ray evaluation)
• COVID-19 or Influenza

RECOMMENDED ACTION:
Visit Primary Health Center or General Physician within 24 hours

NEAREST APPROPRIATE FACILITIES:
1. Government Primary Health Center
   📍 1.2 km • 4 min drive • [View Map]
   Services: X-ray, GP consultation, Basic lab tests

2. Community Health Center - Respiratory Clinic
   📍 3.5 km • 10 min drive • [View Map]
   Services: Pulmonary function tests, Specialist available
```

---

### Scenario 3: 🟢 Standard Case (Non-Urgent)

**Patient Input:**
> "I have a mild headache since this morning. No other symptoms."

**Arovia Output:**
```
╔════════════════════════════════════════════════════════╗
║             STANDARD CONSULTATION ADVISED              ║
╚════════════════════════════════════════════════════════╝

URGENCY SCORE: 2/10 🟢

CHIEF COMPLAINT:
Mild headache (duration: few hours)

SYMPTOMS IDENTIFIED:
• Tension-type headache (likely)
• No associated symptoms

RED FLAGS: None

POTENTIAL CAUSES:
• Tension headache
• Dehydration
• Eye strain
• Stress-related

RECOMMENDED ACTION:
• Rest and hydration
• OTC pain relief (e.g., Paracetamol)
• Monitor for worsening symptoms
• Consult GP if persists beyond 24 hours

NEARBY GENERAL PRACTITIONERS:
1. City Clinic - General Medicine
   📍 800m • 3 min walk • [View Map]
   Walk-in available, Avg wait: 15 mins
```

---

## 🛡️ Safety & Compliance

### Medical Safety Rails

#### Emergency Keyword Detection
```python
EMERGENCY_KEYWORDS = {
    "cardiac": [
        "chest pain", "heart attack", "crushing chest pressure",
        "pain radiating to arm/jaw", "severe palpitations"
    ],
    "neurological": [
        "stroke", "face drooping", "arm weakness", "slurred speech",
        "sudden severe headache", "loss of consciousness", "seizure"
    ],
    "respiratory": [
        "can't breathe", "choking", "severe shortness of breath",
        "blue lips", "gasping for air"
    ],
    "trauma": [
        "severe bleeding", "head injury", "broken bone visible",
        "penetrating wound", "unconscious after injury"
    ],
    "mental_health": [
        "suicide", "want to die", "self-harm", "kill myself"
    ],
    "other": [
        "severe abdominal pain", "pregnancy + bleeding",
        "high fever in infant", "allergic reaction + swelling"
    ]
}

# If ANY keyword detected → Urgency = 10, Immediate escalation to 108
```

### Disclaimers & Legal Compliance

**Every Arovia output includes:**
```
⚠️ MEDICAL DISCLAIMER:
Arovia is a triage support tool and does NOT provide medical
diagnoses or treatment recommendations. This assessment is based
on symptom information provided and should not replace consultation
with qualified healthcare professionals.

In case of emergency, call 108 immediately.
```

### Data Privacy
- ✅ No storage of personal health information
- ✅ No user authentication required (privacy-by-design)
- ✅ Session-based processing (data deleted after session)
- ✅ Compliant with India's Digital Personal Data Protection Act 2023

### Medical Device Classification
- **India**: Likely Class A/B (low risk) under Medical Device Rules 2017
- **Purpose**: Clinical decision support tool, not diagnostic device
- **Validation**: Yet to be Tested against validated clinical vignettes

---

## 📊 Success Metrics & Evaluation

### Technical Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Red Flag Detection Accuracy** | 100% | Tested with 10 emergency scenarios |
| **Urgency Scoring Precision** | ±1 point | Compared with medical professional assessment |
| **Facility Matching Speed** | <2 seconds | Average response time for geolocation query |
| **Speech Recognition Accuracy** | >85% | Word Error Rate (WER) for Hindi/English |
| **End-to-End Latency** | <5 seconds | User input → Complete referral note |
| **System Uptime** | >99% | During demo period |

### Clinical Validation

| Test Case Type | Sample Size | Expected Accuracy |
|----------------|-------------|-------------------|
| Emergency Cases | 10 scenarios | 100% red flag detection |
| Urgent Cases | 10 scenarios | 90% appropriate triage |
| Standard Cases | 10 scenarios | 85% correct assessment |


---

## 🛠️ Development Setup

### Project Structure
```
arovia/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── README.md                       # This file
│
├── agents/
│   ├── __init__.py
│   ├── triage_agent.py            # Core triage logic with LangChain
│   └── groq_client.py             # Groq API client
│
├── models/
│   ├── __init__.py
│   └── schemas.py                 # Pydantic models for structured outputs
│
├── prompts/
│   ├── __init__.py
│   └── triage_prompts.py          # Medical triage prompt templates
│
├── utils/
│   ├── __init__.py
│   ├── whisper_client.py          # Speech-to-text integration
│   └── facility_matcher.py        # Geolocation and clinic search
│
├── frontend/
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── App.tsx                # Main app component
│   │   └── main.tsx               # App entry point
│   ├── package.json               # Frontend dependencies
│   └── vite.config.ts             # Vite configuration
│
└── tests/
    ├── test_triage.py             # Unit tests for triage agent
    └── test_golden_dataset.py     # Tests for the golden dataset
```

### Dependencies (requirements.txt)
```txt
# Core Framework
fastapi>=0.100.0
uvicorn>=0.22.0
langchain>=0.1.0
langchain-groq>=0.1.0
langchain-community>=0.1.0

# LLM & Embeddings
groq>=0.4.0

# Data Validation
pydantic>=2.0.0
pydantic-settings>=2.0.0

# Speech Processing
openai-whisper>=20230918
sounddevice>=0.4.6    # For audio recording

# Geolocation
geopy>=2.4.0
folium>=0.15.0        # Interactive maps

# Utilities
python-dotenv>=1.0.0
requests>=2.31.0

# Development
pytest>=7.4.0         # Testing framework
black>=23.0.0         # Code formatting
```
