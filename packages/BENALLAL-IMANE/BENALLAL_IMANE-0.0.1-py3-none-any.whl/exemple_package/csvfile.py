import csv

# Données initiales sur les hôtels
hotels_data = [
    ["ID", "Nom de l'hôtel", "Prix chambre", "Disponibilité"],
    ["1", "Hôtel Luxe", "200", "15"],
    ["2", "Auberge Charme", "150", "20"],
    ["3", "Résidence Vue Mer", "300", "10"]
]

# Nouvelles données sur d'autres hôtels
new_hotels_data = [
    ["4", "Hôtel Montagnard", "180", "12"],
    ["5", "Pension Jardin", "120", "25"],
    ["6", "Spa & Resort", "250", "8"]
]

# Nom du fichier CSV
filename_hotel = "hotel.csv"

# Écriture des données initiales
with open(filename_hotel, 'w', newline='') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerows(hotels_data)

# Augmenter le prix de chaque chambre de 15%
with open(filename_hotel, 'r') as f:
    csvreader = csv.reader(f)
    data = list(csvreader)

for row in data[1:]:  # Ignorer l'en-tête
    room_price = float(row[2])
    new_room_price = room_price * 1.15  # Augmenter de 15%
    row[2] = "{:.2f}".format(new_room_price)  # Formater le prix avec deux décimales

# Nom du fichier CSV à écrire
filename_hotel_modified = "hotel_modifie.csv"

# Écrire les données modifiées dans un nouveau fichier CSV
with open(filename_hotel_modified, 'w', newline='') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerows(data)

# Afficher les données modifiées
with open(filename_hotel_modified, 'r') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        print(row)