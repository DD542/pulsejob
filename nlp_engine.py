import pandas as pd
from collections import Counter
from database import get_toutes_offres

COMPETENCES_TECH = [
    "python", "sql", "scala",
    "pandas", "numpy", "tensorflow", "pytorch", "keras",
    "spark", "hadoop", "airflow", "kafka", "dbt",
    "power bi", "tableau", "looker", "metabase",
    "aws", "azure", "gcp", "docker", "kubernetes",
    "nlp", "git", "linux",
    "mongodb", "postgresql", "mysql", "elasticsearch",
    "streamlit", "flask", "fastapi",
    "machine learning", "deep learning",
    "scikit-learn", "excel", "statistiques"
]

def nettoyer(texte):
    if not texte:
        return ""
    return texte.lower().encode("ascii", "ignore").decode("ascii")

def extraire_competences(description):
    texte = nettoyer(description)
    return [c for c in COMPETENCES_TECH if nettoyer(c) in texte]

def analyser_competences():
    df = get_toutes_offres()
    print(f"Analyse de {len(df)} offres...")
    toutes = []
    for desc in df["description"]:
        toutes.extend(extraire_competences(desc))
    compteur = Counter(toutes)
    result = pd.DataFrame(compteur.most_common(20), columns=["competence", "occurences"])
    print("\nTop 20 compétences :")
    print(result.to_string(index=False))
    return result

def analyser_localisations():
    df = get_toutes_offres()
    top = df["localisation"].value_counts().head(15).reset_index()
    top.columns = ["ville", "nombre_offres"]
    return top

def analyser_entreprises():
    df = get_toutes_offres()
    top = df["entreprise"].value_counts().head(15).reset_index()
    top.columns = ["entreprise", "nombre_offres"]
    return top

def analyser_contrats():
    df = get_toutes_offres()
    contrats = df["type_contrat"].value_counts().reset_index()
    contrats.columns = ["type_contrat", "nombre"]
    return contrats

if __name__ == "__main__":
    analyser_competences()
    analyser_localisations()
    analyser_entreprises()