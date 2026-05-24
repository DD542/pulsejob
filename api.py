from flask import Flask, jsonify
from flask_cors import CORS
from database import get_toutes_offres
from nlp_engine import (
    analyser_competences,
    analyser_localisations,
    analyser_entreprises,
    analyser_contrats
)

app = Flask(__name__)
CORS(app)

MOTS_EXCLUS = [
    "r", "age automatique", "ntissage profond",
    "nce des donn", "lyste de donn", "erie des donn",
    "age des donn", "java"
]

def nettoyer_competences(df):
    return df[
        ~df["competence"].apply(
            lambda x: any(mot in str(x) for mot in MOTS_EXCLUS)
        )
    ].reset_index(drop=True)

@app.route("/api/stats")
def stats():
    df = get_toutes_offres()
    return jsonify({
        "total_offres": len(df),
        "total_villes": int(df["localisation"].nunique()),
        "total_entreprises": int(df[df["entreprise"] != "Non précisé"]["entreprise"].nunique()),
    })

@app.route("/api/competences")
def competences():
    df = nettoyer_competences(analyser_competences())
    return jsonify(df.head(15).to_dict(orient="records"))

@app.route("/api/villes")
def villes():
    df = analyser_localisations()
    return jsonify(df.head(10).to_dict(orient="records"))

@app.route("/api/entreprises")
def entreprises():
    df = analyser_entreprises()
    df = df[df["entreprise"] != "Non précisé"].head(10)
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/contrats")
def contrats():
    df = analyser_contrats()
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/offres")
def offres():
    df = get_toutes_offres()
    df = df[["titre", "entreprise", "localisation", "type_contrat", "experience", "date_publication"]]
    return jsonify(df.head(50).to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)