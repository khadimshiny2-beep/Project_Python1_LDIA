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
# Groupes sanguins—Seuls les groupes valides sont acceptés :  A+, A-, B+, B-, AB+, AB-, O+, O-
# —Tout autre groupe est invalide et entraîne le rejet du patientPoids et taille
# —Valeur non numérique :  "abc"—Valeur manquante : champ vide ou  "N/A"
# —Poids impossible : inférieur à 1 ou supérieur à 300
# —Taille impossible : inférieure à 50 ou supérieure à 250Doublons
# —Doublons exacts : même ligne répétée
# —Quasi-doublons : même patient avec légère différence (espace en fin de nom)

# 3. Règles de nettoyage à respecter
#
# 
# 
# 
# 

#
#

import re


def nettoyer_noms_prenoms(patient):
    """
    Nettoie les champs 'nom' et 'prenom' du dictionnaire patient.
    """
    try:
        nom = patient["nom"].replace("\xa0", " ").strip()
        patient["nom"] = nom.title() if nom != "" else ""

        prenom = patient["prenom"].replace("\xa0", " ").strip()
        patient["prenom"] = prenom.title() if prenom != "" else ""

        return patient

    except Exception as e:
        print(f"Erreur lors du nettoyage du nom/prénom (patient {patient.get('id', '?')}) : {e}")
        return patient


def nettoyer_telephones(patient):
    """
    Nettoie le champ 'telephone' du dictionnaire patient.
    """
    try:
        tel = patient["telephone"].strip().replace(" ", "").replace("-", "")

        if tel.startswith("+221"):
            tel = tel[4:]
        elif tel.startswith("00221"):
            tel = tel[5:]

        patient["telephone"] = tel if re.fullmatch(r"7\d{8}", tel) else ""

        return patient

    except Exception as e:
        print(f"Erreur lors du nettoyage du téléphone (patient {patient.get('id', '?')}) : {e}")
        return patient


def nettoyer_villes(patient):
    """
    Nettoie le champ 'ville' du dictionnaire patient :
    - enlève les espaces inutiles (y compris invisibles)
    - met en format titre
    - corrige les fautes de frappe / orthographe connues
    """
    try:
        ville = patient["ville"].replace("\xa0", " ").strip()

        if ville == "":
            patient["ville"] = ""
            return patient

        ville = ville.title()

        corrections = {
            "Dakar": "Dakar",
            "Dakarr": "Dakar",
            "Dakkar": "Dakar",
            "Kaolak": "Kaolack",
            "Kaolack": "Kaolack",
            "Ziguinchor": "Ziguinchor",
            "Ziguincor": "Ziguinchor",
            "Ziginchor": "Ziguinchor",
            "Tambacounda": "Tambacounda",
            "Tamba": "Tambacounda",
            "Thies": "Thies",
            "Thiès": "Thies",
            "Thiess": "Thies",
            "Diourbel": "Diourbel",
            "Diorbel": "Diourbel",
            "Louga": "Louga",
            "Lougar": "Louga",
            "Saint-Louis": "Saint-Louis",
            "Saint Louis": "Saint-Louis",
            "Saint Louise": "Saint-Louis",
            "Saint-Louise": "Saint-Louis"
        }
        patient["ville"] = corrections.get(ville, ville)
        return patient
    except Exception as e:
        print(f"Erreur lors du nettoyage de la ville (patient {patient.get('id', '?')}) : {e}")
        return patient

def nettoyer_tous_les_patients(patients):
    """
    Parcourt la liste de patients une seule fois et applique
    les trois nettoyages (nom/prenom, telephone, ville) sur chacun.
    """
    for patient in patients:
        nettoyer_noms_prenoms(patient)
        nettoyer_telephones(patient)
        nettoyer_villes(patient)

    return patients