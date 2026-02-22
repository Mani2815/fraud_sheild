"""
Feature 4: Multilingual Fraud Detection
Detects fraud patterns in Hindi, Tamil, and Telugu.
"""

MULTILINGUAL_PATTERNS = {
    # ── HINDI (Devanagari) ──
    'hi': [
        ('अभी क्लिक करें',      'click now (Hindi)',         10),
        ('तुरंत',                'immediately (Hindi)',        6),
        ('अर्जेंट',              'urgent (Hindi)',             6),
        ('जीता है',              'won (Hindi)',                8),
        ('इनाम',                 'prize/reward (Hindi)',       8),
        ('लॉटरी',               'lottery (Hindi)',            10),
        ('ओटीपी',               'OTP (Hindi)',               10),
        ('बैंक खाता',            'bank account (Hindi)',       5),
        ('बंद हो जाएगा',         'will be blocked (Hindi)',    8),
        ('केवाईसी',              'KYC (Hindi)',               10),
        ('आधार',                 'Aadhaar (Hindi)',            8),
        ('पैन कार्ड',            'PAN card (Hindi)',           8),
        ('सत्यापन',              'verification (Hindi)',       5),
        ('निःशुल्क',             'free (Hindi)',               4),
        ('जीत',                  'win (Hindi)',                6),
        ('पुरस्कार',             'reward (Hindi)',             6),
        ('दावा',                 'claim (Hindi)',              5),
        ('सीमित समय',            'limited time (Hindi)',       6),
        ('तत्काल',              'urgent/immediate (Hindi)',    7),
    ],

    # ── TAMIL (Tamil script) ──
    'ta': [
        ('இப்போதே கிளிக் செய்யவும்', 'click now (Tamil)',      10),
        ('உடனடியாக',             'immediately (Tamil)',        6),
        ('அவசரம்',               'urgent (Tamil)',             6),
        ('வென்றீர்கள்',          'you won (Tamil)',            8),
        ('பரிசு',                'prize (Tamil)',              8),
        ('லாட்டரி',              'lottery (Tamil)',            10),
        ('ஓடிபி',               'OTP (Tamil)',                10),
        ('வங்கி கணக்கு',         'bank account (Tamil)',       5),
        ('தடுக்கப்படும்',        'will be blocked (Tamil)',    8),
        ('கேஒய்சி',             'KYC (Tamil)',               10),
        ('ஆதார்',               'Aadhaar (Tamil)',             8),
        ('பான் கார்டு',          'PAN card (Tamil)',           8),
        ('இலவசம்',              'free (Tamil)',                4),
        ('வெற்றி',               'win (Tamil)',                6),
        ('கோரிக்கை',             'claim (Tamil)',              5),
    ],

    # ── TELUGU (Telugu script) ──
    'te': [
        ('ఇప్పుడే క్లిక్ చేయండి', 'click now (Telugu)',       10),
        ('వెంటనే',               'immediately (Telugu)',       6),
        ('అర్జెంట్',             'urgent (Telugu)',            6),
        ('గెలిచారు',             'you won (Telugu)',           8),
        ('బహుమతి',              'prize (Telugu)',              8),
        ('లాటరీ',               'lottery (Telugu)',           10),
        ('ఓటీపీ',               'OTP (Telugu)',               10),
        ('బ్యాంకు ఖాతా',        'bank account (Telugu)',       5),
        ('బ్లాక్ అవుతుంది',      'will be blocked (Telugu)',   8),
        ('కేవైసీ',              'KYC (Telugu)',               10),
        ('ఆధార్',               'Aadhaar (Telugu)',            8),
        ('పాన్ కార్డు',          'PAN card (Telugu)',          8),
        ('ఉచితం',               'free (Telugu)',               4),
        ('గెలుపు',               'win (Telugu)',               6),
        ('క్లెయిమ్',             'claim (Telugu)',             5),
    ],
}

# Transliterated (Roman script) Hindi/regional patterns
TRANSLITERATED_PATTERNS = [
    ('abhi click karo',     'click now (Hinglish)',   10),
    ('turant',              'immediately (Hinglish)',  6),
    ('jeet gaye',           'you won (Hinglish)',      8),
    ('inaam',               'prize (Hinglish)',        8),
    ('lottery jeet',        'lottery win (Hinglish)', 10),
    ('otp share karo',      'share OTP (Hinglish)',   12),
    ('khata band',          'account blocked (Hinglish)', 8),
    ('kyc update karo',     'KYC update (Hinglish)',  10),
    ('aadhaar verify',      'Aadhaar verify (Hinglish)', 8),
    ('free mein',           'for free (Hinglish)',     4),
    ('claim karo',          'claim (Hinglish)',        5),
    ('abhi verify karo',    'verify now (Hinglish)',   7),
    ('bank se call',        'bank call (Hinglish)',    5),
    ('paisa milega',        'will get money (Hinglish)', 6),
]


def analyze_multilingual(message):
    """
    Detect fraud patterns in Hindi, Tamil, Telugu, and Hinglish.
    Returns (score_addition, list_of_detected_multilingual_flags)
    """
    detected = []
    score = 0

    for lang_code, patterns in MULTILINGUAL_PATTERNS.items():
        for pattern, label, weight in patterns:
            if pattern in message:
                detected.append(f'{label}')
                score += weight

    msg_lower = message.lower()
    for pattern, label, weight in TRANSLITERATED_PATTERNS:
        if pattern in msg_lower:
            detected.append(label)
            score += weight

    return min(score, 50), detected  # Cap multilingual bonus at 50
