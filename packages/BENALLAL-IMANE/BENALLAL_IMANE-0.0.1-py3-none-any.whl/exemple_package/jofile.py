import json

# Lecture des données JSON depuis un fichier
with open("personnel.json", "r") as fichier_json:
    donnees_json = fichier_json.read()

# Conversion des données JSON en un dictionnaire
personne_recuperee = json.loads(donnees_json)

# Affichage des données récupérées
print(personne_recuperee)