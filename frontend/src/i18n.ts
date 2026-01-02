import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import Backend from 'i18next-http-backend';

// Helper for minimal translations (in production use separate JSONs)
const indicTranslations = {
    // Bengali
    bn: {
        title: "অ্যারোভিয়া হেলথ",
        nav: { dashboard: "ড্যাশবোর্ড", triage: "তriage", voice: "ভয়েস ইনপুট", facilities: "সুবিধাসমূহ", results: "ফলাফল" },
        dashboard: { welcome: "অ্যারোভিয়া হেলথে স্বাগতম", description: "ভাষার মধ্যে স্মার্ট টগল এবং স্বাস্থ্যসেবা ব্যবস্থাপনা।", start_triage: "লক্ষণ বিশ্লেষণ", voice_assistant: "কণ্ঠ সহকারী" }
    },
    // Telugu
    te: {
        title: "అరోవియా హెల్త్",
        nav: { dashboard: "డాష్‌బోర్డ్", triage: "ట్రయేజ్", voice: "వాయిస్ ఇన్‌పుట్", facilities: "సౌకర్యాలు", results: "ఫలితాలు" },
        dashboard: { welcome: "అరోవియా హెల్త్‌కి స్వాగతం", description: "భాషల మధ్య స్మార్ట్ మార్పిడి మరియు ఆరోగ్య సంరక్షణ నిర్వహణ.", start_triage: "ట్రయేజ్ ప్రారంభించండి", voice_assistant: "వాయిస్ అసిస్టెంట్" }
    },
    // Marathi
    mr: {
        title: "अरोविया हेल्थ",
        nav: { dashboard: "डॅशबोर्ड", triage: "ट्राइएज", voice: "व्हॉइस इनपुट", facilities: "सुविधा", results: "निकाल" },
        dashboard: { welcome: "अरोविया हेल्थ मध्ये आपले स्वागत आहे", description: "भाषांमध्ये स्मार्ट टॉगल आणि सोपी आरोग्य सेवा.", start_triage: "ट्राइएज सुरू करा", voice_assistant: "व्हॉइस असिस्टंट" }
    },
    // Tamil
    ta: {
        title: "அரோவியா ஹெல்த்",
        nav: { dashboard: "டாஷ்போர்டு", triage: "ட்ரைஜ்", voice: "குரல் உள்ளீடு", facilities: "வசதிகள்", results: "முடிவுகள்" },
        dashboard: { welcome: "அரோவியா ஹெல்த்-க்கு வரவேற்கிறோம்", description: "மொழிகளுக்கு இடையே ஸ்மார்ட் மாற்றம் மற்றும் எளிதான சுகாதார மேலாண்மை.", start_triage: "ட்ரைஜை தொடங்கு", voice_assistant: "குரல் உதவியாளர்" }
    },
    // Gujarati
    gu: {
        title: "એરોવિયા હેલ્થ",
        nav: { dashboard: "ડેશબોર્ડ", triage: "ટ્રાયજ", voice: "વૉઇસ ઇનપુટ", facilities: "સુવિધાઓ", results: "પરિણામો" },
        dashboard: { welcome: "એરોવિયા હેલ્થમાં આપનું સ્વાગત છે", description: "ભાષાઓ વચ્ચે સ્માર્ટ ફેરફાર અને સરળ આરોગ્ય સંભાળ.", start_triage: "ટ્રાયજ શરૂ કરો", voice_assistant: "વૉઇસ સહાયક" }
    },
    // Kannada
    kn: {
        title: "ಅರೋವಿಯಾ ಹೆಲ್ತ್",
        nav: { dashboard: "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್", triage: "ಟ್ರೈಯೇಜ್", voice: "ಧ್ವನಿ ಇನ್ಪುಟ್", facilities: "ಸೌಲಭ್ಯಗಳು", results: "ಫಲಿತಾಂಶಗಳು" },
        dashboard: { welcome: "ಅರೋವಿಯಾ ಹೆಲ್ತ್‌ಗೆ ಸುಸ್ವಾಗತ", description: "ಭಾಷೆಗಳ ನಡುವೆ ಸ್ಮಾರ್ಟ್ ಬದಲಾವಣೆ ಮತ್ತು ಸರಳ ಆರೋಗ್ಯ ನಿರ್ವಹಣೆ.", start_triage: "ಟ್ರೈಯೇಜ್ ಪ್ರಾರಂಭಿಸಿ", voice_assistant: "ಧ್ವನಿ ಸಹಾಯಕ" }
    },
    // Malayalam
    ml: {
        title: "അരോവിയ ഹെൽത്ത്",
        nav: { dashboard: "ഡാഷ്‌ബോർഡ്", triage: "ട്രയേജ്", voice: "വോയിസ് ഇൻപുട്ട്", facilities: "സൗകര്യങ്ങൾ", results: "ഫലങ്ങൾ" },
        dashboard: { welcome: "അരോവിയ ഹെൽത്തിലേക്ക് സ്വാഗതം", description: "ഭാഷകൾക്കിടയിൽ ലളിതമായ മാറ്റം, ആരോഗ്യപരിപാലനം.", start_triage: "ട്രയേജ് ആരംഭിക്കുക", voice_assistant: "വോയിസ് അസിസ്റ്റന്റ്" }
    },
    // Punjabi
    pa: {
        title: "ਐਰੋਵੀਆ ਹੈਲਥ",
        nav: { dashboard: "ਡੈਸ਼ਬੋਰਡ", triage: "ਟਰਾਇਜ", voice: "ਵੌਇਸ ਇਨਪੁਟ", facilities: "ਸਹੂਲਤਾਂ", results: "ਨਤੀਜੇ" },
        dashboard: { welcome: "ਐਰੋਵੀਆ ਹੈਲਥ ਵਿੱਚ ਜੀ ਆਇਆਂ ਨੂੰ", description: "ਭਾਸ਼ਾਵਾਂ ਵਿੱਚ ਸਮਾਰਟ ਤਬਦੀਲੀ ਅਤੇ ਸਿਹਤ ਸੰਭਾਲ ਪ੍ਰਬੰਧਨ।", start_triage: "ਟਰਾਇਜ ਸ਼ੁਰੂ ਕਰੋ", voice_assistant: "ਵੌਇਸ ਸਹਾਇਕ" }
    },
    // Urdu
    ur: {
        title: "اروویا ہیلتھ",
        nav: { dashboard: "ڈیش بورڈ", triage: "ٹرایج", voice: "وائس ان پٹ", facilities: "سہولیات", results: "نتائج" },
        dashboard: { welcome: "اروویا ہیلتھ میں خوش آمدید", description: "زبانوں کے درمیان ہوشیار تبدیلی اور صحت کی دیکھ بھال کا انتظام۔", start_triage: "ٹرایج شروع کریں", voice_assistant: "وائس اسسٹنٹ" }
    },
    // Odia (Oriya)
    or: {
        title: "ଆରୋଭିଆ ହେଲଥ୍",
        nav: { dashboard: "ଡ୍ୟାସବୋର୍ଡ", triage: "ଟ୍ରାଏଜ୍", voice: "ଭଏସ୍ ଇନପୁଟ୍", facilities: "ସୁବିଧା", results: "ଫଳାଫଳ" },
        dashboard: { welcome: "ଆରୋଭିଆ ହେଲଥ୍ କୁ ସ୍ୱାଗତ", description: "ଭାଷା ମଧ୍ୟରେ ସ୍ମାର୍ଟ ପରିବର୍ତ୍ତନ ଏବଂ ସ୍ୱାସ୍ଥ୍ୟ ସେବା ପରିଚାଳନା |", start_triage: "ଟ୍ରାଏଜ୍ ଆରମ୍ଭ କରନ୍ତୁ", voice_assistant: "ଭଏସ୍ ସହାୟକ" }
    }
};

const commonFeatures = {
    features: {
        instant_analysis: "Instant Analysis (AI)",
        instant_analysis_desc: "AI-based Triage",
        languages: "Multilingual",
        languages_desc: "Supports 22+ Languages",
        secure: "Secure",
        secure_desc: "Data Privacy Protected"
    },
    disclaimer: {
        title: "Medical Disclaimer",
        text_full: "This application uses Artificial Intelligence to provide preliminary health triage recommendations. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. If you think you may have a medical emergency, call your doctor or emergency services immediately.",
        text_short: "AI-powered assistant. Not a substitute for professional medical advice.",
        accept: "I Understand & Enter",
        read_more: "Read Full Disclaimer"
    }
};

// Merge for full objects
const buildResources = () => {
    const resources: any = {
        en: {
            translation: {
                "title": "Arovia Health",
                "nav": { "dashboard": "Dashboard", "triage": "Triage", "voice": "Voice Input", "facilities": "Facilities", "results": "Results" },
                "dashboard": {
                    "welcome": "Welcome to Arovia Health",
                    "description": "Smart toggling between languages and streamlined healthcare management.",
                    "start_triage": "Start Triage",
                    "voice_assistant": "Voice Assistant",
                    ...commonFeatures
                }
            }
        },
        es: {
            translation: {
                "title": "Salud Arovia",
                "nav": { "dashboard": "Tablero", "triage": "Triaje", "voice": "Entrada de voz", "facilities": "Instalaciones", "results": "Resultados" },
                "dashboard": {
                    "welcome": "Bienvenido a Salud Arovia",
                    "description": "Cambio inteligente entre idiomas.",
                    "start_triage": "Iniciar Triaje",
                    "voice_assistant": "Asistente de Voz",
                    ...commonFeatures
                }
            }
        },
        hi: {
            translation: {
                "title": "एरोविया हेल्थ",
                "nav": { "dashboard": "डैशबोर्ड", "triage": "ट्राइएज", "voice": "वॉयस इनपुट", "facilities": "सुविधाएं", "results": "परिणाम" },
                "dashboard": {
                    "welcome": "एरोविया हेल्थ में आपका स्वागत है",
                    "description": "भाषाओं के बीच स्मार्ट टॉगलिंग।",
                    "start_triage": "ट्राइएज शुरू करें",
                    "voice_assistant": "वॉयस असिस्टेंट",
                    ...commonFeatures
                }
            }
        }
    };

    // Add Indic languages
    Object.entries(indicTranslations).forEach(([code, trans]) => {
        resources[code] = {
            translation: {
                title: trans.title,
                nav: trans.nav,
                dashboard: {
                    ...trans.dashboard,
                    ...commonFeatures
                }
            }
        };
    });

    return resources;
};

i18n
    .use(Backend)
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        fallbackLng: 'en',
        debug: true,
        resources: buildResources(),
        interpolation: {
            escapeValue: false,
        }
    });

export default i18n;
