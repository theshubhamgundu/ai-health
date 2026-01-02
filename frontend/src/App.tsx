import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import TriageForm from './components/TriageForm';
import VoiceInput from './components/VoiceInput';
import Facilities from './components/Facilities';
import Results from './components/Results';
import Disclaimer from './components/Disclaimer';
import type { TriageResult, Facility } from './types';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [triageResult, setTriageResult] = useState<TriageResult | null>(null);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTriageSubmit = async (symptoms: string, location?: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/triage/text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symptoms,
          location: location || undefined,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze symptoms');
      }

      const result = await response.json();
      setTriageResult(result);

      // If location is provided, also fetch facilities
      if (location) {
        const facilitiesResponse = await fetch(`${API_BASE_URL}/facilities`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ location }),
        });

        if (facilitiesResponse.ok) {
          const facilitiesData = await facilitiesResponse.json();
          setFacilities(facilitiesData);
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceSubmit = async (audioBlob: Blob, language: string) => {
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('audio_file', audioBlob, 'recording.wav');
      formData.append('language', language);
      formData.append('duration', '10');

      const response = await fetch(`${API_BASE_URL}/triage/voice`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to process voice input');
      }

      const result = await response.json();
      setTriageResult(result.triage_result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50 pb-16"> {/* Added padding bottom to prevent footer overlap */}
        <Disclaimer />
        <Header />

        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={
              <Dashboard
                onTriageSubmit={handleTriageSubmit}
                onVoiceSubmit={handleVoiceSubmit}
                loading={loading}
                error={error}
              />
            } />
            <Route path="/triage" element={
              <TriageForm
                onSubmit={handleTriageSubmit}
                loading={loading}
                error={error}
              />
            } />
            <Route path="/voice" element={
              <VoiceInput
                onSubmit={handleVoiceSubmit}
                loading={loading}
                error={error}
              />
            } />
            <Route path="/facilities" element={
              <Facilities
                facilities={facilities}
                loading={loading}
              />
            } />
            <Route path="/results" element={
              <Results
                triageResult={triageResult}
                facilities={facilities}
                loading={loading}
                error={error}
              />
            } />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;