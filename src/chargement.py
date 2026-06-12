# ---> Lire les fichiers 'patients_bruts.txt' et 'patients_propres.csv'
# ---> Lire le nombre total de lignes dans le fichier 'patients_bruts.txt'

import os

def obtenir_chemin_donnees(nom_fichier):
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    racine_projet = os.path.dirname(dossier_script)
    return os.path.join(racine_projet, "data", nom_fichier)


def charger_donnees(chemin_fichier):
    """
    Lit le fichier de données brutes et retourne une liste de lignes.
    Gère les erreurs si le fichier est introuvable ou illisible.
    """
    lignes = []
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as fichier:
            for ligne in fichier:
                ligne = ligne.strip()  
                if ligne != "":        
                    lignes.append(ligne)
        print(f"Chargement réussi : {len(lignes)} lignes lues depuis '{chemin_fichier}'.")
    except FileNotFoundError:
        print(f"Erreur : le fichier '{chemin_fichier}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur inattendue lors du chargement : {e}")

    return lignes