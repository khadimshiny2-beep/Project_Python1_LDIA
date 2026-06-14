from chargement import charger_donnees, obtenir_chemin_donnees, creation_dictionnaire_patients
from nettoyage import nettoyer_tous_les_patients, nettoyer_doublons
from validation import filtrer_patients_valides
from export import exporter_csv, exporter_json, exporter_rapport, obtenir_chemin_sortie

# Import des statistiques avec fallback si le module n'est pas encore prêt
try:
    from statistiques import calculer_statistiques
except ImportError:
    def calculer_statistiques(patients_valides):
        """Version temporaire en attendant le module statistiques.py"""
        return {
            "nb_valides": len(patients_valides),
            "moyenne_age": 0,
            "moyenne_poids": 0,
            "ville_freq": "N/A",
            "repartition_groupes": {},
        }


# ---------- ETAT GLOBAL DU PROGRAMME ----------
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


# ---------- OPTION 1 : CHARGER ----------
def option_charger():
    chemin = obtenir_chemin_donnees("patients_bruts.txt")
    etat["lignes_brutes"] = charger_donnees(chemin)

    if not etat["lignes_brutes"]:
        print("Aucune donnée chargée. Vérifie le chemin du fichier.")
        return

    patients, nb_invalides = creation_dictionnaire_patients(etat["lignes_brutes"])
    etat["patients"] = patients
    etat["nb_invalides_parsing"] = nb_invalides
    etat["charge"] = True
    etat["nettoye"] = False  # reset si on recharge

    print(f"\n{len(etat['lignes_brutes'])} lignes chargées, {len(patients)} patients créés.")


# ---------- OPTION 2 : AFFICHER LES ANOMALIES ----------
def option_anomalies():
    if not etat["charge"]:
        print("Veuillez d'abord charger les données (option 1).")
        return

    print("\n--- ANOMALIES DETECTEES (avant nettoyage) ---")
    groupes_valides = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}

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

        # Téléphone (avant nettoyage)
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
            print(f"  Patient id={p['id']} : {', '.join(anomalies)}")

    print("--- Fin de la liste des anomalies ---")


# ---------- OPTION 3 : NETTOYER ----------
def option_nettoyer():
    if not etat["charge"]:
        print("Veuillez d'abord charger les données (option 1).")
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

    print(f"\nNettoyage terminé : {len(patients_valides)} patients valides, "
          f"{nb_doublons} doublons supprimés, {len(patients_rejetes)} rejetés.")


# ---------- OPTION 4 : STATISTIQUES ----------
def option_statistiques():
    if not etat["nettoye"]:
        print("Veuillez d'abord nettoyer les données (option 3).")
        return

    stats = calculer_statistiques(etat["patients_valides"])
    etat["stats"] = stats

    print("\n--- STATISTIQUES ---")
    print(f"Patients valides       : {stats.get('nb_valides', 0)}")
    print(f"Moyenne des âges        : {stats.get('moyenne_age', 0):.2f}")
    print(f"Moyenne des poids        : {stats.get('moyenne_poids', 0):.2f}")
    print(f"Ville la plus fréquente  : {stats.get('ville_freq', 'N/A')}")
    print("Répartition des groupes sanguins :")
    for groupe, nb in stats.get("repartition_groupes", {}).items():
        print(f"  {groupe} : {nb}")


# ---------- OPTION 5 : EXPORTER ----------
def option_exporter():
    if not etat["nettoye"]:
        print("Veuillez d'abord nettoyer les données (option 3).")
        return

    if not etat["stats"]:
        etat["stats"] = calculer_statistiques(etat["patients_valides"])

    chemin_csv = obtenir_chemin_sortie("patients_propres.csv", "data")
    chemin_json = obtenir_chemin_sortie("patients_propres.json", "data")
    chemin_rapport = obtenir_chemin_sortie("rapport.txt", "rapport")

    exporter_csv(etat["patients_valides"], chemin_csv)
    exporter_json(etat["patients_valides"], chemin_json)
    exporter_rapport(
        chemin_rapport, 
        etat["stats"], 
        etat["raisons_rejet"],
    )

    print("\nExport terminé (CSV, JSON, rapport).")


# ---------- MENU PRINCIPAL ----------
def afficher_menu():
    print("\n============================================")
    print(" SYSTEME DE NETTOYAGE DE DONNEES MEDICALES")
    print("============================================")
    print("1. Charger les données brutes")
    print("2. Afficher les anomalies détectées")
    print("3. Nettoyer les données")
    print("4. Afficher les statistiques")
    print("5. Exporter les données propres")
    print("6. Quitter")


def main():
    while True:
        afficher_menu()
        choix = input("Choix : ").strip()

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
            print("Au revoir !")
            break
        else:
            print("Choix invalide, veuillez entrer un nombre entre 1 et 6.")


if __name__ == "__main__":
    main()