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
# Nom / Prénom    →  Format titre 
# —première lettre majuscule  (Diallo)
# Téléphone →  9 chiffres sans espaces, commence par 7
# Ville     →  Orthographe standardisée, format titre
# Groupe sanguin  →  Valeurs strictement autorisées uniquement
# Poids           →  Nombre réel valide, entre 1 et 300
# Taille          →  Nombre entier valide, entre 50 et 250
# Doublons        →  Supprimer toutes les répétitions