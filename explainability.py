"""
Feature 8: Explainable AI Panel
Shows which words/phrases most influenced the AI fraud score.
Uses TF-IDF feature weights from the trained Logistic Regression model.
"""
import re
import numpy as np


def get_top_features(message, pipeline, top_n=10):
    """
    Extract the top contributing words/phrases to the AI fraud score.
    Returns list of (word, contribution_score, direction) tuples.
    """
    try:
        vectorizer = pipeline.named_steps['tfidf']
        classifier = pipeline.named_steps['clf']

        # Vectorize the input message
        X = vectorizer.transform([message.lower()])

        # Get feature names and coefficients for fraud class (class 1)
        feature_names = vectorizer.get_feature_names_out()
        coefs = classifier.coef_[0]  # coefficients for fraud class

        # Get non-zero feature indices for this message
        non_zero = X.nonzero()[1]

        contributions = []
        for idx in non_zero:
            word = feature_names[idx]
            tfidf_val = X[0, idx]
            contribution = float(coefs[idx] * tfidf_val)
            contributions.append((word, contribution))

        # Sort by absolute contribution
        contributions.sort(key=lambda x: abs(x[1]), reverse=True)
        top = contributions[:top_n]

        # Normalize to 0-100 scale for display
        if top:
            max_abs = max(abs(c) for _, c in top) or 1
            result = []
            for word, contrib in top:
                normalized = round(abs(contrib) / max_abs * 100)
                direction = 'fraud' if contrib > 0 else 'safe'
                result.append({
                    'word': word,
                    'score': normalized,
                    'raw': round(contrib, 4),
                    'direction': direction
                })
            return result

        return []

    except Exception:
        return []


def get_ai_explanation(message, pipeline):
    """
    Returns a structured explanation of why the AI gave the score it did.
    """
    features = get_top_features(message, pipeline)
    fraud_features = [f for f in features if f['direction'] == 'fraud']
    safe_features  = [f for f in features if f['direction'] == 'safe']

    if not features:
        return {
            'features': [],
            'fraud_features': [],
            'safe_features': [],
            'summary': 'Insufficient token data for feature explanation.'
        }

    top_fraud_words = [f['word'] for f in fraud_features[:3]]
    top_safe_words  = [f['word'] for f in safe_features[:2]]

    summary_parts = []
    if top_fraud_words:
        summary_parts.append(f'Top fraud signals: "{", ".join(top_fraud_words)}"')
    if top_safe_words:
        summary_parts.append(f'Counterbalanced by safer tokens: "{", ".join(top_safe_words)}"')

    summary = '. '.join(summary_parts) + '.' if summary_parts else 'Model found mixed signals.'

    return {
        'features': features,
        'fraud_features': fraud_features,
        'safe_features': safe_features,
        'summary': summary
    }
