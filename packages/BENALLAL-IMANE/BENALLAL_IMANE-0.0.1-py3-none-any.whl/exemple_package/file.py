#Écriture initiale dans le fichier :
with open("imane.txt","w")as f:
    f.write("je m'appelle imane benaallal\n")
    f.write("j'ai 23 ans ")

#Ajout de contenu dans le fichier 
with open("imane.txt","a")as f:
    f.write("et je suis photographe")

#Lecture du contenu du fichier
with open("imane.txt","r") as f:
    print(f.read())