import re

def nettoyer_noms_prenoms(patient):
    """
    Nom / Prénom → Format titre — première lettre majuscule (Diallo)
    Supprime les espaces inutiles en début, fin et les doubles espaces internes.
    """
    try:
        nom = patient["nom"].replace("\xa0", " ").strip()
        nom = " ".join(nom.split())
        patient["nom"] = nom.title() if nom != "" else ""

        prenom = patient["prenom"].replace("\xa0", " ").strip()
        prenom = " ".join(prenom.split())
        patient["prenom"] = prenom.title() if prenom != "" else ""

        return patient
    except Exception as e:
        print(f"Erreur nettoyage Nom/Prénom (ID {patient.get('id', '?')}) : {e}")
        return patient


def nettoyer_telephones(patient):
    """
    Téléphone → 9 chiffres sans espaces, commence par 7
    Supprime les tirets, espaces et indicatifs internationaux.
    """
    try:
        tel = patient["telephone"].strip().replace(" ", "").replace("-", "")

        if tel.startswith("+221"):
            tel = tel[4:]
        elif tel.startswith("00221"):
            tel = tel[5:]

        # On garde une chaîne vide si le numéro est suspect (ex: 770000000)
        if len(set(tel)) == 1:
            patient["telephone"] = ""
        else:
            # On applique la règle stricte : 9 chiffres commençant par 7
            patient["telephone"] = tel if re.fullmatch(r"7\d{8}", tel) else ""

        return patient
    except Exception as e:
        print(f"Erreur nettoyage Téléphone (ID {patient.get('id', '?')}) : {e}")
        return patient


def nettoyer_villes(patient):
    """
    Ville → Orthographe standardisée, format titre
    """
    try:
        ville = patient["ville"].replace("\xa0", " ").strip()
        if ville == "":
            patient["ville"] = ""
            return patient

        ville = ville.title()

        corrections = {
            "Dakar": "Dakar", "Dakarr": "Dakar", "Dakkar": "Dakar",
            "Kaolak": "Kaolack", "Kaolack": "Kaolack",
            "Ziguinchor": "Ziguinchor", "Ziguincor": "Ziguinchor", "Ziginchor": "Ziguinchor",
            "Tambacounda": "Tambacounda", "Tamba": "Tambacounda",
            "Thies": "Thies", "Thiès": "Thies", "Thiess": "Thies",
            "Diourbel": "Diourbel", "Diorbel": "Diourbel",
            "Louga": "Louga", "Lougar": "Louga",
            "Saint-Louis": "Saint-Louis", "Saint Louis": "Saint-Louis",
            "Saint Louise": "Saint-Louis", "Saint-Louise": "Saint-Louis"
        }
        patient["ville"] = corrections.get(ville, ville)
        return patient
    except Exception as e:
        print(f"Erreur nettoyage Ville (ID {patient.get('id', '?')}) : {e}")
        return patient


def nettoyer_groupe_sanguin(patient):
    """
    Groupe sanguin → Nettoyage de surface (Majuscule, suppression des espaces).
    La validation stricte se fera dans validation.py
    """
    try:
        patient["groupe_sanguin"] = patient["groupe_sanguin"].strip().upper().replace(" ", "")
        return patient
    except Exception as e:
        print(f"Erreur nettoyage Groupe Sanguin (ID {patient.get('id', '?')}) : {e}")
        return patient


def nettoyer_poids_taille(patient):
    """
    Poids et Taille → Supprime simplement les espaces pour éviter les bugs de parsing.
    Conserve le format chaîne de caractères (str) pour l'étape d'affichage des anomalies.
    """
    try:
        patient["poids"] = patient["poids"].strip().replace(" ", "")
        patient["taille"] = patient["taille"].strip().replace(" ", "")
        return patient
    except Exception as e:
        print(f"Erreur nettoyage Poids/Taille (ID {patient.get('id', '?')}) : {e}")
        return patient


def nettoyer_doublons(patients):
    """
    Doublons → Supprimer toutes les répétitions de lignes exactes ou quasi-doublons.
    """
    patients_uniques = []
    cles_identifiees = set()
    nb_doublons = 0

    for p in patients:
        # Création d'une clé d'identification textuelle unique
        nom_cle = p["nom"].strip().lower()
        prenom_cle = p["prenom"].strip().lower()
        tel_cle = p["telephone"].strip().replace(" ", "").replace("-", "")

        cle_unique = (nom_cle, prenom_cle, tel_cle)

        if cle_unique in cles_identifiees:
            nb_doublons += 1
        else:
            cles_identifiees.add(cle_unique)
            patients_uniques.append(p)

    return patients_uniques, nb_doublons


def nettoyer_tous_les_patients(patients):
    """
    Parcourt la liste et applique toutes les règles de standardisation textuelle.
    """
    for patient in patients:
        nettoyer_noms_prenoms(patient)
        nettoyer_telephones(patient)
        nettoyer_villes(patient)
        nettoyer_groupe_sanguin(patient)
        nettoyer_poids_taille(patient)

    return patients