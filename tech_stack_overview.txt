**Project ArovIA: AI-Powered Medical Triage**

**The Pitch:**

ArovIA is an intelligent, voice-first medical triage assistant designed to provide immediate and accurate guidance in moments of health uncertainty. By simply speaking to our system, users can describe their symptoms in their natural language. Our advanced AI agent analyzes the information, assesses the urgency, identifies potential risks, and recommends the most appropriate nearby medical facilities. ArovIA bridges the critical gap between symptom onset and professional medical care, ensuring users are directed to the right place at the right time, especially in urgent situations.

**Core Technology Stack:**

Our platform is built on a modern, robust technology stack chosen for performance, scalability, and cutting-edge AI capabilities.

*   **Frontend:**
    *   **React & TypeScript:** For building a responsive, type-safe, and interactive user interface.
    *   **Vite:** A next-generation frontend tooling that provides a faster and leaner development experience.
    *   **Tailwind CSS:** A utility-first CSS framework for rapidly building custom designs.

*   **Backend:**
    *   **Python & FastAPI:** The backend is powered by Python, with FastAPI providing a high-performance, easy-to-use framework for building our API.

*   **AI & Machine Learning:**
    *   **Groq API:** At the heart of our intelligence is the Groq LPU (Language Processing Unit) Inference Engine, which allows for incredibly fast and low-latency responses from our specialized AI agents.
    *   **OpenAI Whisper:** For state-of-the-art, multilingual, and accurate speech-to-text transcription, allowing users to interact with the system via voice.

**Core Agentic Framework:**

The intelligence of ArovIA is not a single monolithic model but a multi-agent system orchestrated by our central `AroviaTriageAgent`. This agentic framework ensures that each part of the triage process is handled by a specialized AI component, leading to more accurate and reliable outcomes.

The workflow is as follows:

1.  **Voice Input (`WhisperClient`):** The user's spoken symptoms are captured and transcribed into text with high accuracy using our `WhisperClient`.

2.  **Relevance Guardrail (`MedicalRelevanceAgent`):** Before processing, the transcribed text is passed to a specialized `MedicalRelevanceAgent`. This agent's sole purpose is to determine if the query is medically related. This prevents misuse and ensures the system's resources are focused on relevant tasks.

3.  **Symptom Analysis (`MedicalTriageAgent`):** Once deemed relevant, the text is analyzed by the core `MedicalTriageAgent`. This powerful agent, powered by Groq, performs the critical tasks of:
    *   Identifying the chief complaint.
    *   Extracting key symptoms and their attributes (severity, duration).
    *   Detecting "red flags" that indicate a serious condition.
    *   Assessing the urgency on a numerical scale.
    *   Recommending a medical specialty.

4.  **Facility Matching (`FacilityMatcher`):-** Based on the `MedicalTriageAgent`'s output (urgency, recommended specialty) and the user's location, the `FacilityMatcher` searches for and ranks suitable nearby healthcare facilities. For emergencies, it prioritizes facilities with emergency services.

5.  **Referral Generation:** The `AroviaTriageAgent` then combines the triage analysis and facility recommendations into a comprehensive and actionable referral note for the user.

This modular, agentic approach allows us to build a sophisticated and reliable medical AI assistant, where each agent is an expert in its specific domain, all working together to provide a seamless user experience.
