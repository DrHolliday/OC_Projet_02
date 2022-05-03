#RI: Importation des packages necessaire au projet: 
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse

URL = "https://books.toscrape.com/"

def getCategorieLivres(categorie):
    lien = categorie["lien"]
    livresCategorie = []
    soup , livres = getLivresParPage(categorie["lien"] , categorie["nom"] )
    livresCategorie = livresCategorie + livres
    pageSuivante = soup.find("li" , {"class" : "next"})
    while pageSuivante:
        pageSuivanteHref = pageSuivante.find("a") ["href"]
        if pageSuivanteHref:
            pageSuivanteUrl = urllib.parse.urljoin(lien, pageSuivanteHref) 
            soup , livres = getLivresParPage(pageSuivanteUrl , categorie["nom"] )
            livresCategorie = livresCategorie + livres
            pageSuivante = soup.find("li" , {"class" : "next"})
        else:
            break
    return livresCategorie



def getLivresParPage(lienDeLaPage, nomDeCategorie):
    reponse = requests.get(lienDeLaPage)
    soup = BeautifulSoup(reponse.content.decode("utf-8" , "ignore") , "html.parser")
    articles = soup.findAll( "articles" , {"class" : "product_pod"} )
    livres = []
    for article in articles:
        temporaire = article.find("a")
        livreUrl = "{0}catalogue{1}".format (URL, str(temporaire["href"]).replace("../../..") , "" )
        livre = getInformationLivre(livreUrl, nomDeLaCategorie)
        if livre:
            livres.append(livre)
    return soup, livre

def getInformationLivre(urlLivre, nomDeLaCategorie):
    # avec Url livre, recup information que je met dans un objet {} et le retourne 
    # je dois recupoerer les infos de cette page : https://books.toscrape.com/catalogue/giant-days-vol-2-giant-days-5-8_895/index.html
    # retourner cet objet
    # appeler la fonction saveImageLivre

    pass

def saveImageLivre(nomDuFichier, urlDeLimage, nomDeCategorie):
    # je réutiliserai cette fonction dans la fonction du dessus: 
    pass

def fichierCsv(categorie, livres):
    # Juste envoyer panda dans livre
    # Créer un répertoir de catégorie pour les fichiers CSV en me servant du nom de la categorie que je recup
    pass

def getCategories(soup):
    categoriesTemp = soup.find("ul" , {"class" : "nav nav-list"}).ul.findAll("a") 
    categories = []
    for categorieTemp in categoriesTemp:
        #RI: Je récupère les noms de catégorie et les Urls dans un tableau categories
        categories.append({"nom" : str(categorieTemp.text).strip() , "lien" : urllib.parse.urljoin( URL , categorieTemp ["href"])})
    return categories

reponse = requests.get(URL)
soup = BeautifulSoup(reponse.text , "html.parser")

categories = getCategories(soup)

#RI: BOUCLE F I N A L E QUI APPELLE MES FONCTIONS UNE FOIS TOUT FAIT !
# for categorie in categories:
#     livres = getCategorieLivres(categorie)
#     fichierCsv(categorie, livres)


#TESTS : -----> 

print(categories)
