#RI: Importation des packages necessaire au projet: 
from textwrap import indent
import requests
#BSA pour beautifullsoup et requete sur tag html etc.
from bs4 import BeautifulSoup
import pandas as pd
# os pour la creation de dossier ( images)
import os

# ---- A FAIRE ------------------------------------------
# •	ok product_page_url
# •	ok universal_ product_code (upc)
# •	ok title
# •	ok price_including_tax
# •	ok price_excluding_tax
# •	ok number_available 
# •	ok product_description
# •	ok category
# •	ok review_rating
# •	ok image_url
# -- Dossier Image et sauvegarde jpg
# -- Dataframe du produit


# RI: Fonction pour récupérer infos d'une page produit et enregistrer dans une liste

def recupPageProduit():
    url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")

    #RI: Récupération des parties qui m'intéressent et l'afficher/stocker:
    productPageUrl = url
    prodType = soup.find("th", text="Product Type").find_next_sibling("td").text.strip()
    upc = soup.find("th", text="UPC").find_next_sibling("td").text.strip()
    titre = soup.find("h1").text.strip()
    prixSansTaxe = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").text.strip()
    prixAvecTaxe = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").text.strip()
    disponibilite = soup.find("th", text="Availability").find_next_sibling("td").text.strip()
    description = soup.find("div", id="product_description").find_next_sibling("p").text.strip()
    categorie = soup.find("ul", class_="breadcrumb").findChildren()[4].find("a").text.strip()
    reviews = soup.find("th", text="Number of reviews").find_next_sibling("td").text.strip()
    image = soup.find("div", class_="item active").find("img").get("src")

    #RI : Vérification dossier images (création si non existant) Sauvegarde de l illustration dans le dossier
    dossierImages = "images"
    isExist = os.path.exists(dossierImages)
    if isExist == True:
        print("Le dossier images existe!")
        #RI : Alors enregistrer le fichier image dans le dossier images (voir si renommer fichier ?)
    else:
        print("pas de dossier Images")
        #RI : Créer le dossier images
        os.makedirs(dossierImages)
        print("Dossier images créé")
    
    #RI: Creation de mon Tableau Avec les données récupérées de la page produit:
    tableauProduit = [productPageUrl, prodType, upc, titre, prixSansTaxe, prixAvecTaxe, disponibilite, description, categorie, reviews, image]
    print(tableauProduit)

    #RI: Création fichier CSV (Fonctionne pas encore 31/03/2022)
    produit = pd.DataFrame({"tableauProduit" : tableauProduit})
    produit = produit.set_index("tableauProduit").T
    tableauProduit.to_csv("list_tableauProduit.csv", index=False)




recupPageProduit()