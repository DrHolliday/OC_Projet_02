from dataclasses import replace
import textwrap
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
import os

url = "http://books.toscrape.com/index.html"
reponse = requests.get(url)
soup = BeautifulSoup(reponse.content.decode("utf-8" , "ignore") , "html.parser")



# Récupération de toutes les url des catégories
def toutesLesCategories():
    if reponse.ok:
        # Je créé la var liens de type liste [] qui servira à récupérer les url plus tard
        tableauDeToutesLesCategories = []
        soup = BeautifulSoup(reponse.content.decode("utf-8" , "ignore") , "html.parser")
        #RI + 24/03/22: Je cible le div qui contient les catégories (plutôt que de cibler toute la page) 
        div = soup.find("div" , class_="side_categories").find("ul" , class_="nav nav-list").find("ul")
        #RI: Je boucle dans le div pour récupérer les liens des catégories:
        for categorie in div.findAll("a"):
            #RI: Teste si la balise a possède un attribut href et append dans ma liste "liens" si c'est le cas. et concatène le lien.
            tableauDeToutesLesCategories.append(categorie["href"].replace("catalogue" , "http://books.toscrape.com/catalogue"))

    print(tableauDeToutesLesCategories)
    return tableauDeToutesLesCategories

toutesLesCategories()
# Recup toute les categories de la page Home ça marche 01/05/2022 ! 