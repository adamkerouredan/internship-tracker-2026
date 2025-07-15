# 📬 Internship Tracker 2026

This tool automatically scrapes the careers pages of top-tier financial institutions (J.P. Morgan, Goldman Sachs, Citadel, BNP Paribas, etc.) to detect relevant **Quant/Trading/Structuring internships** for the **2026 intake**.

It uses:
- `requests` + `BeautifulSoup` for web scraping
- `dotenv` to manage secrets
- `smtplib` to send styled email reports
- Automatic daily email alerts (via GitHub Actions or cron)

## 🚀 Usage

1. Fill in your `.env` file with:
