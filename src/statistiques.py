# --->  calculs et statistiques apres nettoyage et validation
# Modules autorisés uniquement : pas de collections, pas de numpy, pas de pandas


def analyser_fichier_patients(patients, nb_total_brut=0, nb_doublons=0, nb_rejetes=0):
    """
    Calcule les statistiques sur la liste de patients valides.

    Paramètres :
        patients      : liste de dicts (patients valides, déjà nettoyés)
        nb_total_brut : int, nombre de lignes dans le fichier brut
        nb_doublons   : int, nombre de doublons supprimés
        nb_rejetes    : int, nombre de patients rejetés

    Retourne :
        dict de statistiques, ou None en cas d'erreur critique
    """
    try:
        stats = {}

        # 1. Nombre total de patients dans le fichier brut
        stats["nb_total_brut"] = nb_total_brut

        # 2. Nombre de patients valides après nettoyage
        stats["nb_valides"] = len(patients)

        # 3. Nombre de doublons supprimés
        stats["nb_doublons"] = nb_doublons

        # 4. Nombre de lignes rejetées
        stats["nb_rejetes"] = nb_rejetes

        # 5. Moyenne des âges des patients valides
        try:
            ages = [p["age"] for p in patients if isinstance(p["age"], int)]
            stats["age_moyen"] = round(sum(ages) / len(ages), 1) if ages else "N/A"
        except Exception as e:
            print(f"Erreur lors du calcul de la moyenne des âges : {e}")
            stats["age_moyen"] = "N/A"

        # 6. Moyenne des poids des patients valides
        try:
            poids_liste = [p["poids"] for p in patients if isinstance(p.get("poids"), (int, float))]
            stats["poids_moyen"] = round(sum(poids_liste) / len(poids_liste), 1) if poids_liste else "N/A"
        except Exception as e:
            print(f"Erreur lors du calcul de la moyenne des poids : {e}")
            stats["poids_moyen"] = "N/A"

        # 7. Ville la plus fréquente (sans Counter : dict manuel)
        try:
            comptage_villes = {}
            for p in patients:
                ville = p.get("ville", "")
                if ville != "":
                    if ville in comptage_villes:
                        comptage_villes[ville] += 1
                    else:
                        comptage_villes[ville] = 1

            if comptage_villes:
                ville_top = max(comptage_villes, key=lambda v: comptage_villes[v])
                stats["ville_top"]       = ville_top
                stats["ville_top_count"] = comptage_villes[ville_top]
            else:
                stats["ville_top"]       = "N/A"
                stats["ville_top_count"] = 0
        except Exception as e:
            print(f"Erreur lors du calcul de la ville la plus fréquente : {e}")
            stats["ville_top"]       = "N/A"
            stats["ville_top_count"] = 0

        # 8. Répartition des groupes sanguins (sans Counter : dict manuel)
        try:
            ordre_groupes = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
            comptage_groupes = {g: 0 for g in ordre_groupes}

            for p in patients:
                groupe = p.get("groupe_sanguin", "")
                if groupe in comptage_groupes:
                    comptage_groupes[groupe] += 1

            stats["groupes_sanguins"] = comptage_groupes
        except Exception as e:
            print(f"Erreur lors du calcul des groupes sanguins : {e}")
            stats["groupes_sanguins"] = {}

        return stats

    except Exception as e:
        print(f"Erreur critique lors de l'analyse des statistiques : {e}")
        return None


def afficher_statistiques(stats):
    """
    Affiche toutes les statistiques demandées dans le terminal.
    """
    try:
        if stats is None:
            print("Erreur : aucune statistique à afficher.")
            return

        ligne = "=" * 46

        print(f"\n{ligne}")
        print("    STATISTIQUES DES DONNÉES MÉDICALES")
        print(f"{ligne}")

        # 1. Total brut
        try:
            print(f"\n  Patients dans le fichier brut  : {stats['nb_total_brut']}")
        except KeyError:
            print("\n  Patients dans le fichier brut  : N/A")

        # 2. Valides
        try:
            print(f"  Patients valides               : {stats['nb_valides']}")
        except KeyError:
            print("  Patients valides               : N/A")

        # 3. Doublons
        try:
            print(f"  Doublons supprimés             : {stats['nb_doublons']}")
        except KeyError:
            print("  Doublons supprimés             : N/A")

        # 4. Rejetés
        try:
            print(f"  Lignes rejetées                : {stats['nb_rejetes']}")
        except KeyError:
            print("  Lignes rejetées                : N/A")

        # 5. Moyenne des âges
        try:
            age_aff = stats['age_moyen']
            if isinstance(age_aff, (int, float)):
                age_aff = f"{age_aff:.1f} ans"
            print(f"\n  Moyenne des âges               : {age_aff}")
        except KeyError:
            print("\n  Moyenne des âges               : N/A")

        # 6. Moyenne des poids
        try:
            poids_aff = stats['poids_moyen']
            if isinstance(poids_aff, (int, float)):
                poids_aff = f"{poids_aff:.1f} kg"
            print(f"  Moyenne des poids              : {poids_aff}")
        except KeyError:
            print("  Moyenne des poids              : N/A")

        # 7. Ville la plus fréquente
        try:
            print(f"\n  Ville la plus fréquente        : {stats['ville_top']} ({stats['ville_top_count']} patients)")
        except KeyError:
            print("\n  Ville la plus fréquente        : N/A")

        # 8. Répartition groupes sanguins
        try:
            print(f"\n{'─' * 46}")
            print("  RÉPARTITION DES GROUPES SANGUINS")
            print(f"{'─' * 46}")
            groupes = stats["groupes_sanguins"]
            if groupes:
                for groupe, count in groupes.items():
                    print(f"    {groupe:<5} : {count} patient(s)")
            else:
                print("    Aucun groupe sanguin disponible.")
        except KeyError:
            print("  Groupes sanguins               : N/A")

        print(f"\n{ligne}\n")

    except Exception as e:
        print(f"Erreur lors de l'affichage des statistiques : {e}")


def calculer_statistiques(patients_valides):
    try:
        stats_brutes = analyser_fichier_patients(patients=patients_valides)

        return {
            "nb_valides"         : stats_brutes.get("nb_valides", 0),
            "moyenne_age"        : stats_brutes.get("age_moyen", 0),
            "moyenne_poids"      : stats_brutes.get("poids_moyen", 0),
            "ville_freq"         : stats_brutes.get("ville_top", "N/A"),
            "repartition_groupes": stats_brutes.get("groupes_sanguins", {}),
        }

    except Exception as e:
        print(f"Erreur dans calculer_statistiques : {e}")
        return {}