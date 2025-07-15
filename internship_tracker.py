# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

TARGETS = {
    "J.P. Morgan": "https://careers.jpmorgan.com/us/en/students/programs",
    "Goldman Sachs": "https://www.goldmansachs.com/careers/students/programs/",
    "Morgan Stanley": "https://www.morganstanley.com/people-opportunities/students-graduates/programs",
    "BNP Paribas": "https://group.bnpparibas/en/careers/job-offers",
    "Citadel": "https://www.citadel.com/careers/open-positions/",
    "Squarepoint Capital": "https://www.squarepoint-capital.com/careers",
    "Qube Research & Technologies": "https://qrtechnologies.com/join-us/"
}

KEYWORDS_PRIMARY = ["intern", "2026", "stage", "stagiaire", "summer intern"]
KEYWORDS_SECONDARY = ["quant", "trading", "structure", "derivatives", "research", "markets"]

def scan_url(firm, url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text().lower()

        score_primary = sum(1 for k in KEYWORDS_PRIMARY if k in text)
        score_secondary = sum(1 for k in KEYWORDS_SECONDARY if k in text)

        has_2026 = "2026" in text
        has_intern = any(k in text for k in ["intern", "stage", "stagiaire"])
        has_relevant = any(k in text for k in KEYWORDS_SECONDARY)

        if has_2026 and has_intern and score_secondary > 0:
            tag = "🔥 Très Pertinent"
        elif has_2026 and has_intern:
            tag = "⭐ Pertinent"
        elif has_intern and has_relevant:
            tag = "💡 Potentiel"
        else:
            tag = "– Aucune correspondance"

        return (firm, url, tag)
    except Exception as e:
        return (firm, url, f"❌ Erreur : {str(e)}")

results = [scan_url(firm, url) for firm, url in TARGETS.items()]

tres_pertinent = []
pertinent = []
potentiel = []
erreurs = []

for firm, url, tag in results:
    if "Très Pertinent" in tag:
        tres_pertinent.append((firm, url))
    elif "Pertinent" in tag:
        pertinent.append((firm, url))
    elif "Potentiel" in tag:
        potentiel.append((firm, url))
    elif "Erreur" in tag:
        erreurs.append((firm, url, tag))

now = datetime.now().strftime("%d/%m/%Y à %H:%M")

html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            padding: 20px;
            max-width: 800px;
            margin: auto;
        }}
        .header {{
            background-color: #4a90e2;
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .section {{
            background-color: white;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            margin-top: 0;
        }}
        .company {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        .company:last-child {{
            border-bottom: none;
        }}
        .link {{
            text-decoration: none;
            color: #4a90e2;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Internship Tracker 2026</h1>
        <p>Rapport généré le {now}</p>
    </div>
"""

def render_section(title, companies, emoji):
    if not companies:
        return f'<div class="section"><h2>{emoji} {title}</h2><p><i>Aucune offre trouvée.</i></p></div>'
    html_part = f'<div class="section"><h2>{emoji} {title}</h2>'
    for firm, url in companies:
        html_part += f'''
            <div class="company">
                <div>{firm}</div>
                <div><a class="link" href="{url}" target="_blank">Voir l'offre</a></div>
            </div>
        '''
    html_part += '</div>'
    return html_part

html += render_section("Offres très pertinentes", tres_pertinent, "🔥")
html += render_section("Offres pertinentes", pertinent, "⭐")
html += render_section("Offres potentielles", potentiel, "💡")

if erreurs:
    html += '<div class="section"><h2>❌ Erreurs</h2>'
    for firm, url, err in erreurs:
        html += f'<p><b>{firm}</b> — {err}</p>'
    html += '</div>'

html += """
    <div class="section" style="text-align:center;">
        <p>⏱️ Prochaine analyse dans 24h</p>
        <p style="font-size:12px; color:#999;">Automatisé via GitHub Actions</p>
    </div>
</body>
</html>
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = f"📬 Tracker Internships 2026 – Résultats {now}"
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER

part1 = MIMEText(html, "html", "utf-8")
msg.attach(part1)

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("[✔] Email envoyé avec succès.")
except Exception as e:
    print(f"[❌] Échec de l’envoi d’email : {e}")
