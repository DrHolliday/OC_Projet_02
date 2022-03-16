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


# RI:--------------------[ TESTS DEBUT ]--------------------

# afficher le contenu qui nous intéresse: (test sur text, headers, balises etc)
# print(reponse.text)


# RI:---------------------[ TESTS FIN ]---------------------


#RI: Code de scrapping du site http://books.toscrape.com/

# RI: Je récupère les éléments qui m'intéressent "text" stocké dans ma variable "reponse":
soup = BeautifulSoup(reponse.text)

#   RI: Cette partie va rechercher les balises etc qui m'intéressent title, headers etc. 
#       le .text précise qu on veut récup uniquement en format text sans les balises  
title = soup.find("title")
print(title.text)

