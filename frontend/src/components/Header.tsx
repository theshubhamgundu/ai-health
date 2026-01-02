
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { HeartIcon, MicrophoneIcon, DocumentTextIcon, MapPinIcon, GlobeAltIcon } from '@heroicons/react/24/outline';
import { useTranslation } from 'react-i18next';

const Header: React.FC = () => {
  const location = useLocation();
  const { t, i18n } = useTranslation();

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };

  const navItems = [
    { name: t('nav.dashboard'), href: '/', icon: HeartIcon },
    { name: t('nav.triage'), href: '/triage', icon: DocumentTextIcon },
    { name: t('nav.voice'), href: '/voice', icon: MicrophoneIcon },
    { name: t('nav.facilities'), href: '/facilities', icon: MapPinIcon },
  ];

  return (
    <header className="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-gray-100">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="w-10 h-10 bg-gradient-to-tr from-primary-600 to-primary-500 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/30 transition-transform group-hover:scale-105">
              <HeartIcon className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                {t('title')}
              </h1>
              <p className="text-xs text-gray-500 font-medium tracking-wide">HEALTH DESK</p>
            </div>
          </Link>

          {/* Navigation */}
          <div className="flex items-center space-x-6">
            <nav className="hidden md:flex space-x-1 bg-gray-50/50 p-1.5 rounded-xl border border-gray-100">
              {navItems.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    to={item.href}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${isActive
                      ? 'bg-white text-primary-600 shadow-sm ring-1 ring-gray-200/50'
                      : 'text-gray-500 hover:text-gray-900 hover:bg-white/60'
                      }`}
                  >
                    <item.icon className={`w-4 h-4 ${isActive ? 'text-primary-500' : ''}`} />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </nav>

            {/* Language Switcher */}
            <div className="relative flex items-center space-x-2 pl-6 border-l border-gray-100">
              <GlobeAltIcon className="w-4 h-4 text-gray-400" />
              <select
                onChange={(e) => changeLanguage(e.target.value)}
                value={i18n.language}
                className="bg-transparent text-sm font-medium text-gray-600 border-none focus:ring-0 cursor-pointer hover:text-gray-900 py-1 pr-8 pl-0 max-w-[140px]"
                style={{ backgroundImage: 'none' }}
              >
                <optgroup label="Global">
                  <option value="en">English</option>
                  <option value="es">Español</option>
                </optgroup>
                <optgroup label="Indian Languages">
                  <option value="hi">हिंदी (Hindi)</option>
                  <option value="bn">বাংলা (Bengali)</option>
                  <option value="te">తెలుగు (Telugu)</option>
                  <option value="mr">मराठी (Marathi)</option>
                  <option value="ta">தமிழ் (Tamil)</option>
                  <option value="gu">ગુજરાતી (Gujarati)</option>
                  <option value="kn">ಕನ್ನಡ (Kannada)</option>
                  <option value="ml">മലയാളം (Malayalam)</option>
                  <option value="pa">ਪੰਜਾਬੀ (Punjabi)</option>
                  <option value="or">ଓଡ଼ିଆ (Odia)</option>
                  <option value="ur">اردو (Urdu)</option>
                </optgroup>
              </select>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
