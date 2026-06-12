# ---> Doit contenir le menu 
#         ============================================
#           SYSTÈME DE NETTOYAGE DE DONNÉES MÉDICALES
#            ============================================
# 1. Charger les données brutes
# 2. Afficher les anomalies détectées
# 3. Nettoyer les données
# 4. Afficher les statistiques
# 5. Exporter les données propres
# 6. Quitter
# Choix :

from chargement import charger_donnees, obtenir_chemin_donnees

chemin = obtenir_chemin_donnees("patients_bruts.txt")
donnees = charger_donnees(chemin)
chemin1 = obtenir_chemin_donnees("patients_propres.csv")
