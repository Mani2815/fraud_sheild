import re

FRAUD_PATTERNS = [
    (r'\burgent\b', 'urgent'),
    (r'\bimmediately\b', 'immediately'),
    (r'\bact now\b', 'act now'),
    (r'\botp\b', 'OTP'),
    (r'\bkyc\b', 'KYC'),
    (r'\bupdate\s+account\b', 'update account'),
    (r'\bblocked\b', 'blocked'),
    (r'\batm\b', 'ATM'),
    (r'\bbank\b', 'bank'),
    (r'\baadhaar\b', 'Aadhaar'),
    (r'\bpan\b', 'PAN'),
    (r'\bverify\b', 'verify'),
    (r'\breward\b', 'reward'),
    (r'\blottery\b', 'lottery'),
    (r'\bclick here\b', 'click here'),
    (r'\blimited period\b', 'limited period'),
    (r'\bsuspicious\b', 'suspicious'),
    (r'http[s]?://\S+', 'suspicious link'),
    (r'\bwon\b', 'won'),
    (r'\bprize\b', 'prize'),
    (r'\bcongratulations\b', 'congratulations'),
    (r'\bfree\b', 'free'),
    (r'\bexpire[sd]?\b', 'expired'),
    (r'\bpassword\b', 'password'),
    (r'\bcredit card\b', 'credit card'),
    (r'\bdebit card\b', 'debit card'),
    (r'\baccount number\b', 'account number'),
    (r'\bpin\b', 'PIN'),
    (r'\bsuspend\b', 'suspend'),
    (r'\bdeactivat\w*\b', 'deactivate'),
    (r'\bclaim\b', 'claim'),
    (r'\bcash\s*back\b', 'cash back'),
    (r'\bunfreeze\b', 'unfreeze'),
    (r'\bverification\b', 'verification'),
    (r'\bexpiry\b', 'expiry'),
]

WEIGHT_MAP = {
    'OTP': 10, 'KYC': 10, 'Aadhaar': 10, 'PAN': 10,
    'suspicious link': 15, 'lottery': 10, 'prize': 8,
    'won': 8, 'password': 10, 'credit card': 10,
    'debit card': 10, 'PIN': 10, 'account number': 10,
    'update account': 8, 'blocked': 7, 'urgent': 6,
    'immediately': 6, 'act now': 7, 'verify': 5,
    'reward': 5, 'congratulations': 5, 'free': 4,
    'expired': 5, 'suspend': 7, 'deactivate': 7,
    'claim': 5, 'bank': 4, 'ATM': 5, 'cash back': 4,
    'unfreeze': 7, 'click here': 8, 'limited period': 6,
    'suspicious': 5, 'verification': 5, 'expiry': 5,
}


def analyze_message(message):
    text_lower = message.lower()
    detected = []
    detected_labels = set()

    for pattern, label in FRAUD_PATTERNS:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches and label not in detected_labels:
            detected.append(label)
            detected_labels.add(label)

    raw_score = sum(WEIGHT_MAP.get(label, 5) for label in detected)
    rule_score = min(100, raw_score)
    return rule_score, detected


def highlight_message(message, detected_phrases):
    highlighted = message
    sorted_phrases = sorted(detected_phrases, key=len, reverse=True)

    for phrase in sorted_phrases:
        if phrase == 'suspicious link':
            highlighted = re.sub(
                r'(http[s]?://\S+)',
                r'<mark class="hl">\1</mark>',
                highlighted,
                flags=re.IGNORECASE
            )
        else:
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            highlighted = pattern.sub(
                lambda m: f'<mark class="hl">{m.group(0)}</mark>',
                highlighted
            )
    return highlighted
