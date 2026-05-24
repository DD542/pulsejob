# PulseJob

> Observatoire en temps réel du marché Data & Intelligence Artificielle en France

PulseJob est un dashboard full-stack qui collecte, analyse et visualise les offres d'emploi Data & IA en France via l'API officielle France Travail. Il combine un pipeline de données Python, un moteur NLP de détection de compétences et une interface web Vue.js professionnelle.

---

## Aperçu

- **720+ offres** collectées en temps réel
- **296 villes** couvertes sur tout le territoire français
- **156 entreprises** identifiées
- **20 compétences tech** détectées automatiquement par NLP

---

## Stack Technique

| Couche | Technologie |
|--------|------------|
| Collecte de données | Python, API France Travail (OAuth2) |
| Stockage | SQLite |
| NLP | Python, détection par pattern matching |
| Backend API | Flask, Flask-CORS |
| Frontend | Vue.js 3, Vite, Tailwind CSS 3 |
| Graphiques | SVG custom (BarChart, DonutChart) |
| HTTP Client | Axios |

---

## Architecture

France Travail API → collector.py (Collecte & stockage SQLite) → nlp_engine.py (Analyse NLP) → api.py (API REST Flask port 5001) → pulsejob-frontend (Dashboard Vue.js port 5173)

---

## Fonctionnalités

- Collecte automatique des offres par mots-clés (data scientist, machine learning, data engineer...)
- Détection NLP des compétences techniques dans les descriptions (Python, SQL, Docker, AWS...)
- Dashboard interactif : KPIs, graphiques en barres, donut chart, tableau filtrable
- Recherche en temps réel dans les offres
- Design dark mode responsive (desktop et mobile)

---

## Lancer le projet

### Prérequis

- Python 3.10+
- Node.js 18+

### Backend

Cloner le projet et installer les dépendances Python, créer un fichier config.py avec vos identifiants France Travail (CLIENT_ID et CLIENT_SECRET), puis lancer la collecte avec python collector.py et l'API avec python api.py.

### Frontend

Dans le dossier pulsejob-frontend, installer les dépendances avec npm install puis lancer avec npm run dev. Ouvrir http://localhost:5173.

---

## Structure du projet

pulsejob/ contient api.py (API REST Flask), collector.py (collecte des offres), database.py (gestion SQLite), nlp_engine.py (analyse NLP), dashboard.py (prototype Streamlit backup), requirements.txt et le dossier pulsejob-frontend avec les composants Vue.js (Dashboard.vue, KpiCard.vue, BarChart.vue, DonutChart.vue, OffresTable.vue, SectionTitle.vue).

---

## Auteur

**Dylan Menga Wanda** — B3 Data & IA — ECE Paris — Supervisé par Ali Boukehila

---

## Licence

MIT