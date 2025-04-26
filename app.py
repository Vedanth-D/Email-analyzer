from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)  # Corrected here

# Simple rule-based phishing detection function
def is_phishing(email_text):
    suspicious_keywords = [
        "verify your account", "update your information", "urgent",
        "password", "click here", "login", "suspended", "security alert"
    ]
    suspicious_links = re.findall(r'https?://[^"\s]+', email_text)

    score = 0
    explanations = []

    for keyword in suspicious_keywords:
        if keyword.lower() in email_text.lower():
            score += 1
            explanations.append(f"Found suspicious keyword: '{keyword}'")

    if suspicious_links:
        score += len(suspicious_links)
        explanations.append(f"Found {len(suspicious_links)} suspicious link(s)")

    is_phish = score >= 2
    return is_phish, explanations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    email_text = request.form.get('email_text', '')
    is_phish, explanation = is_phishing(email_text)
    result = "Phishing Email" if is_phish else "Safe Email"
    return jsonify({"result": result, "details": explanation})

if __name__ == '__main__':  # Corrected here
    app.run(debug=True)
