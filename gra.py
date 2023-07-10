#__________BIBLIOTEKI

#requests i bs4 do web scrappingu
import requests
from bs4 import BeautifulSoup
#pandas do dataframe
import pandas as pd


#__________WYBRANIE STRONY

#pokazujemy, ze dzialamy jako przegladarka
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

#wybieramy strone do analizy
page = "https://www.transfermarkt.pl/spieler-statistik/wertvollstespieler/marktwertetop"
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')



#_________WYBIERANIE I OBRÓBKA ELEMENTÓW

#wybieramy elementy na podstawie odpowiednich tagow html
Players = pageSoup.find_all("td", {"class": "hauptlink"})
Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})

#tworzymy puste listy
PlayersList = []
ValuesList = []


#dodajemy odpowiednie elementy (w przypadku Players biore co drugi element, ponieważ find_all znalazło wszystkie classes zarówno hauptlink oraz rechts hauptlink)
for i in range(0,50,2):
    PlayersList.append(Players[i].text)

for i in range(0,25):
    ValuesList.append(Values[i].text)


#tworzymy ramke danych
df = pd.DataFrame({"Players":PlayersList,"Values":ValuesList})

print(df.head(15))