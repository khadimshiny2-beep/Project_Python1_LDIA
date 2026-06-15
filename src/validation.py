# validation.py

def valider_nom_prenom(patient):
    try:
        return patient.get("nom", "").strip() != "" and patient.get("prenom", "").strip() != ""
    except Exception:
        return False


def valider_telephone(patient):
    # Le numéro doit faire exactement 9 chiffres et commencer par un 7 suite au nettoyage
    tel = patient.get("telephone", "").strip()
    return len(tel) == 9 and tel.startswith("7") and tel.isdigit()


def valider_age(patient):
    try:
        age_str = str(patient.get("age", "")).strip()
        if age_str == "" or age_str.upper() == "N/A":
            return False
        age = int(age_str)
        return 0 <= age <= 120
    except (ValueError, KeyError):
        return False


def valider_groupe_sanguin(patient):
    groupes_valides = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}
    return patient.get("groupe_sanguin", "").strip().upper() in groupes_valides


def valider_poids(patient):
    try:
        poids_str = str(patient.get("poids", "")).strip()
        if poids_str == "" or poids_str.upper() == "N/A":
            return False
        poids = float(poids_str)
        return 1 <= poids <= 300
    except (ValueError, KeyError):
        return False


def valider_taille(patient):
    try:
        taille_str = str(patient.get("taille", "")).strip()
        if taille_str == "" or taille_str.upper() == "N/A":
            return False
        taille = int(float(taille_str))
        return 50 <= taille <= 250
    except (ValueError, KeyError):
        return False


def patient_est_valide(patient):
    """
    Vérifie toutes les conditions de validité d'un patient.
    Retourne (True, "") si valide, ou (False, raison) sinon.
    """
    if not valider_nom_prenom(patient):
        return False, "nom ou prénom manquant"

    if not valider_telephone(patient):
        return False, "téléphone invalide"

    if not valider_age(patient):
        return False, "âge invalide (manquant, négatif ou > 120)"

    if not valider_groupe_sanguin(patient):
        return False, "groupe sanguin invalide ou non reconnu"

    if not valider_poids(patient):
        return False, "poids invalide ou manquant"

    if not valider_taille(patient):
        return False, "taille invalide ou manquante"

    return True, ""


def filtrer_patients_valides(patients):
    """
    Sépare la liste en patients valides et rejetés.
    Retourne (patients_valides, patients_rejetes, raisons_rejet)
    """
    patients_valides = []
    patients_rejetes = []
    raisons_rejet = []

    for patient in patients:
        est_valide, raison = patient_est_valide(patient)

        if est_valide:
            # Copie locale ou conversion finale optionnelle pour l'exportation interne si besoin
            # Mais on préserve la structure de dictionnaire d'origine attendue par main.py
            patients_valides.append(patient)
        else:
            patients_rejetes.append(patient)
            raisons_rejet.append((patient.get("id", "?"), raison))

    return patients_valides, patients_rejetes, raisons_rejet