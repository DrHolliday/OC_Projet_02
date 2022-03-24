import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/index.html"
reponse = requests.get(url)

#RI: Récupérer toutes les catégories de la page home (DEBUT !)

if reponse.ok:
    # Je créé la var liens de type liste [] qui servira à récupérer les url plus tard
    liens = []
    soup = BeautifulSoup(reponse.text, "html.parser")

    #RI + RICKEL ! BONNE METHODE ! 24/03/22: Je cible le div qui contient les catégories (plutôt que de cibler toute la page) 
    div = soup.find("div" , class_="side_categories").find("ul" , class_="nav nav-list").find("ul")

    #RI: Je boucle dans le div pour récupérer les liens des catégories:
    for elem in div.findAll("a"):

        #RI: Teste si la balise a possède un attribut href et append dans ma liste "liens" si c'est le cas.
        liens.append(elem["href"])

for url in liens:
    print(url)

#RI: Récupérer toutes les catégories de la page home (FIN !)