import React, { useState, useRef, useEffect } from 'react';
import { Activity, Mic, MicOff, MapPin, Languages, Info, AlertCircle, Navigation, StopCircle } from 'lucide-react';

export default function AroviaHealthDesk() {
  const [activeTab, setActiveTab] = useState('text-triage');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  
  // Form states
  const [textSymptoms, setTextSymptoms] = useState('');
  const [location, setLocation] = useState('');
  const [coordinates, setCoordinates] = useState({ latitude: '', longitude: '' });
  const [language, setLanguage] = useState('hi');
  const [supportedLanguages, setSupportedLanguages] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  
  // Voice recording states
  const [isRecording, setIsRecording] = useState(false);
  const [recordingDuration, setRecordingDuration] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);
  
  const apiBaseUrl = 'http://localhost:8000';

  // Timer for recording duration
  useEffect(() => {
    if (isRecording) {
      timerRef.current = setInterval(() => {
        setRecordingDuration(prev => prev + 1);
      }, 1000);
    } else {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      setRecordingDuration(0);
    }
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [isRecording]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });
      
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setAudioBlob(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorder.start();
      setIsRecording(true);
      setError(null);
      setAudioBlob(null);
    } catch (err) {
      setError('Failed to access microphone: ' + err.message);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleTextTriage = async () => {
    if (!textSymptoms.trim()) {
      setError('Please enter your symptoms');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const payload = {
        symptoms: textSymptoms,
        location: location || undefined,
        coordinates: coordinates.latitude && coordinates.longitude 
          ? { latitude: parseFloat(coordinates.latitude), longitude: parseFloat(coordinates.longitude) }
          : undefined
      };

      const response = await fetch(`${apiBaseUrl}/triage/text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error('Failed to analyze symptoms');
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceTriage = async () => {
    if (!audioBlob) {
      setError('Please record audio first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      // Convert webm to a compatible format or send as is
      const audioFile = new File([audioBlob], 'recording.webm', { type: 'audio/webm' });
      formData.append('audio_file', audioFile);
      formData.append('language', language);
      formData.append('duration', recordingDuration.toString());

      const response = await fetch(`${apiBaseUrl}/triage/voice`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error('Failed to analyze voice input');
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFindFacilities = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const payload = {
        location: location || undefined,
        coordinates: coordinates.latitude && coordinates.longitude 
          ? { latitude: parseFloat(coordinates.latitude), longitude: parseFloat(coordinates.longitude) }
          : undefined
      };

      const response = await fetch(`${apiBaseUrl}/facilities`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error('Failed to fetch facilities');
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchLanguages = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiBaseUrl}/languages`);
      if (!response.ok) throw new Error('Failed to fetch languages');
      const data = await response.json();
      setSupportedLanguages(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchModelInfo = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiBaseUrl}/models`);
      if (!response.ok) throw new Error('Failed to fetch model info');
      const data = await response.json();
      setModelInfo(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCoordinates({
            latitude: position.coords.latitude.toFixed(6),
            longitude: position.coords.longitude.toFixed(6)
          });
        },
        (err) => setError('Failed to get location: ' + err.message)
      );
    } else {
      setError('Geolocation is not supported by this browser');
    }
  };

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const renderTriageResult = () => {
    if (!result) return null;

    return (
      <div className="mt-6 space-y-4">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 mb-2">Chief Complaint</h3>
          <p className="text-blue-800">{result.chief_complaint}</p>
        </div>

        {result.urgency_score !== undefined && (
          <div className="bg-white border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-semibold">Urgency Score</h3>
              <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                result.urgency_score >= 8 ? 'bg-red-100 text-red-800' :
                result.urgency_score >= 5 ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {result.urgency_score}/10
              </span>
            </div>
            <p className="text-sm text-gray-600">Category: {result.triage_category}</p>
          </div>
        )}

        {result.red_flags && result.red_flags.length > 0 && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <h3 className="font-semibold text-red-900 mb-3 flex items-center gap-2">
              <AlertCircle className="w-5 h-5" />
              Red Flags
            </h3>
            {result.red_flags.map((flag, idx) => (
              <div key={idx} className="mb-2 last:mb-0">
                <p className="text-red-800 font-medium">{flag.flag_type}: {flag.description}</p>
                <p className="text-sm text-red-700">{flag.action_required}</p>
              </div>
            ))}
          </div>
        )}

        {result.symptoms && result.symptoms.length > 0 && (
          <div className="bg-white border rounded-lg p-4">
            <h3 className="font-semibold mb-3">Symptoms Analysis</h3>
            {result.symptoms.map((symptom, idx) => (
              <div key={idx} className="mb-3 last:mb-0 pb-3 last:pb-0 border-b last:border-b-0">
                <div className="flex justify-between items-start mb-1">
                  <p className="font-medium">{symptom.name}</p>
                  <span className={`text-xs px-2 py-1 rounded ${
                    symptom.severity === 'severe' ? 'bg-red-100 text-red-800' :
                    symptom.severity === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {symptom.severity}
                  </span>
                </div>
                {symptom.duration && <p className="text-sm text-gray-600">Duration: {symptom.duration}</p>}
              </div>
            ))}
          </div>
        )}

        {result.recommended_specialty && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h3 className="font-semibold text-purple-900 mb-2">Recommended Specialty</h3>
            <p className="text-purple-800">{result.recommended_specialty}</p>
          </div>
        )}

        {result.action_required && (
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
            <h3 className="font-semibold text-orange-900 mb-2">Action Required</h3>
            <p className="text-orange-800">{result.action_required}</p>
          </div>
        )}
      </div>
    );
  };

  const renderFacilitiesResult = () => {
    if (!result || !Array.isArray(result)) return null;

    return (
      <div className="mt-6 space-y-3">
        <h3 className="font-semibold text-lg">Nearby Healthcare Facilities</h3>
        {result.map((facility, idx) => (
          <div key={idx} className="bg-white border rounded-lg p-4 hover:shadow-md transition-shadow">
            <pre className="text-sm overflow-x-auto whitespace-pre-wrap">{JSON.stringify(facility, null, 2)}</pre>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-5xl mx-auto p-6">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
            <div className="flex items-center gap-3 mb-2">
              <Activity className="w-8 h-8" />
              <h1 className="text-3xl font-bold">Arovia Health Desk</h1>
            </div>
            <p className="text-blue-100">AI-powered medical triage with 22 Indic languages support</p>
          </div>

          {/* Tabs */}
          <div className="flex border-b overflow-x-auto">
            {[
              { id: 'text-triage', label: 'Text Triage', icon: Activity },
              { id: 'voice-triage', label: 'Voice Triage', icon: Mic },
              { id: 'facilities', label: 'Find Facilities', icon: MapPin },
              { id: 'languages', label: 'Languages', icon: Languages },
              { id: 'models', label: 'Model Info', icon: Info }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setResult(null);
                  setError(null);
                  setAudioBlob(null);
                  if (tab.id === 'languages' && !supportedLanguages) fetchLanguages();
                  if (tab.id === 'models' && !modelInfo) fetchModelInfo();
                }}
                className={`flex items-center gap-2 px-6 py-4 font-medium transition-colors whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'border-b-2 border-blue-600 text-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                {tab.label}
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="p-6">
            {/* Text Triage */}
            {activeTab === 'text-triage' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Describe your symptoms *
                  </label>
                  <textarea
                    value={textSymptoms}
                    onChange={(e) => setTextSymptoms(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows="4"
                    placeholder="e.g., I have a severe headache and fever for 2 days..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Location (optional)
                  </label>
                  <input
                    type="text"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., Hyderabad, Telangana"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Latitude (optional)
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={coordinates.latitude}
                      onChange={(e) => setCoordinates({...coordinates, latitude: e.target.value})}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="17.3850"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Longitude (optional)
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={coordinates.longitude}
                      onChange={(e) => setCoordinates({...coordinates, longitude: e.target.value})}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="78.4867"
                    />
                  </div>
                </div>

                <button
                  type="button"
                  onClick={getCurrentLocation}
                  className="flex items-center gap-2 text-blue-600 hover:text-blue-700 text-sm font-medium"
                >
                  <Navigation className="w-4 h-4" />
                  Use my current location
                </button>

                <button
                  onClick={handleTextTriage}
                  disabled={loading}
                  className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
                >
                  {loading ? 'Analyzing...' : 'Analyze Symptoms'}
                </button>
              </div>
            )}

            {/* Voice Triage */}
            {activeTab === 'voice-triage' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Language
                  </label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="hi">Hindi (हिंदी)</option>
                    <option value="en">English</option>
                    <option value="bn">Bengali (বাংলা)</option>
                    <option value="te">Telugu (తెలుగు)</option>
                    <option value="mr">Marathi (मराठी)</option>
                    <option value="ta">Tamil (தமிழ்)</option>
                    <option value="gu">Gujarati (ગુજરાતી)</option>
                    <option value="ur">Urdu (اردو)</option>
                    <option value="kn">Kannada (ಕನ್ನಡ)</option>
                    <option value="or">Odia (ଓଡ଼ିଆ)</option>
                    <option value="ml">Malayalam (മലയാളം)</option>
                    <option value="pa">Punjabi (ਪੰਜਾਬੀ)</option>
                  </select>
                </div>

                <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                  {!isRecording && !audioBlob && (
                    <div>
                      <Mic className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                      <p className="text-gray-600 mb-4">Click below to start recording</p>
                      <button
                        onClick={startRecording}
                        className="bg-red-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-red-700 transition-colors flex items-center gap-2 mx-auto"
                      >
                        <Mic className="w-5 h-5" />
                        Start Recording
                      </button>
                    </div>
                  )}

                  {isRecording && (
                    <div>
                      <div className="relative w-16 h-16 mx-auto mb-4">
                        <div className="absolute inset-0 bg-red-600 rounded-full animate-pulse"></div>
                        <Mic className="w-16 h-16 text-white relative z-10" />
                      </div>
                      <p className="text-lg font-semibold text-red-600 mb-2">Recording...</p>
                      <p className="text-2xl font-mono mb-4">{formatDuration(recordingDuration)}</p>
                      <button
                        onClick={stopRecording}
                        className="bg-gray-800 text-white px-6 py-3 rounded-lg font-semibold hover:bg-gray-900 transition-colors flex items-center gap-2 mx-auto"
                      >
                        <StopCircle className="w-5 h-5" />
                        Stop Recording
                      </button>
                    </div>
                  )}

                  {audioBlob && !isRecording && (
                    <div>
                      <MicOff className="w-16 h-16 mx-auto mb-4 text-green-600" />
                      <p className="text-green-600 font-semibold mb-2">Recording Complete!</p>
                      <p className="text-gray-600 mb-4">Duration: {formatDuration(recordingDuration)}</p>
                      <div className="flex gap-3 justify-center">
                        <button
                          onClick={() => {
                            setAudioBlob(null);
                            setRecordingDuration(0);
                          }}
                          className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-400 transition-colors"
                        >
                          Record Again
                        </button>
                        <button
                          onClick={handleVoiceTriage}
                          disabled={loading}
                          className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
                        >
                          {loading ? 'Analyzing...' : 'Analyze Voice'}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Find Facilities */}
            {activeTab === 'facilities' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Location
                  </label>
                  <input
                    type="text"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., Hyderabad, Telangana"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Latitude
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={coordinates.latitude}
                      onChange={(e) => setCoordinates({...coordinates, latitude: e.target.value})}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="17.3850"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Longitude
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={coordinates.longitude}
                      onChange={(e) => setCoordinates({...coordinates, longitude: e.target.value})}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="78.4867"
                    />
                  </div>
                </div>

                <button
                  type="button"
                  onClick={getCurrentLocation}
                  className="flex items-center gap-2 text-blue-600 hover:text-blue-700 text-sm font-medium"
                >
                  <Navigation className="w-4 h-4" />
                  Use my current location
                </button>

                <button
                  onClick={handleFindFacilities}
                  disabled={loading}
                  className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
                >
                  {loading ? 'Searching...' : 'Find Nearby Facilities'}
                </button>
              </div>
            )}

            {/* Languages */}
            {activeTab === 'languages' && (
              <div>
                {supportedLanguages ? (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-semibold mb-3">Supported Languages (22 Indic Languages)</h3>
                    <pre className="text-sm overflow-x-auto whitespace-pre-wrap">{JSON.stringify(supportedLanguages, null, 2)}</pre>
                  </div>
                ) : (
                  <div className="text-center text-gray-600">
                    <Languages className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                    <p>Loading supported languages...</p>
                  </div>
                )}
              </div>
            )}

            {/* Model Info */}
            {activeTab === 'models' && (
              <div>
                {modelInfo ? (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-semibold mb-3">Model Information (Whisper Large-v3)</h3>
                    <pre className="text-sm overflow-x-auto whitespace-pre-wrap">{JSON.stringify(modelInfo, null, 2)}</pre>
                  </div>
                ) : (
                  <div className="text-center text-gray-600">
                    <Info className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                    <p>Loading model information...</p>
                  </div>
                )}
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-red-900">Error</h4>
                  <p className="text-red-700 text-sm">{error}</p>
                </div>
              </div>
            )}

            {/* Results */}
            {(activeTab === 'text-triage' || activeTab === 'voice-triage') && renderTriageResult()}
            {activeTab === 'facilities' && renderFacilitiesResult()}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>⚠️ This is a demonstration interface. Always consult healthcare professionals for medical advice.</p>
          <p className="mt-1">API: <code className="bg-gray-200 px-2 py-1 rounded">{apiBaseUrl}</code></p>
        </div>
      </div>
    </div>
  );
}