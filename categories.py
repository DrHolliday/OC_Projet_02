import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/index.html"
reponse = requests.get(url)

#RI: Récupérer toutes les catégories de la page home (DEBUT !)

if reponse.ok:
    # Je créé la var liens de type liste [] qui servira à récupérer les url plus tard
    liens = []
    soup = BeautifulSoup(reponse.text, "html.parser")

    #RI: Je cible le div qui contient les catégories (plutôt que de cibler toute la page)
    div = soup.find("div" , class_="side_categories")

    #RI: Je boucle dans le div pour récupérer les liens des catégories:
    for elem in div.findAll("li"):
            a = elem.find("a")
            try:
                if "href" in a.attrs:
                    url = a.get("href")
                    liens.append(url)
            except:
                pass
            for url in liens:
                print(url)

#RI: Récupérer toutes les catégories de la page home (FIN !)