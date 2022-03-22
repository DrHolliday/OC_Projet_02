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


# RI: Je récupère les éléments qui m'intéressent "text" stocké dans ma variable "reponse" utiliser un parser html.parser pour bypass erreur. 

soup = BeautifulSoup(reponse.text, "html.parser")


# RI: Boucle de récupération des catégories (tous les a) en ciblanc "ul" et sa "classe" .nav nav-list 

categories = soup.findAll("a")
for categories in soup.find("ul", class_="nav nav-list"):
    print(categories.text)


# RI: Fonction pour récupérer infos d'une page produit ( http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html )

def recupPageProduit():
    # url = "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
    url = input("Entrez l'url du produit")
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")

    titre = soup.find("h1")
    details = soup.find("table", class_="table table-striped")

    print(titre.text)
    print(url)
    print(details.text)

recupPageProduit()