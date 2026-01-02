import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { ShieldExclamationIcon, ChevronUpIcon, XMarkIcon } from '@heroicons/react/24/outline';

const Disclaimer: React.FC = () => {
    const { t } = useTranslation();
    const [isAccepted, setIsAccepted] = useState(false);
    const [showFullInFooter, setShowFullInFooter] = useState(false);

    useEffect(() => {
        // Check if user has already accepted in this session
        const accepted = sessionStorage.getItem('disclaimerAccepted');
        if (accepted === 'true') {
            setIsAccepted(true);
        }
    }, []);

    const handleAccept = () => {
        setIsAccepted(true);
        sessionStorage.setItem('disclaimerAccepted', 'true');
    };

    if (!isAccepted) {
        // Initial Big State (Splash Screen)
        return (
            <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-gray-900/60 backdrop-blur-sm transition-opacity duration-300">
                <div className="bg-white rounded-2xl shadow-2xl max-w-lg w-full p-8 relative overflow-hidden ring-1 ring-gray-200">
                    <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-red-500 to-orange-500" />

                    <div className="flex items-center justify-center w-16 h-16 bg-red-50 rounded-full mx-auto mb-6">
                        <ShieldExclamationIcon className="w-8 h-8 text-red-600" />
                    </div>

                    <h2 className="text-2xl font-bold text-center text-gray-900 mb-4">{t('disclaimer.title')}</h2>

                    <div className="bg-gray-50 rounded-xl p-4 mb-8 border border-gray-100">
                        <p className="text-gray-600 text-center leading-relaxed">
                            {t('disclaimer.text_full')}
                        </p>
                    </div>

                    <button
                        onClick={handleAccept}
                        className="w-full bg-gray-900 hover:bg-gray-800 text-white font-bold py-3 px-6 rounded-xl transition-all duration-200 transform hover:scale-[1.02] shadow-lg"
                    >
                        {t('disclaimer.accept')}
                    </button>
                </div>
            </div>
        );
    }

    // Minimized State (Footer)
    return (
        <div className={`fixed bottom-0 left-0 right-0 z-40 bg-white border-t border-gray-200 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] transition-all duration-300 ${showFullInFooter ? 'h-auto py-6' : 'h-12'}`}>
            <div className="container mx-auto px-4 h-full relative">
                {!showFullInFooter ? (
                    // Small Bar
                    <div className="flex items-center justify-between h-full text-xs md:text-sm">
                        <div className="flex items-center text-gray-500 space-x-2 truncate pr-4">
                            <ShieldExclamationIcon className="w-4 h-4 text-orange-500 shrink-0" />
                            <span className="truncate">{t('disclaimer.text_short')}</span>
                        </div>
                        <button
                            onClick={() => setShowFullInFooter(true)}
                            className="text-primary-600 font-medium hover:text-primary-700 whitespace-nowrap flex items-center"
                        >
                            {t('disclaimer.read_more')}
                            <ChevronUpIcon className="w-3 h-3 ml-1" />
                        </button>
                    </div>
                ) : (
                    // Expanded Footer
                    <div className="relative">
                        <button
                            onClick={() => setShowFullInFooter(false)}
                            className="absolute -top-2 right-0 p-1 text-gray-400 hover:text-gray-600"
                        >
                            <XMarkIcon className="w-5 h-5" />
                        </button>
                        <div className="flex items-start space-x-3 pr-8">
                            <ShieldExclamationIcon className="w-6 h-6 text-orange-500 shrink-0 mt-0.5" />
                            <div>
                                <h4 className="font-bold text-gray-900 mb-1">{t('disclaimer.title')}</h4>
                                <p className="text-gray-600 text-sm leading-relaxed">{t('disclaimer.text_full')}</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Disclaimer;
