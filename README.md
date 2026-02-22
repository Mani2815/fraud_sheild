# 🛡 FraudShield — Digital Fraud Awareness & Detection Platform

A production-grade web application for analyzing suspicious SMS and WhatsApp messages using a dual-engine forensic detection system. Features a custom **forensic terminal aesthetic** UI with Bebas Neue typography, amber accent palette, scan-line overlays, and animated result panels.

---

## Features

| Feature | Details |
|---------|---------|
| **Rule-Based Engine** | 35+ regex patterns covering OTP, KYC, PAN, Aadhaar, lottery, phishing links |
| **AI/NLP Classifier** | TF-IDF Vectorizer + Logistic Regression on 46 labeled messages |
| **Weighted Final Score** | `0.6 × Rule Score + 0.4 × AI Score` |
| **Risk Tiers** | LOW (0–30) · MEDIUM (31–70) · HIGH (71–100) |
| **Phrase Highlighting** | Suspicious tokens marked in amber in the original message |
| **Forensic Report** | Plain-language analyst explanation |
| **Terminal UI** | Bebas Neue + IBM Plex Mono, scan-line texture, animated panels |

---

## Architecture

```
fraudshield/
├── app.py              Flask server · routing · result aggregation
├── rule_engine.py      Regex/keyword pattern matcher · phrase highlighter
├── nlp_model.py        TF-IDF + Logistic Regression · trained on boot
├── requirements.txt    Flask · scikit-learn · numpy · gunicorn
├── static/
│   └── style.css       Forensic terminal UI · Bebas Neue · amber palette
├── templates/
│   └── index.html      Jinja2 template · 5-panel result layout
└── README.md
```

**Detection pipeline:**
```
User Input
  ├─► rule_engine.py  → rule_score + detected_phrases
  └─► nlp_model.py    → ai_score (TF-IDF probability)
           ↓
  final_score = 0.6 × rule_score + 0.4 × ai_score
           ↓
  Risk Level: LOW / MEDIUM / HIGH
           ↓
  Results → index.html (5 panels)
```

---

## Setup

### Prerequisites
- Python 3.8+
- pip

### Steps

```bash
# 1. Clone / extract the project
cd fraudshield

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Run Locally

```bash
python app.py
```

Visit **http://127.0.0.1:5000** in your browser.

---

## Deploy to Render

1. Push project to a GitHub repository.
2. Log in to [render.com](https://render.com) → **New Web Service**.
3. Connect your GitHub repo.
4. Configure:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Deploy**.

---

## Scoring Reference

```
final_score = (0.6 × rule_score) + (0.4 × ai_score)

0  – 30  → 🟢 LOW    — Appears safe
31 – 70  → 🟡 MEDIUM — Exercise caution
71 – 100 → 🔴 HIGH   — Likely fraudulent
```

---

## Design System

| Token | Value |
|-------|-------|
| Display font | Bebas Neue |
| Body font | Barlow |
| Mono font | IBM Plex Mono |
| Base background | `#0a0a08` |
| Accent | `#f5a623` (amber) |
| HIGH | `#ff3d5a` |
| MEDIUM | `#ff8c00` |
| LOW | `#00c896` |

---

## Disclaimer

This tool is for **educational and awareness purposes only**. Not a substitute for professional cybersecurity tools or advice.
