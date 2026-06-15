# Projet Python 1 — Prétraitement et Nettoyage de Données Médicales

**Université ROSE DIENG FRANCE-SÉNÉGAL**
Année académique 2025-2026
Programmation Python 1

## Membres du binôme

- [Gueye Ahmadoul Khadim]
- [Adji Fatouma]

## Description du projet

Une clinique médicale dispose d'un fichier de données patients (`patients_bruts.txt`) collecté depuis plusieurs sources sur plusieurs années. Ce fichier contient de nombreuses anomalies : espaces inutiles, fautes de frappe, valeurs manquantes, doublons, formats incohérents, etc.

Ce programme lit ce fichier brut, détecte les anomalies, nettoie les données, valide chaque patient selon des règles strictes, calcule des statistiques et exporte un dataset final exploitable (CSV et JSON).

## Structure du projet

```
projet_python/
├── data/
│   ├── patients_bruts.txt
│   ├── patients_propres.csv
│   └── patients_propres.json
├── src/
│   ├── main.py             
│   ├── chargement.py      
│   ├── nettoyage.py       
│   ├── validation.py       
│   ├── statistiques.py     
│   ├──export.py          
├── rapport/
│   └── rapport.txt
└── README.md
```

## Fonctionnement

Le programme s'exécute en mode console via un menu interactif :

```
============================================
 SYSTÈME DE NETTOYAGE DE DONNÉES MÉDICALES
============================================
1. Charger les données brutes
2. Afficher les anomalies détectées
3. Nettoyer les données
4. Afficher les statistiques
5. Exporter les données propres
6. Quitter
```


## 📝 Système de Journalisation (Logs)

Le projet intègre désormais un système de suivi (logging) personnalisé qui enregistre automatiquement le déroulement des opérations, les anomalies rencontrées et les erreurs système. Cela permet de garder un historique des exécutions sans encombrer la console de l'utilisateur.

### 🗂️ Structure et Emplacement
À la première exécution du programme, un dossier `logs/` est automatiquement créé à la racine du projet s'il n'existe pas.
* **Fichier généré :** `logs/application.log`
* **Encodage :** UTF-8

### ⚙️ Fonctionnalités des Logs
* **Séparateur de session :** Chaque démarrage de l'application inscrit un bloc visuel indiquant la date et l'heure de la `NOUVELLE SESSION`.
* **Niveaux de gravité :**
  * `[INFO]` : Suivi des étapes clés réussies (ex: démarrage, chargement de X lignes, fin d'un export).
  * `[AVERTISSEMENT]` : Alertes non critiques (ex: lignes ignorées au parsing, doublons détectés, patients rejetés lors du nettoyage).
  * `[ERREUR]` : Problèmes bloquants ou actions impossibles (ex: tentative de nettoyage sans données chargées, fichier introuvable, échec d'écriture).

### 📄 Exemple de rendu dans `application.log`

```text
============================================================
NOUVELLE SESSION - 15/06/2026 14:15:36
============================================================
[2026-06-15 14:15:36] [INFO] Programme démarré
[2026-06-15 14:15:42] [INFO] Chargement réussi : 150 lignes lues, 142 patients créés
[2026-06-15 14:15:42] [AVERTISSEMENT] 8 lignes ignorées au parsing (format invalide)
[2026-06-15 14:15:50] [INFO] Nettoyage terminé : 130 valides, 2 doublons supprimés, 10 rejetés
[2026-06-15 14:15:50] [AVERTISSEMENT] Patient id=42 rejeté : âge irréaliste (>120)
[2026-06-15 14:16:05] [INFO] Export terminé : CSV, JSON et rapport générés (130 patients exportés)
```

### Détail des traitements

1. **Chargement** : lecture du fichier `patients_bruts.txt`, découpage de chaque ligne (`;`) et création d'un dictionnaire par patient.
2. **Anomalies** : analyse des données brutes et affichage de chaque anomalie détectée (âge invalide, téléphone mal formaté, groupe sanguin incorrect, poids/taille non numériques, etc.).
3. **Nettoyage** :
   - Noms et prénoms : suppression des espaces (y compris invisibles) et mise en format titre.
   - Téléphones : suppression des espaces, tirets et préfixes internationaux (`+221`, `00221`), validation du format `7XXXXXXXX`.
   - Villes : mise en format titre et **correction automatique** des fautes de frappe via la distance de Levenshtein (bonus).
   - Suppression des doublons exacts et quasi-doublons.
4. **Validation** : chaque patient est vérifié (âge, groupe sanguin, poids, taille, nom/prénom, téléphone). Tout patient ne respectant pas une règle est rejeté avec une raison précise.
5. **Statistiques** : nombre de patients (brut, valides, doublons, rejetés), moyenne des âges, moyenne des poids, ville la plus fréquente, répartition des groupes sanguins.
6. **Export** :
   - `patients_propres.csv` : dataset final nettoyé et validé.
   - `patients_propres.json` : export bonus au format JSON.
   - `rapport.txt` : statistiques globales, liste détaillée des erreurs par patient rejeté, statistiques finales.

## Règles de nettoyage et de rejet

| Champ | Règle de nettoyage | Cause de rejet |
|---|---|---|
| Nom / Prénom | Format titre, espaces supprimés | Champ vide après nettoyage |
| Téléphone | 9 chiffres, sans espaces/tirets, préfixe international supprimé | Format invalide après nettoyage |
| Ville | Format titre, orthographe corrigée automatiquement | — |
| Groupe sanguin | — | Hors de A+, A-, B+, B-, AB+, AB-, O+, O- |
| Âge | Converti en entier | Manquant, négatif ou supérieur à 120 |
| Poids | Converti en réel | Manquant, "N/A", non numérique, hors [1, 300] |
| Taille | Convertie en entier | Manquante, "N/A", non numérique, hors [50, 250] |

## Fonctionnalités bonus implémentées

- Export au format JSON en plus du CSV
- Correction automatique des villes par distance de Levenshtein

## Contraintes techniques respectées

- Python standard uniquement (modules `csv`, `re`, `json`, `datetime`, `os`)
- Aucune bibliothèque externe de data science (pas de NumPy, pas de Pandas)
- Gestion des exceptions avec `try/except` dans toutes les fonctions sensibles
- Code organisé en modules et fonctions séparées, commenté
- Le programme ne crashe jamais, quelles que soient les données saisies

## Exécution

Depuis le dossier `src/` :

```bash
python main.py
```

Le programme affiche le menu et attend un choix entre 1 et 6.

## Difficultés rencontrées

[ gestion des espaces insécables, choix du seuil de correction automatique des villes, ordre des étapes nettoyage/doublons/validation, 
Chainage d'appel du programme,
Entrée et sortie des différentes fonctions,]
