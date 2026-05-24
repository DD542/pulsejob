# PulseJob

> Observatoire en temps réel du marché Data & Intelligence Artificielle en France

PulseJob est un dashboard full-stack qui collecte, analyse et visualise les offres d'emploi Data & IA en France via l'API officielle France Travail. Il combine un pipeline de collecte de données Python, un moteur NLP de détection automatique de compétences, une API REST Flask et un dashboard Vue.js avec des graphiques SVG custom.

---

## Résultats

| Métrique | Valeur |
|----------|--------|
| Offres collectées | 720+ |
| Villes couvertes | 296 |
| Entreprises identifiées | 156 |
| Compétences détectées | 20 |
| Sources de données | 6 mots-clés différents |

---

## Stack Technique

| Couche | Technologie | Rôle |
|--------|------------|------|
| Collecte | Python 3.10, requests | Appels API France Travail OAuth2 |
| Stockage | SQLite | Persistance locale des offres |
| NLP | Python, pattern matching | Détection de compétences dans les descriptions |
| Backend | Flask 3.x, Flask-CORS | API REST exposant les données analysées |
| Frontend | Vue.js 3, Vite 5 | Interface utilisateur réactive (SPA) |
| Style | Tailwind CSS 3.4.1 | Design system utility-first |
| Graphiques | SVG custom | BarChart et DonutChart sans dépendance externe |
| HTTP | Axios | Communication frontend vers backend |

---

## Architecture

France Travail API (OAuth2) alimente collector.py qui gère l'authentification OAuth2, la recherche par 6 mots-clés, l'extraction et normalisation des champs, et le stockage SQLite avec déduplication. Les données sont stockées dans pulsejob.db avec une table offres contenant id, titre, entreprise, localisation, departement, type_contrat, date_publication, description, competences, salaire, experience et lien. nlp_engine.py effectue le nettoyage ASCII des descriptions, la détection par pattern matching sur 20 compétences tech et les analyses par compétences, villes, entreprises et contrats. api.py expose 6 endpoints Flask sur le port 5001 : /api/stats, /api/competences, /api/villes, /api/entreprises, /api/contrats et /api/offres. Le frontend Vue.js sur le port 5173 consomme ces endpoints via Axios et affiche le dashboard avec les composants Dashboard.vue, KpiCard.vue, BarChart.vue, DonutChart.vue, OffresTable.vue et SectionTitle.vue.

---

## Fonctionnalités détaillées

**Pipeline de collecte**
- Authentification OAuth2 Client Credentials vers France Travail
- Collecte sur 6 requêtes avec pagination (150 offres par requête)
- Déduplication automatique via PRIMARY KEY SQLite
- Respect des rate limits API avec délai entre requêtes

**Moteur NLP**
- Nettoyage ASCII pour neutraliser les problèmes d'encodage
- Détection de 20 compétences : Python, SQL, Git, Docker, AWS, Azure, GCP, Spark, Kubernetes, Airflow, TensorFlow, PyTorch, Pandas, Tableau, Power BI, Scala, NLP, Deep Learning, Machine Learning, Statistiques
- Comptage et classement par fréquence d'apparition

**API REST Flask**
- 6 endpoints JSON consommés par le frontend
- CORS configuré pour les requêtes cross-origin
- Filtrage des termes parasites côté API

**Dashboard Vue.js**
- Graphiques SVG 100% custom sans dépendance externe
- Animations CSS sur les barres au chargement
- Hover interactif sur le donut avec affichage du pourcentage au centre
- Filtrage full-text en temps réel sur le tableau des offres
- Design dark mode responsive avec breakpoints à 1024px et 640px
- Chargement asynchrone de toutes les données en parallèle via Promise.all

---

## Installation

### Prérequis

- Python 3.10+
- Node.js 18+
- Compte développeur France Travail sur https://francetravail.io

### Backend

```bash
git clone https://github.com/DD542/pulsejob.git
cd pulsejob
pip install -r requirements.txt
```

Créer un fichier config.py avec vos identifiants France Travail :

```python
CLIENT_ID = "votre_client_id"
CLIENT_SECRET = "votre_client_secret"
```

```bash
python collector.py
python api.py
```

### Frontend

```bash
cd pulsejob-frontend
npm install
npm run dev
```

Ouvrir http://localhost:5173

---


## Auteur

**Dylan Menga Wanda** — B3 Data & IA — ECE Paris

---

## Licence

MIT