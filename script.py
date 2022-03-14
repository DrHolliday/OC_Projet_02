#RI: Importation des packages necessaire au projet: 

import requests
import beautifulsoup4
import pandas


#RI: On vérifie que le site cible réponds 
r = requests.get("http://books.toscrape.com/")
print(r.status_code)
