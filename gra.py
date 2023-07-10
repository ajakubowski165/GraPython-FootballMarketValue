#__________BIBLIOTEKI

#requests i bs4 do web scrappingu
import requests
from bs4 import BeautifulSoup
#pandas do dataframe
import pandas as pd


#__________POBRANIE I OBROBKA DANYCH

#pokazujemy, ze dzialamy jako przegladarka
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


#tworzymy puste listy pilkarzy oraz ich wartosci
PlayersList = []
ValuesList = []


#wybieramy strone do analizy
for pagenum in range(1, 11):
    page = "https://www.transfermarkt.pl/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page=" + str(pagenum)
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    #wybieramy elementy na podstawie odpowiednich tagow html
    Players = pageSoup.find_all("td", {"class": "hauptlink"})
    Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})

    #dodajemy wartosci do list (w przypadku Players biore co drugi element, ponieważ find_all znalazło wszystkie classes zarówno hauptlink oraz rechts hauptlink)
    for i in range(0,50,2):
        PlayersList.append(Players[i].text)
    for i in range(0,25):
        ValuesList.append(Values[i].text)


#tworzymy ramke danych
df = pd.DataFrame({"Players":PlayersList,"Values":ValuesList})

#wyswietlamy dane
print(df.head(400))
