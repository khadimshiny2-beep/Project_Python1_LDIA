# statistiques.py
# Aucun import de collections ici !

def analyser_fichier_patients(patients, nb_total_brut=0, nb_doublons=0, nb_rejetes=0):
    """
    Calcule les statistiques sur la liste de patients valides en Python pur.
    """
    try:
        stats = {}

        # 1. Comptes généraux
        stats["nb_total_brut"] = nb_total_brut
        stats["nb_valides"] = len(patients)
        stats["nb_doublons"] = nb_doublons
        stats["nb_rejetes"] = nb_rejetes

        # 2. Moyenne des âges
        ages = []
        for p in patients:
            try:
                ages.append(int(str(p["age"]).strip()))
            except (ValueError, KeyError):
                pass
        stats["age_moyen"] = round(sum(ages) / len(ages), 1) if ages else "N/A"

        # 3. Moyenne des poids
        poids_liste = []
        for p in patients:
            try:
                poids_liste.append(float(str(p["poids"]).strip()))
            except (ValueError, KeyError):
                pass
        stats["poids_moyen"] = round(sum(poids_liste), 1) if poids_liste else "N/A"

        # 4. Ville la plus fréquente (Algorithme avec dictionnaire standard)
        compteur_villes = {}
        for p in patients:
            ville = p.get("ville", "").strip()
            if ville:
                # Si la ville existe déjà, on incrémente, sinon on l'initialise à 1
                compteur_villes[ville] = compteur_villes.get(ville, 0) + 1

        # Recherche du maximum manuellement
        if compteur_villes:
            ville_top = None
            max_contacts = -1
            for ville, nb in compteur_villes.items():
                if nb > max_contacts:
                    max_contacts = nb
                    ville_top = ville
            
            stats["ville_top"] = ville_top
            stats["ville_top_count"] = max_contacts
        else:
            stats["ville_top"] = "N/A"
            stats["ville_top_count"] = 0

        # 5. Répartition des groupes sanguins (Algorithme avec dictionnaire standard)
        compteur_groupes = {}
        for p in patients:
            groupe = p.get("groupe_sanguin", "").strip().upper()
            if groupe:
                compteur_groupes[groupe] = compteur_groupes.get(groupe, 0) + 1
        
        stats["groupes_sanguins"] = compteur_groupes

        return stats
    except Exception as e:
        print(f"Erreur lors de l'analyse des statistiques : {e}")
        return {}


def calculer_statistiques(patients_valides):
    """
    Fonction principale appelée par le menu Option 4 de main.py
    """
    try:
        stats_brutes = analyser_fichier_patients(patients=patients_valides)

        return {
            "nb_valides"         : stats_brutes.get("nb_valides", len(patients_valides)),
            "moyenne_age"        : stats_brutes.get("age_moyen", 0),
            "moyenne_poids"      : stats_brutes.get("poids_moyen", 0),
            "ville_freq"         : stats_brutes.get("ville_top", "N/A"),
            "repartition_groupes": stats_brutes.get("groupes_sanguins", {}),
        }
    except Exception as e:
        print(f"Erreur dans calculer_statistiques : {e}")
        return {
            "nb_valides": len(patients_valides),
            "moyenne_age": 0,
            "moyenne_poids": 0,
            "ville_freq": "N/A",
            "repartition_groupes": {},
        }


def afficher_statistiques(stats):
    """
    Affiche proprement les résultats dans la console
    """
    if not stats:
        print("Aucune statistique à afficher.")
        return

    ligne = "═" * 50
    print(f"\n{ligne}\n  RÉSULTATS STATISTIQUES DES PATIENTS VALIDES\n{ligne}")
    print(f"  Nombre de patients valides     : {stats.get('nb_valides', 0)}")
    print(f"  Moyenne d'âge                  : {stats.get('moyenne_age', 'N/A')} ans")
    print(f"  Moyenne de poids               : {stats.get('moyenne_poids', 'N/A')} kg")
    print(f"  Ville la plus fréquente        : {stats.get('ville_freq', 'N/A')}")
    print(f"\n  Répartition des groupes sanguins :")
    
    for groupe, count in stats.get("repartition_groupes", {}).items():
        print(f"    {groupe:<5} : {count} patient(s)")
    print(f"{ligne}\n")