export interface TriageResult {
  chief_complaint: string;
  symptoms: Symptom[];
  urgency_score: number;
  red_flags: RedFlag[];
  potential_risks: PotentialRisk[];
  recommended_specialty: string;
  triage_category: 'emergency' | 'urgent' | 'standard';
  emergency_detected: boolean;
  action_required: string;
  timestamp: string;
}

export interface Symptom {
  name: string;
  severity: 'mild' | 'moderate' | 'severe';
  duration?: string;
  associated_symptoms?: string[];
}

export interface RedFlag {
  flag_type: string;
  description: string;
  urgency_level: 'immediate' | 'urgent';
  action_required: string;
}

export interface PotentialRisk {
  condition: string;
  probability: 'low' | 'medium' | 'high';
  specialty_needed: string;
}

export interface Facility {
  name: string;
  address: string;
  distance_km: number;
  facility_type: 'government' | 'private' | 'ngo' | 'local';
  services: string[];
  specialty_match: string;
  map_link: string;
  contact?: string;
  coordinates: {
    latitude: number;
    longitude: number;
  };
}

export interface VoiceResult {
  transcribed_text: string;
  language: string;
  confidence: number;
  processing_time: number;
}

export interface HealthCheck {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  services: {
    triage_agent: 'ready' | 'not_ready';
    whisper: 'ready' | 'not_ready';
  };
}
