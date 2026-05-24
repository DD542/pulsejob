import requests
import time
from config import CLIENT_ID, CLIENT_SECRET
from database import init_db, inserer_offre


def get_token():
    url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
    params = {"realm": "/partenaire"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "api_offresdemploiv2 o2dsoffre"
    }
    response = requests.post(url, params=params, data=data)
    token = response.json()["access_token"]
    print("Token obtenu avec succès")
    return token


def get_offres(token, mots_cles, debut=0):
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "motsCles": mots_cles,
        "range": f"{debut}-{debut+149}",
        "sort": "1"
    }
    response = requests.get(url, headers=headers, params=params)
    print(f"Status : {response.status_code}")
    if response.status_code not in [200, 206]:
        print(f"Erreur : {response.text}")
        return []
    data = response.json()
    resultats = data.get("resultats", [])
    print(f"{len(resultats)} offres trouvées")
    return resultats


def extraire_offre(o):
    return (
        o.get("id", ""),
        o.get("intitule", ""),
        o.get("entreprise", {}).get("nom", "Non précisé"),
        o.get("lieuTravail", {}).get("libelle", ""),
        o.get("lieuTravail", {}).get("codePostal", "")[:2] if o.get("lieuTravail", {}).get("codePostal") else "",
        o.get("typeContrat", ""),
        o.get("dateCreation", ""),
        o.get("description", ""),
        ", ".join([c.get("libelle", "") for c in o.get("competences", [])]),
        o.get("salaire", {}).get("libelle", "Non précisé"),
        o.get("experienceLibelle", "Non précisé"),
        o.get("origineOffre", {}).get("urlOrigine", "")
    )


def collecter_tout():
    init_db()
    token = get_token()

    mots_cles_list = [
        "data scientist",
        "data analyst",
        "machine learning",
        "intelligence artificielle",
        "data engineer",
        "python data"
    ]

    total = 0
    for mots in mots_cles_list:
        print(f"\nRecherche : '{mots}'")
        offres = get_offres(token, mots)
        for o in offres:
            inserer_offre(extraire_offre(o))
            total += 1
        print(f"{len(offres)} offres récupérées")
        time.sleep(3)

    print(f"\nTotal inséré en base : {total} offres")


if __name__ == "__main__":
    collecter_tout()