#RI: Importation des packages necessaire au projet: 
import requests
from bs4 import BeautifulSoup
import pandas


#RI: On vérifie que le site cible réponds (par requète "get") et on affiche le code réponse ("200" attendu)
url = "http://books.toscrape.com/"
reponse = requests.get(url)

# RI: condition si le site réponds autre chose que code 200
if reponse.ok:
    print(reponse)
else:
    print("Problème avec le site voir doc code:", reponse)


#RI: Code de scrapping du site http://books.toscrape.com/

# RI: Je récupère les éléments qui m'intéressent "text" stocké dans ma variable "reponse": 
######## OK ! 22/03 --> REMARQUE RICKEL: 17/03/2022 PASSER PARAMETRE DE PARSER a beautifulSoup html.parser (A VOIR) / risque de problème d'encodage en utilisant .text

soup = BeautifulSoup(reponse.text, "html.parser")

#   RI: Cette partie va rechercher les balises etc qui m'intéressent title, headers etc. 
#       le .text précise qu on veut récup uniquement en format text sans les balises !  
title = soup.find("title")
print(title.text)

#   RI: Fonction de récupération des catégories. 
li = soup.findAll("li")
print(len(li))

# VOIR exemple ici : https://stackoverflow.com/questions/4362981/beautifulsoup-how-do-i-extract-all-the-lis-from-a-list-of-uls-that-contains
categories = soup.findAll(class_="nav nav-list")
print(len(categories))

print("stop")