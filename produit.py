#RI: Importation des packages necessaire au projet: 
import requests
from bs4 import BeautifulSoup
import pandas


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