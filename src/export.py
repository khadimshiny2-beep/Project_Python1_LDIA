# ---> Ecrire dans les fichiers 'patients_propres.csv' et 'rapport.txt'

import csv
import json
import os
from datetime import datetime


def obtenir_chemin_sortie(nom_fichier, sous_dossier="data"):
    """
    Construit le chemin absolu vers un fichier de sortie
    (data/ pour CSV/JSON, rapport/ pour rapport.txt).
    Crée le dossier s'il n'existe pas.
    """
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    racine_projet = os.path.dirname(dossier_script)
    chemin_dossier = os.path.join(racine_projet, sous_dossier)

    os.makedirs(chemin_dossier, exist_ok=True)

    return os.path.join(chemin_dossier, nom_fichier)


def exporter_csv(patients_valides, chemin_csv):
    """
    Exporte la liste des patients valides vers un fichier CSV.
    """
    try:
        if not patients_valides:
            print("Aucun patient valide à exporter en CSV.")
            return False

        with open(chemin_csv, "w", newline="", encoding="utf-8") as fichier:
            colonnes = ["id", "nom", "prenom", "age", "telephone", "ville",
                        "groupe_sanguin", "poids", "taille"]
            writer = csv.DictWriter(fichier, fieldnames=colonnes)

            writer.writeheader()
            for patient in patients_valides:
                writer.writerow({cle: patient.get(cle, "") for cle in colonnes})

        print(f"Export CSV réussi : {chemin_csv} ({len(patients_valides)} patients)")
        return True

    except Exception as e:
        print(f"Erreur lors de l'export CSV : {e}")
        return False


def exporter_json(patients_valides, chemin_json):
    """
    Exporte la liste des patients valides vers un fichier JSON (bonus).
    """
    try:
        if not patients_valides:
            print("Aucun patient valide à exporter en JSON.")
            return False

        with open(chemin_json, "w", encoding="utf-8") as fichier:
            json.dump(patients_valides, fichier, ensure_ascii=False, indent=4)

        print(f"Export JSON réussi : {chemin_json} ({len(patients_valides)} patients)")
        return True

    except Exception as e:
        print(f"Erreur lors de l'export JSON : {e}")
        return False


def exporter_rapport(chemin_rapport, stats, raisons_rejet):
    """
    Génère le rapport texte contenant :
    - Nombre total de lignes lues, patients valides, doublons, lignes rejetées
    - Liste détaillée de chaque erreur détectée (description par patient rejeté)
    - Statistiques finales (âges, poids, ville, groupes sanguins)
    """
    try:
        if stats is None:
            print("Erreur : impossible de générer le rapport (statistiques manquantes).")
            return False

        with open(chemin_rapport, "w", encoding="utf-8") as fichier:
            ligne = "=" * 50

            fichier.write(f"{ligne}\n")
            fichier.write("RAPPORT DE NETTOYAGE - DONNEES PATIENTS\n")
            fichier.write(f"{ligne}\n")
            fichier.write(f"Date de génération : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

            # --- 1. Résumé global (nb lignes lues, valides, doublons, rejetées) ---
            fichier.write("--- RESUME GLOBAL ---\n")
            fichier.write(f"Nombre total de lignes lues (fichier brut) : {stats.get('nb_total_brut', 'N/A')}\n")
            fichier.write(f"Nombre de patients valides                  : {stats.get('nb_valides', 'N/A')}\n")
            fichier.write(f"Nombre de doublons supprimés                : {stats.get('nb_doublons', 'N/A')}\n")
            fichier.write(f"Nombre de lignes rejetées                   : {stats.get('nb_rejetes', 'N/A')}\n\n")

            # --- 2. Liste détaillée de chaque erreur détectée ---
            fichier.write(f"{ligne}\n")
            fichier.write("LISTE DETAILLEE DES ERREURS DETECTEES\n")
            fichier.write(f"{ligne}\n")

            if raisons_rejet:
                for patient_id, raison in raisons_rejet:
                    fichier.write(f"  - Patient id={patient_id} : {raison}\n")
            else:
                fichier.write("  Aucune erreur détectée, aucun patient rejeté.\n")

            fichier.write("\n")

            # --- 3. Statistiques finales ---
            fichier.write(f"{ligne}\n")
            fichier.write("STATISTIQUES FINALES\n")
            fichier.write(f"{ligne}\n")

            fichier.write(f"Moyenne des âges (patients valides)  : {stats.get('age_moyen', 'N/A')}\n")
            fichier.write(f"Moyenne des poids (patients valides)  : {stats.get('poids_moyen', 'N/A')}\n")

            ville_top = stats.get("ville_top", "N/A")
            ville_top_count = stats.get("ville_top_count", 0)
            fichier.write(f"Ville la plus fréquente                : {ville_top} ({ville_top_count} patients)\n\n")

            fichier.write("Répartition des groupes sanguins :\n")
            groupes = stats.get("groupes_sanguins", {})
            if groupes:
                for groupe, nb in groupes.items():
                    fichier.write(f"  {groupe:<5} : {nb} patient(s)\n")
            else:
                fichier.write("  Aucune donnée disponible.\n")

        print(f"Rapport généré : {chemin_rapport}")
        return True

    except Exception as e:
        print(f"Erreur lors de la génération du rapport : {e}")
        return False