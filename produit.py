#RI: Importation des packages necessaire au projet: 
import requests
#BSA pour beautifullsoup et requete sur tag html etc.
from bs4 import BeautifulSoup
import pandas
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


# RI: Fonction pour récupérer infos d'une page produit

def recupPageProduit():
    url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")

    #RI: Récupération des parties qui m'intéressent et l'afficher/stocker:
    productPageUrl = url
    print("Url de la page: ",productPageUrl)
    prodType = soup.find("th", text="Product Type").find_next_sibling("td")
    print("Product Type:", prodType.text)
    upc = soup.find("th", text="UPC").find_next_sibling("td")
    print("UPC: " , upc.text)
    titre = soup.find("h1")
    print("Titre: " + titre.text)
    prixSansTaxe = soup.find("th", text="Price (excl. tax)").find_next_sibling("td")
    print("Prix (sans taxe): " , prixSansTaxe.text)
    prixAvecTaxe = soup.find("th", text="Price (excl. tax)").find_next_sibling("td")
    print("Prix (avec taxe): " , prixAvecTaxe.text)
    disponibilite = soup.find("th", text="Availability").find_next_sibling("td")
    print("Disponibilité: " , disponibilite.text)
    description = soup.find("div", id="product_description").find_next_sibling("p")
    print("Description du produit : " , description.text)
    categorie = soup.find("ul", class_="breadcrumb").findChildren()[4].find("a").text.strip()
    print("Catégorie: " , categorie)
    reviews = soup.find("th", text="Number of reviews").find_next_sibling("td")
    print("Number of reviews: " , reviews.text)
    image = soup.find("div", class_="item active").find("img").get("src")
    print("Image url: " , image)

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


recupPageProduit()