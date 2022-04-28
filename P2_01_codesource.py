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

url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"


    #RI: Je charge les autres pages de la catégorie si existantes
def changementUrl(pagesCategories):

    url = pagesCategories[1]
    reponse = requests.get(url)
    print("ATTNTION CHANGEMENT URL", url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    return url, soup
    #RI: Créer une boucle sur le nombre d'itération récupéré sur la liste nextpage si existante... a faire 28/04/2022

def pagesCategorie(soup):

    tableauPages = [url,]
    #RI: Si ul class_"pager" existe alors enregistre les pages dans tableauPages sinon fait la page en cours
    pagerExists = soup.find("ul", class_="pager").find("li", class_="next")
    if pagerExists:
        print("Il y a plusieurs pages pour cette catégorie")
        #RI: Trouver et enregistrer l'url des pages existantes dans un tableau
        liens = pagerExists.findAll("a", href=True)
        for a in liens:
            #RI: Concaténer l'url pour les pages en utilisant l'url de la page source et remplace index.html par nvlle pages existantes
            a = format(str( url.replace("index.html", "") + a["href"]) )
            tableauPages.append(a)
    return tableauPages
            

def recupTouteLaCategorie(url):

    reponse = requests.get(url)

    soup = BeautifulSoup(reponse.text, "html.parser")
    
    pagesCategories = pagesCategorie(soup)
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

    # Je charge la prochaine page de la catégorie:
    url, soup = changementUrl(pagesCategories)
   

    #RI: Je relance la recherche dans la nouvelle page et j append a ma variable tableauUrl
    for lis in soup.findAll("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        h3 = lis.find("h3")
        links = h3.findAll("a", href=True)
        for a in links:
            a = format(str(a["href"]).replace("../../../", "http://books.toscrape.com/catalogue/"))
            tableauUrl.append(a)
    
    #RI: lancer la fonction en boucle de recupPageProduit() sur tous les liens du tableau...
    print(tableauUrl)

    for i in tableauUrl:
        url = i
   
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
        dossierImages = "{0}{1}{2}".format("images", os.sep, categorie)
        isExist = os.path.exists(dossierImages)
        if not isExist:
            #RI: Création du dossier de la catégorie qui contiendra les images de cette catégorie !
            if not os.path.exists(dossierImages):
                print("OK Faut le créer ici")
                dossierCategorie = os.path.join(dossierImages, "{0}" .format(str(categorie).replace(":" , "-")) )
                os.makedirs(dossierCategorie)
            pass
        #RI : Alors enregistrer le fichier image dans le dossier images (voir si renommer fichier ?)
        res = requests.get(image , stream=True)
        filename = os.path.join(dossierImages, "{0}.jpg" .format(str(titre).replace(":" , "-",)) )
        print(filename)
        if not os.path.isfile(filename):
            with open(filename, "wb") as images:
                for content in res.iter_content(1024):
                    if not content:
                         break
                    images.write(content)
    
        #RI: Creation de mon Tableau Avec les données récupérées de la page produit:
        tableauProduit = [productPageUrl, prodType, upc, titre, prixSansTaxe, prixAvecTaxe, disponibilite, description, categorie, reviews, image]
        print(tableauProduit)

        #RI: Ecriture dans fichier CSV (livres.csv)
        produit = pd.DataFrame({"tableauProduit" : tableauProduit})
        produit = produit.set_index("tableauProduit").T
        #RI: Ecriture dans le fichier csv en mode "a" = (append, ajouter)
        nomDuFichier = "{0}.csv".format(categorie)
        produit.to_csv(nomDuFichier, mode = "a", index = False)

recupTouteLaCategorie(url)


#RI: OK: Voir Ligne 97 -- Chercher la fonction os."quelquechose" pour créer dossier récursivement des catégories (Stackoverflow)  !! A faire 14/04/2022
#RI: Voir Ligne 23 -- Créer une boucle sur le nombre d'itération récupéré sur la liste nextpage si existante... a faire 28/04/2022