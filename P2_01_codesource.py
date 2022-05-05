from dataclasses import replace
import textwrap
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
import os

#RI: ATTENTION ! Les vérifications de toutes les fonctions nécesscitent l'url de categorie qui contient le plus grand nombre de pages produits "https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html")
url = "https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html"
reponse = requests.get(url)
soup = BeautifulSoup(reponse.content.decode("utf-8" , "ignore") , "html.parser")


def toutesLesCategories():
    #RI: Je récupère l'url de toutes les catégories du site dans un tableau
    url = "https://books.toscrape.com/"
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.content.decode("utf-8" , "ignore") , "html.parser")
    if reponse.ok:
        # Je créé la var liens de type liste [] qui servira à récupérer les url plus tard
        tableauDeToutesLesCategories = []
        soup = BeautifulSoup(reponse.content.decode("utf-8" , "ignore") , "html.parser")

        #RI: Je cible le div qui contient les catégories 
        div = soup.find("div" , class_="side_categories").find("ul" , class_="nav nav-list").find("ul")
        #RI: Je boucle dans le div pour récupérer les liens des catégories:
        for categorie in div.findAll("a"):
            #RI: Teste si la balise "a" possède un attribut "href" et append dans ma liste "liens" et concatène url Exploitable.
            tableauDeToutesLesCategories.append(categorie["href"] .replace("catalogue" , "http://books.toscrape.com/catalogue"))

    return tableauDeToutesLesCategories

# toutesLesCategories()


def pagesCategorie():
    #Ri: Vérifier si plus de 20 produits existent sur la page (afin de savoir si plusieurs page à generer)
    testSurNombreElements = soup.find("form" , {"class" : "form-horizontal"}).find("strong").text.strip()
    if int(testSurNombreElements) > 20:
        print("il y a plus de 20 produits, donc génération de pages supplémentaires")
        pageSuivante = soup.find("li" , {"class" : "current"}).text.strip()
        #RI: Récupération du nombre de pages basé sur le dernier caractere du text dans le code HTML
        nombreDePages = int(pageSuivante[-1])
        if nombreDePages > 1:
            tableauPagesDeLaCategorie = [url,]
            #RI: Calculer le nombre de pages a générer en soustraiant la page index:
            nombreDePages = nombreDePages - 1
            #RI: Pour chaque page a générer, boucler et ajouter la page générée au tableau après la valeur par défaut en incrémentant le numéro de la page
            for i in range(nombreDePages):
                #Ri: remplacer index.html par "page-" i+2 ".html"
                tableauPagesDeLaCategorie.append(url.replace("index.html" , "page-" + str(i+2) + ".html" ))
            return tableauPagesDeLaCategorie
    else:
        print("il y a moins de 20 produits " )
        tableauPagesDeLaCategorie = [url,]
        return tableauPagesDeLaCategorie

# print(pagesCategorie())


def tableauProduitsCategorie():
    #RI: génération d'un tableau de liens de page produit par pages de la catégorie
    tableauUrl = []
    for i in pagesCategorie():
        url = i
        reponse = requests.get(url)
        soup = BeautifulSoup(reponse.content.decode("utf-8" , "ignore") , "html.parser")
        for lis in soup.findAll("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
            h3 = lis.find("h3")
            links = h3.findAll("a", href=True)
            for a in links:
                a = format(str(a["href"]).replace("../../../", "http://books.toscrape.com/catalogue/"))
                tableauUrl.append(a)
    return tableauUrl

# print(tableauProduitsCategorie())


def pageProduitParCategorie():
    for i in tableauProduitsCategorie():
        url = i
        reponse = requests.get(url)
        soup = BeautifulSoup(reponse.content.decode("utf-8" , "ignore") , "html.parser")
        #RI: Je teste mon url pour détecter les pages Index des pages produits, si la catégorie apparait je passe a l'url suivante
        if "/category/" in url:
            print("Pas la bonne page")
        else:
            print("ok, execute le code")
            productPageUrl = url
            prodType = soup.find("th", text="Product Type").find_next_sibling("td").text.strip()
            upc = soup.find("th", text="UPC").find_next_sibling("td").text.strip()
            titre = soup.find("h1").text.strip()
            prixSansTaxe = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").text.strip()
            prixAvecTaxe = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").text.strip()
            disponibilite = soup.find("th", text="Availability").find_next_sibling("td").text.strip()
            #Ri: Test sur le tag P de description, si pas existant remplir par du texte (quelques cas de figure détectés en test)
            try:
                description = soup.find("div", id="product_description").find_next_sibling("p").text.strip() 
            except:
                description = ("Pas de description pour ce produit")
                pass 
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
                    dossierCategorie = os.path.join(dossierImages, "{0}" .format(str(categorie).replace(":" , "-")))
                    os.makedirs(dossierCategorie)
                pass
            #RI : Alors enregistrer le fichier image dans le dossier images (voir si renommer fichier ?)
            res = requests.get(image , stream=True)
            #RI: Gérer le rewrite des symboles qui posent problème dans le nom de fichier.jpg généré (", ', :,) etc.
            filename = os.path.join(dossierImages, "{0}.jpg" .format(str(titre).replace(":" , "-",).replace("/" , "-",).replace("'" , "",).replace('"' , "",).replace('*' , " ",).replace('?' , " ",)))
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

            #RI : Vérification dossier CSV (création si non existant) Sauvegarde du fichier csv dans le dossier csv
            dossierCsv = "{0}".format("csv")
            csvIsExist = os.path.exists(dossierCsv)
            if not csvIsExist:
                nomDuFichier = os.path.join(dossierCsv, "{0}.csv".format(categorie))
                os.makedirs(dossierCsv)
            #RI: Ecriture dans fichier CSV (livres.csv)
            produit = pd.DataFrame({"tableauProduit" : tableauProduit})
            produit = produit.set_index("tableauProduit").T
            #RI: Ecriture dans le fichier csv en mode "a" = (append, ajouter)
            nomDuFichier = os.path.join(dossierCsv, "{0}.csv".format(categorie))
            produit.to_csv(nomDuFichier, mode = "a", index = False)


# pageProduitParCategorie()


#RI: SCRIPT FINAL POUR LANCER LE SCRAPPING SUR TOUT LE SITE:
for i in toutesLesCategories():
    url = i
    pageProduitParCategorie()