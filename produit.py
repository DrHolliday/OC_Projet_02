#RI: Importation des packages necessaire au projet: 
import requests
from bs4 import BeautifulSoup
import pandas


# RI: Fonction pour récupérer infos d'une page produit ( http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html )

# •	product_page_url
# •	universal_ product_code (upc)
# •	title
# •	price_including_tax
# •	price_excluding_tax
# •	number_available
# •	product_description
# •	category
# •	review_rating
# •	image_url




def recupPageProduit():
    url = "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
    # url = input("Entrez l'url du produit")
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")

    titre = soup.find("h1")
    table = soup.find("table", class_="table table-striped")
    
    print("Titre: " + titre.text)

    #RI: Boucle pour cycler dans la table et extraire le contenu des tags: A travailler 28/03/22
    elem = []
    while elem in table:
        upc = soup.find("th", text="UPC")
        print("UPC: " , upc.find_next_sibling("td"))
        prodType = soup.find("th", text="Product Type")
        print("Product Type", prodType.find_next_sibling("td"))
        print(elem)


recupPageProduit()