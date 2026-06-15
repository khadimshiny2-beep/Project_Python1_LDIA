import os
from datetime import datetime


def obtenir_chemin_log(nom_fichier="application.log"):
    """
    Construit le chemin absolu vers le fichier de log,
    dans un dossier logs/ à la racine du projet.
    Crée le dossier s'il n'existe pas.
    """
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    racine_projet = os.path.dirname(dossier_script)
    chemin_dossier = os.path.join(racine_projet, "logs")

    os.makedirs(chemin_dossier, exist_ok=True)

    return os.path.join(chemin_dossier, nom_fichier)


CHEMIN_LOG = obtenir_chemin_log()


def log(message, niveau="INFO"):
    """
    Ajoute une ligne horodatée au fichier de log.
    Niveaux possibles : INFO, AVERTISSEMENT, ERREUR
    """
    try:
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ligne = f"[{horodatage}] [{niveau}] {message}\n"

        with open(CHEMIN_LOG, "a", encoding="utf-8") as fichier:
            fichier.write(ligne)

    except Exception as e:
        print(f"Erreur lors de l'écriture du log : {e}")


def log_info(message):
    log(message, "INFO")


def log_avertissement(message):
    log(message, "AVERTISSEMENT")


def log_erreur(message):
    log(message, "ERREUR")


def log_separateur_session():
    """
    Marque le début d'une nouvelle session dans le fichier de log.
    """
    try:
        with open(CHEMIN_LOG, "a", encoding="utf-8") as fichier:
            fichier.write("\n" + "=" * 60 + "\n")
            fichier.write(f"NOUVELLE SESSION - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            fichier.write("=" * 60 + "\n")
    except Exception as e:
        print(f"Erreur lors de l'écriture du log : {e}")