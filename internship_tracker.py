# -*- coding: utf-8 -*-
"""
Internship Tracker 2026 - Professional Version
Automated web scraping for financial internship opportunities

Author: RIAL Fares
Version: 2.0 - Complete Automation
Date: July 2025

© 2025 RIAL Fares - All rights reserved
This code is protected by copyright. Author credits must be preserved.
"""

#########################################################################################
# CRÉDITS OBLIGATOIRES - NE PAS SUPPRIMER
# 
# Développeur Principal : RIAL Fares
# Projet : Tracker de Stages Financiers 2026
# Version : 2.0 - Automatisation Complète
# 
# CLAUSE DE PROTECTION :
# Les crédits d'auteur (RIAL Fares) sont protégés et ne peuvent être supprimés.
# Toute utilisation de ce code doit conserver la mention de l'auteur original.
#
# © 2025 RIAL Fares - Tous droits réservés
#########################################################################################

import time
import smtplib
import os
import json
import schedule
import threading
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Try to import selenium with proper error handling
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import WebDriverException, TimeoutException
except ImportError as e:
    print(f"Error importing selenium: {e}")
    print("Please install selenium with: pip install -r requirements.txt")
    exit(1)

# Load environment variables
load_dotenv()

# Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your-email@gmail.com")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-app-password")

# TARGETS - Financial companies for internship opportunities
TARGETS = {
    "J.P. Morgan": "https://careers.jpmorgan.com/us/en/students/programs",
    "Goldman Sachs": "https://www.goldmansachs.com/careers/students/programs/",
    "Morgan Stanley": "https://www.morganstanley.com/people-opportunities/students-graduates/programs",
    "Bank of America": "https://campus.bankofamerica.com/",
    "Citigroup": "https://www.citigroup.com/global/careers/students-graduates",
    "Wells Fargo": "https://www.wellsfargo.com/about/careers/student-programs/",
    "Barclays": "https://search.jobs.barclays/students-graduates/",
    "BNP Paribas": "https://group.bnpparibas/en/careers/job-offers",
    "Deutsche Bank": "https://www.db.com/careers/en/grad/internships.html",
    "UBS": "https://www.ubs.com/global/en/careers/students-and-graduates/internships.html",
    "Societe Generale": "https://careers.societegenerale.com/en/job-opportunities",
    "HSBC": "https://www.hsbc.com/careers/students-and-graduates/student-opportunities",
    "Santander": "https://www.santander.com/en/careers/students-and-graduates",
    "ING": "https://www.ing.jobs/Global/Careers/Students-graduates.htm",
    "Credit Agricole": "https://www.credit-agricole.com/en/careers/students-and-young-graduates",
    "Natixis": "https://www.natixis.com/natixis/jcms/careers_5975/en/careers",
    "Nomura": "https://www.nomura.com/europe/careers/graduate/",
    "Jefferies": "https://www.jefferies.com/careers/students-graduates/",
    "Evercore": "https://www.evercore.com/careers/students/",
    "Lazard": "https://www.lazard.com/careers/students-recent-graduates/",
    "Rothschild & Co": "https://www.rothschildandco.com/en/careers/students-and-graduates/",
    "Citadel": "https://www.citadel.com/careers/open-positions/",
    "Citadel Securities": "https://www.citadelsecurities.com/careers/open-positions/",
    "Two Sigma": "https://careers.twosigma.com/careers/SearchJobs",
    "D.E. Shaw": "https://www.deshaw.com/careers",
    "Renaissance Technologies": "https://www.rentec.com/Careers.action",
    "Bridgewater Associates": "https://www.bridgewater.com/careers/",
    "AQR Capital": "https://careers.aqr.com/",
    "Man AHL": "https://www.man.com/careers",
    "Squarepoint Capital": "https://www.squarepoint-capital.com/careers",
    "Qube Research & Technologies": "https://qrtechnologies.com/join-us/",
    "G-Research": "https://www.gresearch.com/careers/students-and-graduates/",
    "Capital Fund Management": "https://www.cfm.fr/careers/interns",
    "Millennium": "https://www.mlp.com/careers/",
    "Point72": "https://www.point72.com/careers/",
    "Jane Street": "https://www.janestreet.com/join-jane-street/open-roles/",
    "Optiver": "https://optiver.com/working-at-optiver/career-opportunities/",
    "IMC Trading": "https://www.imc.com/eu/careers/students/",
    "Jump Trading": "https://www.jumptrading.com/careers/",
    "Hudson River Trading": "https://www.hudsonrivertrading.com/careers/job-openings/",
    "DRW": "https://drw.com/careers",
    "Akuna Capital": "https://akunacapital.com/careers",
    "Maven Securities": "https://www.mavensecurities.com/careers",
    "Susquehanna": "https://www.sig.com/careers/",
    "Tower Research Capital": "https://www.tower-research.com/careers/",
    "Virtu Financial": "https://www.virtu.com/careers/",
    "BlackRock": "https://careers.blackrock.com/early-careers/",
    "Vanguard": "https://www.vanguardjobs.com/students-graduates/",
    "Fidelity": "https://jobs.fidelity.com/students-graduates/",
    "State Street": "https://www.statestreet.com/careers/students-and-graduates",
    "Coinbase": "https://www.coinbase.com/careers/students-new-grads",
    "Binance": "https://www.binance.com/en/careers/students-graduates",
    "Revolut": "https://www.revolut.com/careers/students-graduates/",
    "Robinhood": "https://careers.robinhood.com/students-graduates/",
    "McKinsey": "https://www.mckinsey.com/careers/students",
    "BCG": "https://www.bcg.com/careers/students",
    "Bain": "https://www.bain.com/careers/students-recent-graduates/",
    "Oliver Wyman": "https://www.oliverwyman.com/careers/students-graduates.html"
}

# Keywords for detection
KEYWORDS_PRIMARY = ["intern", "2026", "stage", "stagiaire", "summer intern", "summer analyst"]
KEYWORDS_SECONDARY = ["quant", "trading", "trader", "structuring", "structureur", "sales", "front office",
                     "global markets", "capital markets", "derivatives", "fixed income", "equity",
                     "quantitative research", "algorithmic trading", "risk management"]

def setup_driver():
    """Setup Chrome driver with proper options"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except WebDriverException as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Please ensure Chrome and ChromeDriver are installed and in PATH")
        return None

def analyze_page(driver, url, firm_name, timeout=10):
    """Analyze a company's career page for internship opportunities"""
    try:
        driver.get(url)
        
        # Wait for page to load
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        time.sleep(2)  # Additional wait for dynamic content
        
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        
        # Calculate scores
        primary_score = sum(1 for keyword in KEYWORDS_PRIMARY if keyword in body_text)
        secondary_score = sum(1 for keyword in KEYWORDS_SECONDARY if keyword in body_text)
        
        # Detection flags
        has_2026 = "2026" in body_text
        has_intern = any(k in body_text for k in ["intern", "stage", "stagiaire"])
        has_relevant_terms = any(k in body_text for k in KEYWORDS_SECONDARY)
        
        return {
            "firm": firm_name,
            "url": url,
            "primary_score": primary_score,
            "secondary_score": secondary_score,
            "has_2026": has_2026,
            "has_intern": has_intern,
            "has_relevant_terms": has_relevant_terms,
            "status": "success"
        }
        
    except TimeoutException:
        return {
            "firm": firm_name,
            "url": url,
            "status": "error",
            "error": "Page load timeout"
        }
    except Exception as e:
        return {
            "firm": firm_name,
            "url": url,
            "status": "error",
            "error": str(e)
        }

def categorize_result(result):
    """Categorize analysis results"""
    if result["status"] == "error":
        return "ERROR"
    
    if result["has_2026"] and result["has_intern"] and result["secondary_score"] > 0:
        return "VERY_RELEVANT"
    
    if result["has_2026"] and result["has_intern"]:
        return "RELEVANT"
    
    if result["has_intern"] and result["has_relevant_terms"]:
        return "POTENTIAL"
    
    return "NO_MATCH"

def create_html_email(very_relevant, relevant, potential, no_match, errors):
    """Create HTML email content"""
    current_time = datetime.now().strftime("%d/%m/%Y à %H:%M")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: bold;
            }}
            .header p {{
                margin: 10px 0 0 0;
                font-size: 16px;
                opacity: 0.9;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin-bottom: 30px;
            }}
            .stat-card {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-left: 4px solid #667eea;
            }}
            .stat-number {{
                font-size: 24px;
                font-weight: bold;
                color: #667eea;
            }}
            .stat-label {{
                font-size: 12px;
                color: #666;
                margin-top: 5px;
            }}
            .section {{
                background: white;
                margin-bottom: 25px;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .section-header {{
                padding: 20px;
                color: white;
                font-weight: bold;
                font-size: 18px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .section-header.very-relevant {{
                background: linear-gradient(135deg, #4CAF50, #45a049);
            }}
            .section-header.relevant {{
                background: linear-gradient(135deg, #2196F3, #1976D2);
            }}
            .section-header.potential {{
                background: linear-gradient(135deg, #FF9800, #F57C00);
            }}
            .section-content {{
                padding: 0;
            }}
            .company-item {{
                padding: 15px 20px;
                border-bottom: 1px solid #eee;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: background-color 0.3s;
            }}
            .company-item:hover {{
                background-color: #f8f9fa;
            }}
            .company-item:last-child {{
                border-bottom: none;
            }}
            .company-name {{
                font-weight: bold;
                color: #333;
                font-size: 16px;
            }}
            .company-link {{
                color: #667eea;
                text-decoration: none;
                font-size: 14px;
                padding: 5px 10px;
                border: 1px solid #667eea;
                border-radius: 4px;
                transition: all 0.3s;
            }}
            .company-link:hover {{
                background-color: #667eea;
                color: white;
            }}
            .empty-section {{
                padding: 20px;
                text-align: center;
                color: #666;
                font-style: italic;
            }}
            .priority-badge {{
                background: #e8f5e8;
                color: #2e7d32;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                color: #666;
                font-size: 14px;
            }}
            .emoji {{
                font-size: 20px;
                margin-right: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 Internship Tracker 2026</h1>
            <p>Rapport généré le {current_time}</p>
            <p>Scan de {len(TARGETS)} entreprises financières</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{len(very_relevant)}</div>
                <div class="stat-label">Très pertinentes</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(relevant)}</div>
                <div class="stat-label">Pertinentes</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(potential)}</div>
                <div class="stat-label">Potentielles</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(errors)}</div>
                <div class="stat-label">Erreurs</div>
            </div>
        </div>
    """
    
    # Add sections for each category
    sections = [
        ("very-relevant", "🔥", "Offres très pertinentes", very_relevant, "PRIORITÉ MAX"),
        ("relevant", "⭐", "Offres pertinentes", relevant, ""),
        ("potential", "💡", "Offres potentielles", potential[:10], "Top 10 affichées")
    ]
    
    for section_class, emoji, title, results, badge in sections:
        html += f"""
        <div class="section">
            <div class="section-header {section_class}">
                <span class="emoji">{emoji}</span>
                <span>{title} ({len(results if section_class != 'potential' else potential)})</span>
                {f'<span class="priority-badge">{badge}</span>' if badge else ''}
            </div>
            <div class="section-content">
        """
        
        if results:
            for result in results:
                html += f"""
                <div class="company-item">
                    <div class="company-name">{result['firm']}</div>
                    <a href="{result['url']}" class="company-link" target="_blank">Voir l'offre</a>
                </div>
                """
        else:
            html += f'<div class="empty-section">Aucune offre trouvée dans cette catégorie</div>'
        
        html += "</div></div>"
    
    html += f"""
        <div class="footer">
            <p><strong>Prochaine analyse automatique dans 24h</strong></p>
            <p>Tracker automatisé - Surveillance continue des opportunités stage 2026</p>
        </div>
    </body>
    </html>
    """
    
    return html

def send_email(very_relevant, relevant, potential, no_match, errors):
    """Send email notification with results"""
    if not all([EMAIL_SENDER, EMAIL_RECEIVER, EMAIL_PASSWORD]):
        print("Email configuration missing. Please check .env file.")
        return False
    
    try:
        # Create HTML content
        html_content = create_html_email(very_relevant, relevant, potential, no_match, errors)
        
        # Create text fallback
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text_content = f"""
RAPPORT INTERNSHIP TRACKER 2026
Généré le: {current_time}
Entreprises analysées: {len(TARGETS)}

OFFRES TRÈS PERTINENTES ({len(very_relevant)}):
{"-" * 50}
"""
        
        for result in very_relevant:
            text_content += f"- {result['firm']} -> {result['url']}\\n"
        
        text_content += f"""
OFFRES PERTINENTES ({len(relevant)}):
{"-" * 50}
"""
        
        for result in relevant:
            text_content += f"- {result['firm']} -> {result['url']}\\n"
        
        text_content += f"""
STATISTIQUES:
- Très pertinentes: {len(very_relevant)}
- Pertinentes: {len(relevant)}
- Potentielles: {len(potential)}
- Erreurs: {len(errors)}
"""
        
        # Create email
        msg = MIMEMultipart('alternative')
        msg["Subject"] = f"🎯 Tracker Internships 2026 - {len(very_relevant)} offres prioritaires trouvées"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        
        # Attach both versions
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        print("[✓] Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"[✗] Error sending email: {e}")
        return False

def main():
    """Main execution function"""
    print("🎯 Internship Tracker 2026 - Starting analysis...")
    print("👨‍💻 Développé par RIAL Fares")
    print("=" * 50)
    print(f"Scanning {len(TARGETS)} companies...")
    
    # Setup driver
    driver = setup_driver()
    if not driver:
        print("Failed to setup Chrome driver. Exiting.")
        return
    
    results = []
    
    try:
        # Analyze each company
        for i, (firm, url) in enumerate(TARGETS.items(), 1):
            print(f"[{i}/{len(TARGETS)}] Analyzing: {firm}")
            result = analyze_page(driver, url, firm)
            results.append(result)
            
            # Add delay between requests
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\\n[!] Analysis interrupted by user")
    finally:
        driver.quit()
    
    # Categorize results
    very_relevant = [r for r in results if categorize_result(r) == "VERY_RELEVANT"]
    relevant = [r for r in results if categorize_result(r) == "RELEVANT"]
    potential = [r for r in results if categorize_result(r) == "POTENTIAL"]
    no_match = [r for r in results if categorize_result(r) == "NO_MATCH"]
    errors = [r for r in results if categorize_result(r) == "ERROR"]
    
    # Display results
    print("\\n" + "="*50)
    print("ANALYSIS SUMMARY")
    print("="*50)
    
    print(f"\\n🔥 VERY RELEVANT ({len(very_relevant)}):")
    for result in very_relevant:
        print(f"  - {result['firm']}")
    
    print(f"\\n⭐ RELEVANT ({len(relevant)}):")
    for result in relevant:
        print(f"  - {result['firm']}")
    
    print(f"\\n💡 POTENTIAL ({len(potential)}):")
    for result in potential[:10]:  # Show top 10
        print(f"  - {result['firm']}")
    
    if len(potential) > 10:
        print(f"  ... and {len(potential) - 10} more")
    
    print(f"\\n📊 STATISTICS:")
    print(f"  - Very relevant: {len(very_relevant)}")
    print(f"  - Relevant: {len(relevant)}")
    print(f"  - Potential: {len(potential)}")
    print(f"  - No match: {len(no_match)}")
    print(f"  - Errors: {len(errors)}")
    
    # Send email notification
    if very_relevant or relevant:
        print("\\n📧 Sending email notification...")
        send_email(very_relevant, relevant, potential, no_match, errors)
    else:
        print("\\n📧 No significant results to email")
    
    # Save results to JSON
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "very_relevant": very_relevant,
            "relevant": relevant,
            "potential": potential,
            "no_match": no_match,
            "errors": errors
        }, f, ensure_ascii=False, indent=2)
    
    print("\\n✅ Analysis complete! Results saved to results.json")

def run_scheduled_analysis():
    """Fonction pour exécuter l'analyse programmée"""
    print(f"🕒 Analyse programmée démarrée à {datetime.now().strftime('%H:%M:%S')}")
    main()

def start_scheduler():
    """Démarre le planificateur d'analyses automatiques"""
    # Configuration de l'heure d'exécution (par défaut : 09:00)
    execution_time = os.getenv("EXECUTION_TIME", "09:00")
    print(f"📅 Planificateur démarré - Analyse quotidienne à {execution_time}")
    
    # Programmer l'exécution quotidienne
    schedule.every().day.at(execution_time).do(run_scheduled_analysis)
    
    # Boucle d'exécution du planificateur
    while True:
        schedule.run_pending()
        time.sleep(60)  # Vérifier toutes les minutes

def run_interactive():
    """Mode interactif pour choisir l'exécution"""
    print("🎯 Internship Tracker 2026")
    print("👨‍💻 Développé par RIAL Fares")
    print("=" * 50)
    print("Choisissez le mode d'exécution :")
    print("1. Exécution immédiate (une fois)")
    print("2. Exécution programmée quotidienne")
    print("3. Quitter")
    
    while True:
        try:
            choice = input("\\nVotre choix (1-3): ").strip()
            
            if choice == "1":
                print("\\n🚀 Démarrage de l'analyse...")
                main()
                break
            elif choice == "2":
                execution_time = input("Heure d'exécution quotidienne (format HH:MM, défaut 09:00): ").strip()
                if not execution_time:
                    execution_time = "09:00"
                
                # Valider le format de l'heure
                try:
                    datetime.strptime(execution_time, "%H:%M")
                    os.environ["EXECUTION_TIME"] = execution_time
                    
                    print(f"\\n⏰ Programmation de l'analyse quotidienne à {execution_time}")
                    print("🔄 Le programme va maintenant s'exécuter en arrière-plan...")
                    print("💡 Appuyez sur Ctrl+C pour arrêter le planificateur")
                    
                    # Première exécution immédiate
                    print("\\n🚀 Première exécution...")
                    main()
                    
                    # Démarrer le planificateur
                    start_scheduler()
                    
                except ValueError:
                    print("❌ Format d'heure invalide. Utilisez HH:MM (ex: 09:00)")
                    continue
                except KeyboardInterrupt:
                    print("\\n\\n🛑 Planificateur arrêté par l'utilisateur")
                    break
            elif choice == "3":
                print("👋 Au revoir !")
                break
            else:
                print("❌ Choix invalide. Veuillez choisir 1, 2 ou 3.")
                
        except KeyboardInterrupt:
            print("\\n\\n🛑 Programme arrêté par l'utilisateur")
            break

if __name__ == "__main__":
    # Vérifier si des arguments sont passés
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheduled":
            # Exécution programmée (sans interaction)
            execution_time = os.getenv("EXECUTION_TIME", "09:00")
            print(f"🕒 Mode programmé - Exécution quotidienne à {execution_time}")
            start_scheduler()
        elif sys.argv[1] == "--now":
            # Exécution immédiate
            main()
        else:
            print("Usage: python internship_tracker.py [--scheduled|--now]")
    else:
        # Mode interactif par défaut
        run_interactive()
