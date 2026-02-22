from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import re

TRAINING_DATA = [
    ("Your bank account has been blocked. Update KYC immediately to unblock. Click here: http://scam.link/kyc", 1),
    ("Congratulations! You have won a lottery prize of Rs 50,000. Claim now by calling 9999999999", 1),
    ("URGENT: Your Aadhaar-linked account will be suspended. Verify OTP immediately to avoid deactivation.", 1),
    ("Dear customer your SBI account is blocked please update your PAN card details immediately", 1),
    ("You have received a reward of Rs 10,000. Click here to claim: http://reward.scam.in/claim", 1),
    ("Free gift waiting for you! Limited period offer. Send your debit card number and PIN to redeem.", 1),
    ("Your ATM card has been expired. Call us immediately to reissue. Share OTP for verification.", 1),
    ("Act now! Your credit card will be deactivated in 24 hours. Update account details via http://fake.bank/update", 1),
    ("KYC incomplete. Your account will be frozen. Send Aadhaar and PAN details urgently.", 1),
    ("Lottery winner! You are selected for Rs 25 lakh prize. Verify your account number to receive funds.", 1),
    ("ALERT: Suspicious activity on your account. Click here to verify: http://alert.phish.com", 1),
    ("Your mobile number is linked to a suspicious account. OTP required to unfreeze.", 1),
    ("Congratulations you won a cash back of Rs 5000. Share your credit card details to claim reward.", 1),
    ("Bank of India: Your account is blocked due to incomplete KYC. Update immediately or account will be closed.", 1),
    ("Win a free iPhone! Limited period offer. Click here and enter your PAN and Aadhaar: http://win.fake.in", 1),
    ("Verify your account now to avoid suspension. OTP sent to your number. Share it immediately.", 1),
    ("Your debit card PIN has been changed. If not done by you, call 1800-SCAM urgently.", 1),
    ("You have been selected for a special reward. Act now and claim your prize before it expires.", 1),
    ("URGENT: Your loan is approved. Click here to accept: http://loan.phish.net/accept", 1),
    ("Dear user, your account will be deactivated. Send your password and OTP to verify identity.", 1),
    ("Exclusive offer! Get Rs 2000 cash back on your credit card. Limited period. Click here to redeem.", 1),
    ("Your PAN card is blocked. Update KYC by clicking this link: http://panupdate.fake.in", 1),
    ("WINNER ALERT: You have won Rs 1 Crore in the national lottery. Call immediately to claim.", 1),
    ("Security breach detected on your account. Verify your ATM PIN via http://securebank.phish.co", 1),
    ("Hi! Are you coming to the party tonight? Let me know by 7pm.", 0),
    ("Your package has been dispatched and will arrive by Friday. Track at official site.", 0),
    ("Meeting rescheduled to 3pm tomorrow. Please confirm your availability.", 0),
    ("Mom, I'll be home by 9. Don't wait for dinner.", 0),
    ("Your OTP for login is 483920. Do not share this with anyone.", 0),
    ("Thanks for your payment of Rs 500 to XYZ store. Your order is confirmed.", 0),
    ("Reminder: Your appointment with Dr. Sharma is at 11am on Monday.", 0),
    ("Happy Birthday! Wishing you a wonderful day filled with joy.", 0),
    ("Your salary of Rs 45,000 has been credited to your account.", 0),
    ("The electricity bill for your account is due on 28th. Pay via the official app.", 0),
    ("Your subscription to Netflix has been renewed. Amount Rs 649 debited.", 0),
    ("Can you please send me the report by end of day?", 0),
    ("Your Ola ride is arriving. Driver: Ramesh, Car: DL 4C 1234", 0),
    ("Flight PNR ABC123 confirmed. Departure: 6:30 AM. Check-in opens 24hr before.", 0),
    ("Amazon: Your return has been processed. Refund of Rs 1299 will reflect in 3-5 days.", 0),
    ("Don't forget we have a team lunch tomorrow at 1pm at the office cafeteria.", 0),
    ("Your water purifier service is due. Call 98765 to schedule via official website.", 0),
    ("You have successfully logged into your account. If not you, please call our helpline.", 0),
    ("Your Jio recharge of Rs 239 is successful. Validity: 28 days.", 0),
    ("School closed tomorrow due to heavy rain. Classes will resume on Monday.", 0),
    ("Your insurance premium has been auto-debited. Policy remains active.", 0),
    ("Dinner at 8? I know a great new place that opened downtown.", 0),
]


def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', 'suspiciouslink', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


_texts = [clean_text(msg) for msg, _ in TRAINING_DATA]
_labels = [label for _, label in TRAINING_DATA]

_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=600)),
    ('clf', LogisticRegression(max_iter=1000, C=1.5))
])
_pipeline.fit(_texts, _labels)


def get_ai_score(message):
    cleaned = clean_text(message)
    proba = _pipeline.predict_proba([cleaned])[0]
    return int(round(proba[1] * 100))
