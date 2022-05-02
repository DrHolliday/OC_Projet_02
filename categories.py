import requests
from bs4 import BeautifulSoup
import urllib.parse

url = "http://books.toscrape.com/index.html"
reponse = requests.get(url)
soup = BeautifulSoup(reponse.content.decode("utf-8" , "ignore") , "html.parser")

#RI: Récupérer toutes les catégories de la page home (DEBUT !)

def toutesLesCategories(url):
    if reponse.ok:
        # Je créé la var liens de type liste [] qui servira à récupérer les url plus tard
        tableauDeToutesLesCategories = []
        soup = BeautifulSoup(reponse.content.decode("utf-8" , "ignore") , "html.parser")

        #RI + RICKEL ! BONNE METHODE ! 24/03/22: Je cible le div qui contient les catégories (plutôt que de cibler toute la page) 
        div = soup.find("div" , class_="side_categories").find("ul" , class_="nav nav-list").find("ul")

        #RI: Je boucle dans le div pour récupérer les liens des catégories:
        for categorie in div.findAll("a"):

            #RI: Teste si la balise a possède un attribut href et append dans ma liste "liens" si c'est le cas.
            tableauDeToutesLesCategories.append(categorie["href"])

    print(tableauDeToutesLesCategories)
    return tableauDeToutesLesCategories

toutesLesCategories(url)
# Recup toute les categories de la page Home ça marche 01/05/2022 ! 


def lesPagesDeLaCategorie(toutesLesCategories):
    #RI: Fonction de récupération de toutes les page d'une catégorie
    global soup

    lien = categorie["lien"]

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

# print(lesPagesDeLaCategorie(toutesLesCategories))