# Tracker de Stages 2026 🎯

**Développé par RIAL Fares**

Un outil de web scraping automatisé qui surveille les pages carrières des entreprises financières pour les opportunités de stage 2026 et envoie des notifications par email.

## 👨‍💻 Auteur et Crédits

**Développeur Principal :** RIAL Fares  
**Projet :** Tracker de Stages Financiers 2026  
**Version :** 2.0 - Automatisation Complète  
**Date :** Juillet 2025

> ⚠️ **IMPORTANT** : Ce projet a été développé par RIAL Fares. Les crédits d'auteur doivent être conservés dans toute utilisation, modification ou redistribution de ce code.

## Fonctionnalités

- **Web Scraping Automatisé** : Surveille plus de 50 grandes entreprises financières
- **Catégorisation Intelligente** : Classe les opportunités par pertinence
- **Notifications Email** : Envoie des rapports email au format HTML
- **Gestion d'Erreurs** : Gestion robuste des erreurs pour le web scraping
- **Export de Données** : Sauvegarde les résultats au format JSON
- **Style Professionnel** : Templates email HTML élégants
- **Automatisation Quotidienne** : Exécution programmée tous les jours à heure fixe

## Entreprises Surveillées

Le tracker surveille les opportunités de stage chez :
- **Banques d'Investissement** : J.P. Morgan, Goldman Sachs, Morgan Stanley, etc.
- **Banques Commerciales** : Bank of America, Citigroup, Wells Fargo, etc.
- **Hedge Funds** : Citadel, Two Sigma, D.E. Shaw, etc.
- **Sociétés de Trading** : Jane Street, Optiver, IMC Trading, etc.
- **Gestion d'Actifs** : BlackRock, Vanguard, Fidelity, etc.
- **Conseil** : McKinsey, BCG, Bain, etc.
- **Fintech** : Coinbase, Revolut, Robinhood, etc.

## Installation

1. **Clonez/Téléchargez le projet**
2. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Installez Chrome et ChromeDriver** :
   - Téléchargez le navigateur Chrome
   - Téléchargez ChromeDriver depuis https://chromedriver.chromium.org/
   - Ajoutez ChromeDriver à votre PATH

4. **Configurez les paramètres email** :
   - Copiez `.env.template` vers `.env`
   - Remplissez vos identifiants email (utilisez un mot de passe d'application Gmail)

## Configuration

### Configuration Email (Gmail)
1. Activez l'authentification à 2 facteurs sur votre compte Google
2. Allez sur : https://myaccount.google.com/apppasswords
3. Générez un mot de passe d'application pour "Mail"
4. Utilisez ce mot de passe à 16 caractères dans votre fichier `.env`

### Variables d'Environnement
```env
EMAIL_SENDER=votre-email@gmail.com
EMAIL_RECEIVER=votre-email@gmail.com
EMAIL_PASSWORD=votre-mot-de-passe-app-gmail
EXECUTION_TIME=09:00
```

## Utilisation

### Méthodes d'Exécution

#### 1. Exécution Interactive (Recommandée)
```bash
python internship_tracker.py
```
Le programme vous proposera de choisir :
- Exécution immédiate (une fois)
- Exécution programmée quotidienne
- Quitter

#### 2. Exécution Immédiate
```bash
python internship_tracker.py --now
```
OU double-cliquez sur : `lancer_maintenant.bat`

#### 3. Automatisation Quotidienne
```bash
python internship_tracker.py --scheduled
```
OU double-cliquez sur : `lancer_automatisation.bat`

### Résultats Attendus
- Mises à jour de progression dans la console
- Notification email avec rapport HTML
- Fichier `results.json` avec les résultats détaillés

## Comment ça Marche

1. **Web Scraping** : Utilise Selenium pour visiter chaque page carrière d'entreprise
2. **Analyse de Contenu** : Recherche les mots-clés liés aux stages 2026
3. **Catégorisation** :
   - **Très Pertinent** : Contient "2026" + "stage" + termes financiers
   - **Pertinent** : Contient "2026" + "stage"
   - **Potentiel** : Contient "stage" + termes financiers
4. **Rapport Email** : Envoie un résumé au format HTML
5. **Export de Données** : Sauvegarde les résultats dans un fichier JSON

## Mots-Clés

### Mots-Clés Primaires
- intern, 2026, stage, stagiaire, summer intern, summer analyst

### Mots-Clés Secondaires (Finance)
- quant, trading, trader, structuring, sales, front office
- global markets, capital markets, derivatives, fixed income
- quantitative research, algorithmic trading, risk management


## Dépannage

### Problèmes Courants

1. **Erreur d'Import Selenium** :
   ```bash
   pip install selenium
   ```

2. **ChromeDriver Introuvable** :
   - Téléchargez depuis https://chromedriver.chromium.org/
   - Ajoutez au PATH ou placez dans le répertoire du projet

3. **Échec d'Authentification Email** :
   - Utilisez un mot de passe d'application Gmail, pas votre mot de passe normal
   - Vérifiez que l'authentification à 2 facteurs est activée

4. **Erreurs de Timeout** :
   - Certains sites peuvent être lents ou bloquer les requêtes automatisées
   - Le script inclut une logique de retry et gestion d'erreurs

5. **Problèmes d'Automatisation** :
   - Vérifiez que le format d'heure est correct (HH:MM)
   - Assurez-vous que le programme reste en arrière-plan
   - Utilisez Ctrl+C pour arrêter l'automatisation

## Personnalisation

### Ajouter de Nouvelles Entreprises
Modifiez le dictionnaire `TARGETS` dans `internship_tracker.py` :
```python
TARGETS = {
    "Nom Entreprise": "https://entreprise.com/carrieres",
    # Ajoutez plus d'entreprises ici
}
```

### Modifier les Mots-Clés
Modifiez les listes de mots-clés pour différents termes de recherche :
```python
KEYWORDS_PRIMARY = ["intern", "2026", "vos-mots-cles"]
KEYWORDS_SECONDARY = ["finance", "termes-secteur"]
```

### Changer l'Heure d'Exécution
Modifiez `EXECUTION_TIME` dans le fichier `.env` :
```env
EXECUTION_TIME=14:30  # Pour 14h30
```

## Automatisation Avancée

### Démarrage Automatique Windows
Pour que le tracker se lance automatiquement au démarrage de Windows :

1. Appuyez sur `Win + R`, tapez `shell:startup`
2. Copiez le fichier `lancer_automatisation.bat` dans ce dossier
3. Le tracker se lancera automatiquement au démarrage

### Exécution en Arrière-Plan
Pour faire tourner le programme en arrière-plan :
```bash
# Windows
start /B python internship_tracker.py --scheduled

# Ou utilisez le fichier batch
lancer_automatisation.bat
```

## Considérations Légales et Éthiques

- **Respectez robots.txt** : Vérifiez les politiques de scraping des sites web
- **Limitation de Débit** : Le script inclut des délais entre les requêtes
- **Usage Personnel** : Destiné à la recherche d'emploi personnelle
- **Confidentialité des Données** : Les identifiants email sont stockés localement

## Contribution

1. Fork le dépôt
2. Créez une branche de fonctionnalité
3. Effectuez vos modifications
4. Testez minutieusement
5. Soumettez une pull request

**Note :** Toute contribution doit respecter les crédits d'auteur originaux (RIAL Fares).

## 👨‍💻 Crédits et Licence

### Auteur Original
**RIAL Fares** - Développeur Principal  
- Conception et développement initial
- Implémentation de l'automatisation
- Interface utilisateur française
- Documentation complète

### Conditions d'Utilisation
- ✅ **Usage personnel** : Libre pour la recherche d'emploi
- ✅ **Partage** : Autorisé avec conservation des crédits
- ✅ **Modification** : Autorisée avec mention de l'auteur original
- ❌ **Usage commercial** : Non autorisé sans permission
- ❌ **Suppression des crédits** : Strictement interdite

### Licence
Ce projet est destiné à un usage éducatif et personnel uniquement. Veuillez respecter les conditions d'utilisation des sites web scrapés.

**© 2025 RIAL Fares - Tous droits réservés**

> **CLAUSE DE PROTECTION** : Les crédits d'auteur (RIAL Fares) sont protégés et ne peuvent être supprimés ou modifiés. Toute utilisation de ce code doit conserver la mention de l'auteur original.

## Support

Pour les problèmes ou questions :
1. Consultez la section dépannage
2. Examinez les messages d'erreur dans la console
3. Assurez-vous que toutes les dépendances sont installées correctement
4. Testez votre configuration avec `python test_setup.py`

## Commandes Utiles

```bash
# Tester votre configuration
python test_setup.py

# Exécuter la configuration initiale
python setup.py

# Exécuter le tracker (mode interactif)
python internship_tracker.py

# Exécution immédiate
python internship_tracker.py --now

# Automatisation quotidienne
python internship_tracker.py --scheduled
```

---

**Note** : Cet outil est conçu pour des activités légitimes de recherche d'emploi. Utilisez-le de manière responsable et conformément aux conditions d'utilisation des sites web.
