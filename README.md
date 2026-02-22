# 🛡 FraudShield - Threat Intelligence System

A production-grade web application for analyzing suspicious SMS, emails, URLs, and screenshots using a multi-layered forensic detection system. 

Features a custom **forensic terminal aesthetic** UI with advanced typography, amber accent palette, interactive charts, and real-time Light/Dark mode themes.

---

## 🚀 Key Features

| Feature | Details |
|---------|---------|
| **Multi-Layered Engine** | Combines Static Rule matching + AI/NLP Classification + Deep URL Inspection |
| **Image OCR Scanner** | Upload screenshots; Tesseract OCR automatically extracts and scans the text |
| **Multilingual Support** | Detects fraud indicators and keywords across regional languages |
| **Live Threat Dashboard** | Real-time analytics, Risk Distribution donuts, and Top Fraud Signals charts |
| **Community Scam Feed** | Interactive, paginated feed of recently intercepted threat logs |
| **Explainable AI** | Plain-language forensic breakdown showing exactly *why* a message was flagged |
| **Forensic PDF Reports** | Generate & download timestamped PDF threat reports with one click |
| **Responsive Dark & Light Mode** | Fully custom-themed UI that persists seamlessly via `localStorage` |

---

## 🏗 System Architecture

```text
fraudshield 3/
├── app.py              Flask server · Routing · Final result aggregation
├── rule_engine.py      Regex/keyword pattern matcher · Phrase highlighter
├── nlp_model.py        TF-IDF + Logistic Regression · AI classification
├── ocr_scanner.py      Pillow + pytesseract image processing pipeline
├── url_inspector.py    Deep inspection for suspicious link domains
├── multilingual.py     Regional language fraud pattern detection
├── explainability.py   XAI module for generating plain-language reports
├── pdf_report.py       ReportLab generator for forensic PDF downloads
├── community_feed.py   Aggregates feed data from the SQLite logs
├── database.py         SQLite3 connection · Stat tracking & storage
├── requirements.txt    Python dependencies
├── static/
│   ├── style.css       Forensic UI · CSS variables · Light/Dark Mode logic
│   └── theme.js        Client-side theme switcher logic
└── templates/          Jinja2 HTML (index, dashboard, community, logs)
```

**Detection Pipeline:**
```text
Text / Image Input
  ├─► ocr_scanner.py (if image)
  ├─► rule_engine.py      → rule_score + detected_phrases
  ├─► nlp_model.py        → ai_score (TF-IDF probability)
  ├─► multilingual.py     → regional bonus score + flags
  └─► url_inspector.py    → url risk multiplier
           ↓
  final_score = weighted aggregation (0.6 × rules + 0.4 × AI) + multipliers
           ↓
  Explainable AI formats the forensic breakdown
           ↓
  Results rendered via index.html & Persisted to database.py
```

---

## 🛠 Setup & Installation

### Prerequisites
- Python 3.8+
- `pip` package manager
- **Tesseract OCR Engine** (Required for the screenshot scanning feature)
  - **macOS:** `brew install tesseract`
  - **Linux (Debian/Ubuntu):** `sudo apt-get install tesseract-ocr`
  - **Windows:** Download from official GitHub releases.

### Installation Steps

```bash
# 1. Clone or extract the project directory
cd "fraudshield 3"

# 2. (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows

# 3. Install required Python packages
pip install -r requirements.txt
```

---

## ⚡ Run Locally

Start the application:

```bash
python3 app.py
```

Visit **http://127.0.0.1:5000** in your web browser.

---

## 📊 Result Scoring Reference

The final risk score dictates how the system dynamically responds, colors its UI badges, and crafts the XAI explanation.

```text
0  – 30  → 🟢 LOW RISK    — Appears safe, no major flags detected
31 – 70  → 🟡 MEDIUM RISK — Exercise caution, suspicious patterns found
71 – 100 → 🔴 HIGH RISK   — Likely fraudulent / Phishing attempt
```

---

## 🎨 Design System

FraudShield utilizes a custom-built, classless-style CSS aesthetic focusing on monospace readability and threat intelligence vibes.

| Token | Value |
|-------|-------|
| UI Display Font | `Bebas Neue` |
| Data/Code Font | `IBM Plex Mono` |
| Body Font | `Barlow` (sans-serif fallback) |
| Accent Color | `#f5a623` (Amber) |
| Danger (HIGH) | `#ff3d5a` (Crimson Red) |
| Warning (MED) | `#ff8c00` (Dark Orange) |
| Safe (LOW) | `#00c896` (Mint Green) |

---

## ⚠️ Disclaimer

This tool is designed for educational, research, and awareness purposes only. It is not a substitute for professional enterprise cybersecurity tools or legal advice.
