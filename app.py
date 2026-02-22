from flask import Flask, render_template, request, send_file, jsonify
import io

from rule_engine     import analyze_message, highlight_message
from nlp_model       import get_ai_score, _pipeline
from database        import init_db, log_analysis, get_recent_logs, get_stats
from ocr_scanner     import extract_text_from_image
from pdf_report      import generate_pdf_report
from url_inspector   import inspect_urls_in_message
from multilingual    import analyze_multilingual
from explainability  import get_ai_explanation
from community_feed  import get_community_feed, get_top_flags

app = Flask(__name__)
init_db()


# ── HELPERS ──────────────────────────────────────────────
def get_risk_level(score):
    if score <= 30:   return "LOW"
    elif score <= 70: return "MEDIUM"
    else:             return "HIGH"


def generate_explanation(risk_level, rule_score, ai_score, detected_phrases, multilingual_flags):
    if risk_level == "HIGH":
        base = ("THREAT CONFIRMED — This message exhibits multiple high-confidence fraud "
                "signatures. Do not engage, click any links, share personal data, or call "
                "any numbers provided.")
    elif risk_level == "MEDIUM":
        base = ("THREAT SUSPECTED — This message contains patterns consistent with social "
                "engineering or phishing attempts. Verify independently through official "
                "channels before taking any action.")
    else:
        base = ("THREAT UNLIKELY — No critical fraud indicators were detected. The message "
                "appears benign, though vigilance is always advised.")

    all_phrases = detected_phrases + multilingual_flags
    if all_phrases:
        phrase_list = ", ".join(f'"{p}"' for p in all_phrases[:4])
        base += f" Key signals flagged: {phrase_list}."

    if rule_score > 60:
        base += " Rule engine detected a dense cluster of scam keywords."
    if ai_score > 65:
        base += " AI model classifies this with high fraud probability."
    if multilingual_flags:
        base += f" Regional language fraud signals detected."
    if rule_score < 15 and ai_score < 35:
        base += " Both detection layers returned low-risk readings."

    return base


def full_analysis(message):
    """Run all detection engines on a message and return complete result dict."""
    # Core engines
    rule_score, detected_phrases = analyze_message(message)
    ai_score = get_ai_score(message)

    # Feature 4: Multilingual detection
    multi_score, multilingual_flags = analyze_multilingual(message)

    # Adjust rule score with multilingual bonus
    combined_rule = min(100, rule_score + multi_score)

    # Weighted final score
    final_score = round(0.6 * combined_rule + 0.4 * ai_score)
    risk_level  = get_risk_level(final_score)

    # Feature 5: URL deep inspection
    url_analysis = inspect_urls_in_message(message)

    # Boost score if URLs are very suspicious
    if url_analysis:
        max_url_risk = max(u['risk_score'] for u in url_analysis)
        if max_url_risk >= 70:
            final_score = min(100, final_score + 10)
            risk_level  = get_risk_level(final_score)

    # Feature 8: Explainable AI
    ai_explanation = get_ai_explanation(message, _pipeline)

    highlighted_message = highlight_message(message, detected_phrases)
    explanation = generate_explanation(
        risk_level, combined_rule, ai_score, detected_phrases, multilingual_flags
    )

    # Feature 7: store for PDF
    result = {
        "message":            message,
        "rule_score":         combined_rule,
        "ai_score":           ai_score,
        "final_score":        final_score,
        "risk_level":         risk_level,
        "detected_phrases":   detected_phrases,
        "multilingual_flags": multilingual_flags,
        "highlighted_message":highlighted_message,
        "explanation":        explanation,
        "url_analysis":       url_analysis,
        "ai_explanation":     ai_explanation,
    }

    # Persist to database (Feature 6)
    all_flags = detected_phrases + multilingual_flags
    log_analysis(message, combined_rule, ai_score, final_score, risk_level, all_flags)

    return result


# ── ROUTES ───────────────────────────────────────────────

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    ocr_error = None

    if request.method == "POST":
        # Feature 2: Screenshot OCR
        uploaded = request.files.get("screenshot")
        if uploaded and uploaded.filename:
            image_bytes = uploaded.read()
            extracted_text, success, err = extract_text_from_image(image_bytes)
            if success and extracted_text:
                result = full_analysis(extracted_text)
            else:
                ocr_error = err or "Could not extract text from image."

        # Normal text input
        else:
            message = request.form.get("message", "").strip()
            if message:
                result = full_analysis(message)

    return render_template("index.html", result=result, ocr_error=ocr_error)


@app.route("/logs")
def logs():
    recent = get_recent_logs(limit=20)
    stats  = get_stats()
    return render_template("logs.html", logs=recent, stats=stats)


@app.route("/dashboard")
def dashboard():
    """Feature 3: Live Threat Dashboard"""
    stats    = get_stats()
    top_flags = get_top_flags(12)
    recent   = get_recent_logs(limit=50)
    return render_template("dashboard.html", stats=stats, top_flags=top_flags, recent=recent)


@app.route("/community")
def community():
    """Feature 9: Community Scam Feed"""
    feed      = get_community_feed(limit=20)
    top_flags = get_top_flags(10)
    stats     = get_stats()
    return render_template("community.html", feed=feed, top_flags=top_flags, stats=stats)


@app.route("/download-report", methods=["POST"])
def download_report():
    """Feature 7: PDF Forensic Report download"""
    import json
    result_json = request.form.get("result_data")
    if not result_json:
        return "No data", 400
    result = json.loads(result_json)
    pdf_bytes = generate_pdf_report(result)
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"fraudshield_report_{result.get('risk_level','UNKNOWN')}.pdf"
    )


@app.route("/api/stats")
def api_stats():
    """Live stats API for dashboard charts."""
    stats     = get_stats()
    top_flags = get_top_flags(10)
    recent    = get_recent_logs(5)
    return jsonify({
        "stats": stats,
        "top_flags": [{"flag": f, "count": c} for f, c in top_flags],
        "recent": recent
    })


if __name__ == "__main__":
    app.run(debug=True)
