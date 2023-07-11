#__________BIBLIOTEKI

#requests i bs4 do web scrappingu
import requests
from bs4 import BeautifulSoup
import pandas as pd #do dataframe
import random #do losowania



#__________POBRANIE I OBROBKA DANYCH

#pokazujemy, ze dzialamy jako przegladarka
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


#tworzymy puste listy pilkarzy oraz ich wartosci
PlayersList = []
ValuesList = []
NationalitiesList = []


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

#wyswietlamy dane dla sprawdzenia
print(df)

#pusta lista wykluczonych wartosci
excluded_values = []
points = 0
rounds = 1

#algorytm gry
while len(excluded_values) < len(df['Players']): #dopóki nie wyczerpie sie liczba wykorzystanych zawodników
    
    x = random.randint(0, len(df['Players']) - 1) #losujemy liczbe
    excluded_values.append(x) #dopisujemy wylosowaną liczbe do liczb wykluczonych
    
    y = random.randint(0, len(df['Players']) - 1) #losujemy drugą liczbe
    excluded_values.append(y) #dopisujemy do wykluczonych
    
    print("--------- RUNDA " + str(rounds) + " ---------")
    print(df['Players'][x] + " " + df['Values'][x] + "   vs.   " + df['Players'][y] + " ??? mln € ")
    print("Czy " + df["Players"][y] + " jest drozszy (D)/ tanszy (T)/ ma taka sama wartosc (S) jak " + df["Players"][x])

    choice = input() 
    while choice not in ["S","D","T"]:
        print("Wybierz S/D/T")
        choice = input()

    if (choice == "D" and df["Values"][x] > df["Values"][y]) or (choice == "S" and df["Values"][x] == df["Values"][y]) or (choice == "T" and df["Values"][x] < df["Values"][y]): #jesli dobry wybor
        points += 1
        print("Zdobywasz punkt! " + df['Players'][y] + " jest warty " + df['Values'][x] + " Twoja ilosc punktow to: " + str(points) + "\n")
    else: #jesli zly wybor
        print("Nie zdobywasz punktu. " + df['Players'][y] + " jest warty " + df['Values'][x] + " Twoja ilość punktów to: " + str(points) + "\n")
    
    rounds += 1

