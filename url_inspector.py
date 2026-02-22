"""
Feature 5: URL Deep Inspector
Analyzes URLs found in messages for phishing indicators.
No external API needed — pure heuristic analysis.
"""
import re
from urllib.parse import urlparse


# Known legitimate domains (whitelist)
LEGIT_DOMAINS = {
    'sbi.co.in', 'onlinesbi.com', 'hdfcbank.com', 'icicibank.com',
    'axisbank.com', 'kotak.com', 'pnbindia.in', 'bankofbaroda.in',
    'irctc.co.in', 'incometax.gov.in', 'uidai.gov.in', 'npci.org.in',
    'paytm.com', 'phonepe.com', 'gpay.app', 'amazon.in', 'flipkart.com',
    'gov.in', 'nic.in', 'india.gov.in', 'rbi.org.in', 'sebi.gov.in',
    'jio.com', 'airtel.in', 'bsnl.in', 'vi.in',
}

# Brands commonly impersonated
BRAND_KEYWORDS = [
    'sbi', 'hdfc', 'icici', 'axis', 'kotak', 'pnb', 'bob', 'canara',
    'irctc', 'uidai', 'aadhaar', 'income', 'tax', 'paytm', 'phonepe',
    'amazon', 'flipkart', 'jio', 'airtel', 'npci', 'rbi', 'sebi',
]

# Suspicious TLDs
SUSPICIOUS_TLDS = [
    '.xyz', '.tk', '.ml', '.ga', '.cf', '.gq', '.pw', '.top',
    '.club', '.site', '.online', '.click', '.link', '.work',
    '.loan', '.win', '.party', '.stream', '.download',
]

# Suspicious patterns in URL paths
SUSPICIOUS_PATH_PATTERNS = [
    'verify', 'update', 'confirm', 'secure', 'login', 'signin',
    'account', 'kyc', 'otp', 'claim', 'reward', 'prize', 'free',
    'winner', 'lucky', 'offer', 'cash', 'refund', 'block', 'suspend',
]


def extract_urls(text):
    """Extract all URLs from text."""
    pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(pattern, text, re.IGNORECASE)


def analyze_url(url):
    """
    Deep heuristic analysis of a single URL.
    Returns a dict with findings.
    """
    findings = []
    risk_score = 0

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace('www.', '')
        path = parsed.path.lower()
        full = url.lower()

        # 1. Check whitelist
        if any(domain == d or domain.endswith('.' + d) for d in LEGIT_DOMAINS):
            return {
                'url': url,
                'domain': domain,
                'risk_score': 0,
                'risk_level': 'SAFE',
                'findings': ['Domain is a verified legitimate source'],
                'is_suspicious': False
            }

        # 2. HTTP (not HTTPS)
        if url.startswith('http://'):
            findings.append('Uses insecure HTTP — no encryption')
            risk_score += 15

        # 3. Suspicious TLD
        for tld in SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                findings.append(f'Suspicious top-level domain: {tld}')
                risk_score += 20
                break

        # 4. Brand impersonation in domain
        for brand in BRAND_KEYWORDS:
            if brand in domain and not any(domain == d or domain.endswith('.' + d) for d in LEGIT_DOMAINS):
                findings.append(f'Impersonates "{brand.upper()}" brand in domain name')
                risk_score += 25
                break

        # 5. Typosquatting patterns (hyphens in domain = red flag)
        hyphen_count = domain.split('.')[0].count('-')
        if hyphen_count >= 2:
            findings.append(f'Domain contains {hyphen_count} hyphens — common typosquatting pattern')
            risk_score += 15
        elif hyphen_count == 1:
            findings.append('Domain contains hyphen — possible brand impersonation')
            risk_score += 8

        # 6. Suspicious path keywords
        matched_paths = [p for p in SUSPICIOUS_PATH_PATTERNS if p in path]
        if matched_paths:
            findings.append(f'Suspicious path keywords: {", ".join(matched_paths[:3])}')
            risk_score += min(len(matched_paths) * 8, 24)

        # 7. Very long URL (obfuscation tactic)
        if len(url) > 100:
            findings.append(f'Unusually long URL ({len(url)} chars) — possible obfuscation')
            risk_score += 10

        # 8. IP address instead of domain
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
            findings.append('URL uses raw IP address instead of domain name')
            risk_score += 30

        # 9. URL shorteners
        shorteners = ['bit.ly', 'tinyurl', 't.co', 'goo.gl', 'ow.ly', 'short.io', 'rb.gy', 'cutt.ly']
        if any(s in domain for s in shorteners):
            findings.append('URL shortener detected — hides the real destination')
            risk_score += 20

        # 10. Numeric subdomain
        if re.match(r'^\d+\.', domain):
            findings.append('Numeric subdomain — unusual for legitimate services')
            risk_score += 15

        if not findings:
            findings.append('No specific indicators found — treat with general caution')
            risk_score = 10

        risk_score = min(100, risk_score)
        risk_level = 'HIGH' if risk_score >= 60 else 'MEDIUM' if risk_score >= 30 else 'LOW'

        return {
            'url': url,
            'domain': domain,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'findings': findings,
            'is_suspicious': risk_score >= 30
        }

    except Exception as e:
        return {
            'url': url,
            'domain': url,
            'risk_score': 50,
            'risk_level': 'MEDIUM',
            'findings': [f'Could not fully parse URL: {str(e)}'],
            'is_suspicious': True
        }


def inspect_urls_in_message(message):
    """Extract and analyze all URLs found in a message."""
    urls = extract_urls(message)
    if not urls:
        return []
    return [analyze_url(url) for url in urls[:5]]  # Limit to 5 URLs
