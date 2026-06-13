# ---> Gestion des erreurs avec try/except
# 2. Liste complète des erreurs présentes dans le fichier
# -Noms et prénoms—Espaces inutiles en début et fin :  " Ndiaye "  →  "Ndiaye"
# —Noms entièrement en minuscules :  "fall"  →  "Fall"
# —Noms entièrement en majuscules :  "DIALLO"  →  "Diallo"
# —Espaces invisibles en fin de chaîne (subtil, difficile à détecter)
# -Âges—Valeur manquante (champ vide)
# —Âge négatif :  -5
# - Âge irréaliste : supérieur à 120
# —Âge égal à zéro :  0(à signaler comme suspect)
# Téléphones—Espaces dans le numéro :  "77 123 45 67"  →  "771234567"
# —Tirets dans le numéro :  "78-222-33-44"  →  "782223344"
# —Préfixe international  00221→ à supprimer
# —Préfixe international  +221→ à supprimer
# —Numéro avec tous les chiffres identiques :  770000000(suspect)
# Villes—Espaces inutiles :  "Dakar "  →  "Dakar"
# —Fautes de frappe :  "dakarr"  →  "Dakar"
# —Majuscules incorrectes :  "THIES"  →  "Thies"
# —Orthographe incohérente :  "Saint louis"  →  "Saint-Louis"
# Groupes sanguins
# —Seuls les groupes valides sont acceptés :  A+, A-, B+, B-, AB+, AB-, O+, O-
# —Tout autre groupe est invalide et entraîne le rejet du patientPoids et taille
# —Valeur non numérique :  "abc"—Valeur manquante : champ vide ou  "N/A"
# —Poids impossible : inférieur à 1 ou supérieur à 300
# —Taille impossible : inférieure à 50 ou supérieure à 250
# —Doublons exacts : même ligne répétée
# —Quasi-doublons : même patient avec légère différence (espace en fin de nom)
def valider_age(patient):
    """
    Vérifie que l'âge est un entier valide compris entre 0 et 120.
    Met à jour patient['age'] en entier si valide, sinon le marque invalide.
    Retourne True si valide, False sinon.
    """
    try:
        age_str = patient["age"].strip()

        if age_str == "":
            return False

        age = int(age_str)

        if age < 0 or age > 120:
            return False

        if age == 0:
            print(f"Patient id={patient['id']} : âge égal à 0 (suspect, mais accepté)")

        patient["age"] = age
        return True

    except (ValueError, KeyError):
        return False


def valider_groupe_sanguin(patient):
    """
    Vérifie que le groupe sanguin appartient à la liste autorisée.
    Retourne True si valide, False sinon.
    """
    groupes_valides = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}

    try:
        groupe = patient["groupe_sanguin"].strip()
        return groupe in groupes_valides
    except (KeyError, AttributeError):
        return False


def valider_poids(patient):
    """
    Vérifie que le poids est un nombre réel valide entre 1 et 300.
    Met à jour patient['poids'] en float si valide.
    Retourne True si valide, False sinon.
    """
    try:
        poids_str = patient["poids"].strip()

        if poids_str == "" or poids_str.upper() == "N/A":
            return False

        poids = float(poids_str)

        if poids < 1 or poids > 300:
            return False

        patient["poids"] = poids
        return True

    except (ValueError, KeyError):
        return False


def valider_taille(patient):
    """
    Vérifie que la taille est un entier valide entre 50 et 250.
    Met à jour patient['taille'] en int si valide.
    Retourne True si valide, False sinon.
    """
    try:
        taille_str = patient["taille"].strip()

        if taille_str == "" or taille_str.upper() == "N/A":
            return False

        taille = int(float(taille_str))  # gère le cas "175.0" si jamais

        if taille < 50 or taille > 250:
            return False

        patient["taille"] = taille
        return True

    except (ValueError, KeyError):
        return False


def valider_nom_prenom(patient):
    """
    Vérifie que nom et prenom ne sont pas vides.
    À appeler APRÈS le nettoyage (nom/prenom déjà strippés).
    """
    try:
        return patient["nom"] != "" and patient["prenom"] != ""
    except KeyError:
        return False


def valider_telephone(patient):
    """
    Vérifie que le téléphone est valide (non vide après nettoyage).
    À appeler APRÈS nettoyer_telephones (qui met "" si invalide).
    """
    try:
        return patient["telephone"] != ""
    except KeyError:
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