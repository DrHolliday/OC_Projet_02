#RI: Importation des packages necessaire au projet: 
from re import T
from textwrap import indent
from numpy import append
import requests
#BSA pour beautifullsoup et requete sur tag html etc.
from bs4 import BeautifulSoup
import pandas as pd
# os pour la creation de dossier ( images)
import os
import shutil

# ---- A FAIRE --------URL DYNAMIQUE pour pages             ---------------
# ---- A FAIRE FIN                    --------------------------------------

# url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
# reponse = requests.get(url)
# soup = BeautifulSoup(reponse.text, "html.parser")


#RI: Script qui vérifie chaque produits d'une catégorie et lance recupPageProduit a chaque produit trouvé dans la catégorie:
#RI:  http://books.toscrape.com/catalogue/category/books/mystery_3/index.html


#RI: Fonction qui vérifie si la catégorie contient plusieurs pages:
def pagesCategorie():

    tableauPages = [url,]
    #RI: Si ul class_"pager" existe alors enregistre les pages dans tableauPages sinon fait la page en cours
    pagerExists = soup.find("ul", class_="pager")
    if pagerExists:
        print("Il y a plusieurs pages pour cette catégorie")
        #RI: Trouver et enregistrer l'url des pages existantes dans un tableau
        liens = pagerExists.findAll("a", href=True)
        for a in liens:
            #RI: Concaténer l'url pour les pages en utilisant l'url de la page source et remplace index.html par nvlle pages existantes
            a = format(str( url.replace("index.html", "") + a["href"]) )
            tableauPages.append(a)
            return(tableauPages)
            
    else:
        print("Aucune autre page")

# pagesCategorie()


#RI: Fonction findUrl récupère l'url de toutes les pages produit d'une catégorie et les stock dans un tableau
def findUrl():

    tableauUrl = []

    for lis in soup.findAll("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        h3 = lis.find("h3")
        links = h3.findAll("a", href=True)
        for a in links:
            a = format(str(a["href"]).replace("../../../", "http://books.toscrape.com/catalogue/"))
            tableauUrl.append(a)

    print(tableauUrl)
    return(tableauUrl)
    
# findUrl()


# RI: Fonction pour récupérer infos d'une page produit et enregistrer dans une liste
def recupPageProduit():
    # url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
    # reponse = requests.get(url)
    # soup = BeautifulSoup(reponse.text, "html.parser")

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
    image = str(soup.find("div", class_="item active").find("img").get("src")).replace("../../" , "http://books.toscrape.com/")
    print(titre)
    #RI : Vérification dossier images (création si non existant) Sauvegarde de l illustration dans le dossier
    dossierImages = "images"
    isExist = os.path.exists(dossierImages)
    if isExist:
        print("Le dossier images existe!")
        #RI : Alors enregistrer le fichier image dans le dossier images (voir si renommer fichier ?)
        res = requests.get(image , stream=True)
        filename = os.path.join(dossierImages, "{0}.jpg" .format(str(titre).replace(":" , "-")) )
        print(filename)
        if not os.path.isfile(filename):
            with open(filename, "wb") as images:
                for content in res.iter_content(1024):
                    if not content:
                        break
                    images.write(content)
    else:
        print("pas de dossier Images")
        #RI : Créer le dossier images
        os.makedirs(dossierImages)
        print("Dossier images créé")
    
    #RI: Creation de mon Tableau Avec les données récupérées de la page produit:
    tableauProduit = [productPageUrl, prodType, upc, titre, prixSansTaxe, prixAvecTaxe, disponibilite, description, categorie, reviews, image]
    print(tableauProduit)

    #RI: Ecriture dans fichier CSV (livres.csv)
    produit = pd.DataFrame({"tableauProduit" : tableauProduit})
    produit = produit.set_index("tableauProduit").T
    #RI: Ecriture dans le fichier csv en mode "a" = (append, ajouter)
    produit.to_csv(r'livres.csv', mode = "a", index = False)

# recupPageProduit()


#RI: Créer un script qui utilise les 3 fonctions plus haut sur une url ! pour le faire réaliser l'opération
# pagesCategorie()
# findUrl()
# recupPageProduit()

def recupTouteLaCategorie():
    global url
    url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    global reponse
    reponse = requests.get(url)
    global soup
    soup = BeautifulSoup(reponse.text, "html.parser")
    
    pagesCategories = pagesCategorie()
    print(pagesCategories)
    print("ma page courante" ,url)

    #RI: Je récupère ma fonction de recherche d'url avant le changement de page et ensuite apres...
    tableauUrl = []

    for lis in soup.findAll("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        h3 = lis.find("h3")
        links = h3.findAll("a", href=True)
        for a in links:
            a = format(str(a["href"]).replace("../../../", "http://books.toscrape.com/catalogue/"))
            tableauUrl.append(a)

    #RI: Je charge la page numéro 2
    def changementUrl():
        global url
        url = pagesCategories[1]
        global reponse
        reponse = requests.get(url)
        print("ATTNTION CHANGEMENT URL", url)
        global soup
        soup = BeautifulSoup(reponse.text, "html.parser")

    changementUrl()

    #RI: Je relance la recherche dans la nouvelle page et j append a ma variable tableauUrl
    for lis in soup.findAll("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        h3 = lis.find("h3")
        links = h3.findAll("a", href=True)
        for a in links:
            a = format(str(a["href"]).replace("../../../", "http://books.toscrape.com/catalogue/"))
            tableauUrl.append(a)
    
    #RI: lancer la fonction en boucle de ficheproduit sur tous les liens du tableau...
    print(tableauUrl)

    for i in tableauUrl:
        url = i

        # print("Test",url)
        
        reponse = requests.get(url)
        soup = BeautifulSoup(reponse.text, "html.parser")

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
        image = str(soup.find("div", class_="item active").find("img").get("src")).replace("../../" , "http://books.toscrape.com/")
        print(titre)
        #RI : Vérification dossier images (création si non existant) Sauvegarde de l illustration dans le dossier
        dossierImages = "images"
        isExist = os.path.exists(dossierImages)
        if isExist:
            print("Le dossier images existe!")
            #RI : Alors enregistrer le fichier image dans le dossier images (voir si renommer fichier ?)
            res = requests.get(image , stream=True)
            filename = os.path.join(dossierImages, "{0}.jpg" .format(str(titre).replace(":" , "-")) )
            print(filename)
            if not os.path.isfile(filename):
                with open(filename, "wb") as images:
                    for content in res.iter_content(1024):
                        if not content:
                            break
                        images.write(content)
        else:
            print("pas de dossier Images")
            #RI : Créer le dossier images
            os.makedirs(dossierImages)
            print("Dossier images créé")
    
        #RI: Creation de mon Tableau Avec les données récupérées de la page produit:
        tableauProduit = [productPageUrl, prodType, upc, titre, prixSansTaxe, prixAvecTaxe, disponibilite, description, categorie, reviews, image]
        print(tableauProduit)

        #RI: Ecriture dans fichier CSV (livres.csv)
        produit = pd.DataFrame({"tableauProduit" : tableauProduit})
        produit = produit.set_index("tableauProduit").T
        #RI: Ecriture dans le fichier csv en mode "a" = (append, ajouter)
        produit.to_csv(r'livres.csv', mode = "a", index = False)

recupTouteLaCategorie()