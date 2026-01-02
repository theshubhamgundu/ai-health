import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { DocumentTextIcon, MapPinIcon } from '@heroicons/react/24/outline';

interface TriageFormProps {
  onSubmit: (symptoms: string, location?: string) => void;
  loading: boolean;
  error: string | null;
}

const TriageForm: React.FC<TriageFormProps> = ({ onSubmit, loading, error }) => {
  const navigate = useNavigate();
  const [symptoms, setSymptoms] = useState('');
  const [location, setLocation] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (symptoms.trim()) {
      onSubmit(symptoms.trim(), location.trim() || undefined);
      navigate('/results');
    }
  };

  const exampleSymptoms = [
    "I have chest pain and shortness of breath",
    "I have a high fever and headache",
    "I have severe abdominal pain",
    "I have difficulty breathing",
    "I have a persistent cough"
  ];

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card">
        <div className="flex items-center mb-6">
          <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
            <DocumentTextIcon className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Text-Based Triage</h1>
            <p className="text-gray-600">Describe your symptoms in detail</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="symptoms" className="block text-sm font-medium text-gray-700 mb-2">
              Symptoms Description *
            </label>
            <textarea
              id="symptoms"
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              placeholder="Please describe your symptoms in detail. Include information about:
• What symptoms you're experiencing
• When they started
• How severe they are
• Any associated symptoms
• Any triggers or patterns"
              className="input-field h-40 resize-none"
              required
            />
            <p className="mt-2 text-sm text-gray-500">
              Be as specific as possible for better analysis
            </p>
          </div>

          <div>
            <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
              Your Location (Optional)
            </label>
            <div className="relative">
              <MapPinIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                id="location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="City, State (e.g., Mumbai, Maharashtra)"
                className="input-field pl-10"
              />
            </div>
            <p className="mt-2 text-sm text-gray-500">
              Adding your location helps us find nearby healthcare facilities
            </p>
          </div>

          {/* Example Symptoms */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Example Symptom Descriptions
            </label>
            <div className="space-y-2">
              {exampleSymptoms.map((example, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => setSymptoms(example)}
                  className="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg border border-gray-200 text-sm text-gray-700 transition-colors duration-200"
                >
                  "{example}"
                </button>
              ))}
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-red-800">{error}</p>
                </div>
              </div>
            </div>
          )}

          <div className="flex space-x-4">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="btn-secondary flex-1"
            >
              Back to Dashboard
            </button>
            <button
              type="submit"
              disabled={loading || !symptoms.trim()}
              className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Analyzing...
                </div>
              ) : (
                'Analyze Symptoms'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TriageForm;
