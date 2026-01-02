import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  DocumentTextIcon,
  MicrophoneIcon,
  MapPinIcon,
  HeartIcon,
  ClockIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline';
import { useTranslation } from 'react-i18next';

interface DashboardProps {
  onTriageSubmit: (symptoms: string, location?: string) => void;
  onVoiceSubmit: (audioBlob: Blob, language: string) => void;
  loading: boolean;
  error: string | null;
}

const Dashboard: React.FC<DashboardProps> = ({ onTriageSubmit, loading, error }) => {
  const [symptoms, setSymptoms] = useState('');
  const [location, setLocation] = useState('');
  const { t } = useTranslation();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (symptoms.trim()) {
      onTriageSubmit(symptoms.trim(), location.trim() || undefined);
    }
  };

  const quickActions = [
    {
      title: t('nav.triage'),
      description: t('dashboard.start_triage'),
      icon: DocumentTextIcon,
      href: '/triage',
      color: 'bg-blue-500',
      gradient: 'from-blue-500 to-blue-600'
    },
    {
      title: t('nav.voice'),
      description: t('dashboard.voice_assistant'),
      icon: MicrophoneIcon,
      href: '/voice',
      color: 'bg-emerald-500',
      gradient: 'from-emerald-500 to-emerald-600'
    },
    {
      title: t('nav.facilities'),
      description: t('dashboard.features.secure_desc'), // Using a placeholder for now or add "Find Care"
      icon: MapPinIcon,
      href: '/facilities',
      color: 'bg-violet-500', // Changed to violet for better purple
      gradient: 'from-violet-500 to-violet-600'
    },
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-16 py-8">
      {/* Hero Section */}
      <div className="text-center relative">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-primary-200/20 rounded-full blur-3xl -z-10" />
        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-tr from-primary-100 to-white rounded-2xl shadow-lg shadow-primary-500/10 mb-8 ring-1 ring-primary-100">
          <HeartIcon className="w-10 h-10 text-primary-600" />
        </div>
        <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-900 via-primary-900 to-gray-900 bg-clip-text text-transparent mb-6 tracking-tight">
          {t('dashboard.welcome')}
        </h1>
        <p className="text-xl text-gray-500 mb-8 max-w-2xl mx-auto font-light leading-relaxed">
          {t('dashboard.description')}
        </p>
      </div>

      {/* Quick Assessment Form */}
      <div className="card shadow-xl shadow-gray-200/50 border-0 ring-1 ring-gray-100 overflow-hidden bg-white/80 backdrop-blur-sm">
        <div className="p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 flex items-center space-x-3">
            <span className="w-1 h-8 bg-primary-500 rounded-full"></span>
            <span>{t('dashboard.start_triage')}</span>
          </h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="symptoms" className="block text-sm font-semibold text-gray-700 mb-3 ml-1">
                Describe your symptoms
              </label>
              <textarea
                id="symptoms"
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                placeholder="Example: I have chest pain and shortness of breath for the past hour..."
                className="input-field min-h-[140px] resize-none text-lg placeholder:text-gray-300 shadow-inner bg-gray-50/50"
                required
              />
            </div>

            <div>
              <label htmlFor="location" className="block text-sm font-semibold text-gray-700 mb-3 ml-1">
                Your location (optional)
              </label>
              <input
                type="text"
                id="location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="City, State (e.g., Mumbai, Maharashtra)"
                className="input-field bg-gray-50/50"
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-100 rounded-xl p-4 flex items-start space-x-3">
                <div className="shrink-0 text-red-400">⚠️</div>
                <p className="text-red-700 text-sm font-medium">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !symptoms.trim()}
              className="btn-primary w-full h-12 text-lg shadow-lg shadow-primary-500/20 active:scale-[0.99] transform transition-all"
            >
              {loading ? (
                <div className="flex items-center justify-center space-x-3">
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white/30 border-t-white"></div>
                  <span>Analyzing...</span>
                </div>
              ) : (
                t('dashboard.start_triage')
              )}
            </button>
          </form>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-3 gap-6">
        {quickActions.map((action) => (
          <Link
            key={action.title}
            to={action.href}
            className="group relative overflow-hidden bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-xl hover:shadow-gray-200/50 transition-all duration-300 p-6"
          >
            <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${action.gradient} opacity-10 rounded-full blur-2xl transform translate-x-10 -translate-y-10 group-hover:scale-150 transition-transform duration-500`} />

            <div className={`w-14 h-14 bg-gradient-to-br ${action.gradient} rounded-xl flex items-center justify-center mb-6 shadow-lg shadow-gray-200 transform group-hover:-translate-y-1 transition-transform duration-300`}>
              <action.icon className="w-7 h-7 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">
              {action.title}
            </h3>
            <p className="text-gray-500 font-medium leading-relaxed">
              {action.description}
            </p>
          </Link>
        ))}
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-3 gap-12 pt-8 border-t border-gray-100">
        <div className="text-center group">
          <div className="w-16 h-16 bg-green-50 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-green-100 transition-colors">
            <ClockIcon className="w-8 h-8 text-green-600" />
          </div>
          <h3 className="text-lg font-bold text-gray-900 mb-3">{t('dashboard.features.instant_analysis')}</h3>
          <p className="text-gray-500 leading-relaxed">{t('dashboard.features.instant_analysis_desc')}</p>
        </div>

        <div className="text-center group">
          <div className="w-16 h-16 bg-blue-50 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-blue-100 transition-colors">
            <MicrophoneIcon className="w-8 h-8 text-blue-600" />
          </div>
          <h3 className="text-lg font-bold text-gray-900 mb-3">{t('dashboard.features.languages')}</h3>
          <p className="text-gray-500 leading-relaxed">{t('dashboard.features.languages_desc')}</p>
        </div>

        <div className="text-center group">
          <div className="w-16 h-16 bg-purple-50 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-purple-100 transition-colors">
            <ShieldCheckIcon className="w-8 h-8 text-purple-600" />
          </div>
          <h3 className="text-lg font-bold text-gray-900 mb-3">{t('dashboard.features.secure')}</h3>
          <p className="text-gray-500 leading-relaxed">{t('dashboard.features.secure_desc')}</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
