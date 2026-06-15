from chargement import charger_donnees, obtenir_chemin_donnees, creation_dictionnaire_patients
from nettoyage import nettoyer_tous_les_patients, nettoyer_doublons
from validation import filtrer_patients_valides
from export import exporter_csv, exporter_json, exporter_rapport, obtenir_chemin_sortie

try:
    from statistiques import calculer_statistiques
except ImportError:
    def calculer_statistiques(patients_valides):
        return {
            "nb_valides": len(patients_valides),
            "moyenne_age": 0,
            "moyenne_poids": 0,
            "ville_freq": "N/A",
            "repartition_groupes": {},
        }


# ══════════════════════════════════════════════
#               COULEURS ANSI
# ══════════════════════════════════════════════
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"

    # Textes
    BLANC   = "\033[97m"
    GRIS    = "\033[90m"
    ROUGE   = "\033[91m"
    VERT    = "\033[92m"
    JAUNE   = "\033[93m"
    BLEU    = "\033[94m"
    VIOLET  = "\033[95m"
    CYAN    = "\033[96m"

    # Fonds
    FD_BLEU    = "\033[44m"
    FD_VERT    = "\033[42m"
    FD_ROUGE   = "\033[41m"
    FD_JAUNE   = "\033[43m"
    FD_VIOLET  = "\033[45m"

def titre(texte):
    largeur = 50
    print(f"\n{C.FD_BLEU}{C.BLANC}{C.BOLD}{'═' * largeur}{C.RESET}")
    print(f"{C.FD_BLEU}{C.BLANC}{C.BOLD}  {texte.center(largeur - 2)}{C.RESET}")
    print(f"{C.FD_BLEU}{C.BLANC}{C.BOLD}{'═' * largeur}{C.RESET}")

def separateur(couleur=C.GRIS):
    print(f"{couleur}{'─' * 50}{C.RESET}")

def succes(texte):
    print(f"{C.VERT}  ✔  {texte}{C.RESET}")

def erreur(texte):
    print(f"{C.ROUGE}  ✘  {texte}{C.RESET}")

def info(texte):
    print(f"{C.CYAN}  ➜  {texte}{C.RESET}")

def avertissement(texte):
    print(f"{C.JAUNE}  ⚠  {texte}{C.RESET}")


# ══════════════════════════════════════════════
#               ÉTAT GLOBAL
# ══════════════════════════════════════════════
etat = {
    "lignes_brutes": [],
    "nb_invalides_parsing": 0,
    "patients": [],
    "nb_doublons": 0,
    "patients_valides": [],
    "patients_rejetes": [],
    "raisons_rejet": [],
    "stats": {},
    "charge": False,
    "nettoye": False,
}


# ══════════════════════════════════════════════
#          OPTION 1 : CHARGER
# ══════════════════════════════════════════════
def option_charger():
    titre("CHARGEMENT DES DONNÉES")

    chemin = obtenir_chemin_donnees("patients_bruts.txt")
    etat["lignes_brutes"] = charger_donnees(chemin)

    if not etat["lignes_brutes"]:
        erreur("Aucune donnée chargée. Vérifie le chemin du fichier.")
        return

    patients, nb_invalides = creation_dictionnaire_patients(etat["lignes_brutes"])
    etat["patients"] = patients
    etat["nb_invalides_parsing"] = nb_invalides
    etat["charge"] = True
    etat["nettoye"] = False

    separateur(C.VERT)
    succes(f"{len(etat['lignes_brutes'])} lignes lues depuis le fichier brut")
    succes(f"{len(patients)} patients créés avec succès")
    if nb_invalides > 0:
        avertissement(f"{nb_invalides} lignes ignorées (format invalide)")


# ══════════════════════════════════════════════
#          OPTION 2 : ANOMALIES
# ══════════════════════════════════════════════
def option_anomalies():
    titre("ANOMALIES DÉTECTÉES")

    if not etat["charge"]:
        erreur("Veuillez d'abord charger les données (option 1).")
        return

    groupes_valides = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}
    nb_anomalies = 0

    for p in etat["patients"]:
        anomalies = []

        # Age
        age = p["age"].strip()
        if age == "":
            anomalies.append("âge manquant")
        else:
            try:
                age_int = int(age)
                if age_int < 0:
                    anomalies.append("âge négatif")
                elif age_int > 120:
                    anomalies.append("âge irréaliste (>120)")
                elif age_int == 0:
                    anomalies.append("âge égal à 0 (suspect)")
            except ValueError:
                anomalies.append("âge non numérique")

        # Téléphone
        tel = p["telephone"].strip().replace(" ", "").replace("-", "")
        if tel.startswith("+221") or tel.startswith("00221"):
            anomalies.append("préfixe international à supprimer")

        # Groupe sanguin
        if p["groupe_sanguin"].strip() not in groupes_valides:
            anomalies.append(f"groupe sanguin invalide ({p['groupe_sanguin']})")

        # Poids / taille
        for champ, nom_champ in [("poids", "poids"), ("taille", "taille")]:
            valeur = p[champ].strip()
            if valeur == "" or valeur.upper() == "N/A":
                anomalies.append(f"{nom_champ} manquant")
            else:
                try:
                    float(valeur)
                except ValueError:
                    anomalies.append(f"{nom_champ} non numérique ({valeur})")

        if anomalies:
            nb_anomalies += 1
            print(f"  {C.JAUNE}Patient id={p['id']}{C.RESET} : {C.ROUGE}{', '.join(anomalies)}{C.RESET}")

    separateur(C.CYAN)
    if nb_anomalies == 0:
        succes("Aucune anomalie détectée.")
    else:
        avertissement(f"{nb_anomalies} patient(s) avec anomalie(s) détecté(s)")


# ══════════════════════════════════════════════
#          OPTION 3 : NETTOYER
# ══════════════════════════════════════════════
def option_nettoyer():
    titre("NETTOYAGE DES DONNÉES")

    if not etat["charge"]:
        erreur("Veuillez d'abord charger les données (option 1).")
        return

    nettoyer_tous_les_patients(etat["patients"])

    patients_sans_doublons, nb_doublons = nettoyer_doublons(etat["patients"])
    etat["patients"] = patients_sans_doublons
    etat["nb_doublons"] = nb_doublons

    patients_valides, patients_rejetes, raisons = filtrer_patients_valides(etat["patients"])
    etat["patients_valides"] = patients_valides
    etat["patients_rejetes"] = patients_rejetes
    etat["raisons_rejet"] = raisons
    etat["nettoye"] = True

    separateur(C.VERT)
    succes(f"{len(patients_valides)} patients valides après nettoyage")
    if nb_doublons > 0:
        avertissement(f"{nb_doublons} doublon(s) supprimé(s)")
    if len(patients_rejetes) > 0:
        erreur(f"{len(patients_rejetes)} patient(s) rejeté(s)")


# ══════════════════════════════════════════════
#          OPTION 4 : STATISTIQUES
# ══════════════════════════════════════════════
def option_statistiques():
    titre("STATISTIQUES")

    if not etat["nettoye"]:
        erreur("Veuillez d'abord nettoyer les données (option 3).")
        return

    stats = calculer_statistiques(etat["patients_valides"])
    etat["stats"] = stats

    separateur(C.CYAN)
    print(f"  {C.BOLD}{C.BLANC}Patients valides        {C.RESET}: {C.VERT}{stats.get('nb_valides', 0)}{C.RESET}")
    print(f"  {C.BOLD}{C.BLANC}Moyenne des âges        {C.RESET}: {C.CYAN}{stats.get('moyenne_age', 0):.2f} ans{C.RESET}")
    print(f"  {C.BOLD}{C.BLANC}Moyenne des poids       {C.RESET}: {C.CYAN}{stats.get('moyenne_poids', 0):.2f} kg{C.RESET}")
    print(f"  {C.BOLD}{C.BLANC}Ville la plus fréquente {C.RESET}: {C.VIOLET}{stats.get('ville_freq', 'N/A')}{C.RESET}")

    separateur(C.CYAN)
    print(f"  {C.BOLD}{C.BLANC}RÉPARTITION DES GROUPES SANGUINS{C.RESET}")
    separateur(C.GRIS)

    for groupe, nb in stats.get("repartition_groupes", {}).items():
        barre = "█" * nb
        print(f"    {C.JAUNE}{groupe:<5}{C.RESET}: {C.VERT}{nb:>3}{C.RESET}  {C.BLEU}{barre}{C.RESET}")


# ══════════════════════════════════════════════
#          OPTION 5 : EXPORTER
# ══════════════════════════════════════════════
def option_exporter():
    titre("EXPORT DES DONNÉES")

    if not etat["nettoye"]:
        erreur("Veuillez d'abord nettoyer les données (option 3).")
        return

    if not etat["stats"]:
        etat["stats"] = calculer_statistiques(etat["patients_valides"])

    chemin_csv     = obtenir_chemin_sortie("patients_propres.csv", "data")
    chemin_json    = obtenir_chemin_sortie("patients_propres.json", "data")
    chemin_rapport = obtenir_chemin_sortie("rapport.txt", "rapport")

    exporter_csv(etat["patients_valides"], chemin_csv)
    exporter_json(etat["patients_valides"], chemin_json)
    exporter_rapport(chemin_rapport, etat["stats"], etat["raisons_rejet"])

    separateur(C.VERT)
    succes(f"CSV     → {chemin_csv}")
    succes(f"JSON    → {chemin_json}")
    succes(f"Rapport → {chemin_rapport}")


# ══════════════════════════════════════════════
#               MENU PRINCIPAL
# ══════════════════════════════════════════════
def afficher_menu():
    # Indicateurs d'état
    etat_charge  = f"{C.VERT}✔ chargé{C.RESET}"  if etat["charge"]  else f"{C.ROUGE}✘ non chargé{C.RESET}"
    etat_nettoye = f"{C.VERT}✔ nettoyé{C.RESET}" if etat["nettoye"] else f"{C.ROUGE}✘ non nettoyé{C.RESET}"

    print(f"\n{C.FD_BLEU}{C.BLANC}{C.BOLD}{'═' * 50}{C.RESET}")
    print(f"{C.FD_BLEU}{C.BLANC}{C.BOLD}{'SYSTÈME DE NETTOYAGE DE DONNÉES MÉDICALES'.center(50)}{C.RESET}")
    print(f"{C.FD_BLEU}{C.BLANC}{C.BOLD}{'═' * 50}{C.RESET}")
    print(f"  Données : {etat_charge}   Nettoyage : {etat_nettoye}")
    separateur(C.GRIS)
    print(f"  {C.CYAN}{C.BOLD}1.{C.RESET}  Charger les données brutes")
    print(f"  {C.CYAN}{C.BOLD}2.{C.RESET}  Afficher les anomalies détectées")
    print(f"  {C.CYAN}{C.BOLD}3.{C.RESET}  Nettoyer les données")
    print(f"  {C.CYAN}{C.BOLD}4.{C.RESET}  Afficher les statistiques")
    print(f"  {C.CYAN}{C.BOLD}5.{C.RESET}  Exporter les données propres")
    print(f"  {C.ROUGE}{C.BOLD}6.{C.RESET}  Quitter")
    separateur(C.GRIS)


def main():
    while True:
        afficher_menu()
        choix = input(f"  {C.BOLD}Choix : {C.RESET}").strip()

        if choix == "1":
            option_charger()
        elif choix == "2":
            option_anomalies()
        elif choix == "3":
            option_nettoyer()
        elif choix == "4":
            option_statistiques()
        elif choix == "5":
            option_exporter()
        elif choix == "6":
            print(f"\n{C.VERT}{C.BOLD}  Au revoir !{C.RESET}\n")
            break
        else:
            erreur("Choix invalide. Entrez un nombre entre 1 et 6.")


if __name__ == "__main__":
    main()