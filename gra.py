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

# Usunięcie zbędnych znaków i konwersja na typ int
df['Values'] = df['Values'].str.replace(' mln €', '').str.replace(',', '.').astype(float).astype(int)



#algorytm gry - nagła śmierć
#pusta lista wykluczonych wartosci
excluded_values = []
points = 0
rounds = 1
i=1

while len(excluded_values) < len(df['Players']): #dopóki nie wyczerpie sie liczba wykorzystanych zawodników

    x = random.randint(0, len(df['Players']) - 1) #losujemy liczbe
    while x in excluded_values: #jesli x znajduje sie w wykluczonych liczbach
        x = random.randint(0, len(df['Players']) - 1) #losujemy ponownie
    excluded_values.append(x) #dopisujemy wylosowaną liczbe do liczb wykluczonych
    
    y = random.randint(0, len(df['Players']) - 1) #losujemy drugą liczbe
    while y in excluded_values: #jesli y znajduje sie w wykluczonych liczbach
        y = random.randint(0, len(df['Players']) - 1) #losujemy ponownie
    excluded_values.append(y) #dopisujemy do wykluczonych
    

    #numer rundy oraz instrukcja wyboru
    print("--------- RUNDA " + str(rounds))
    print(df['Players'][x] + " " + str(df['Values'][x]) + " mln €   vs.   " + df['Players'][y] + " ??? mln € ")
    print("Czy " + df["Players"][y] + " jest drozszy (D)/ tanszy (T)/ ma taka sama wartosc (S) jak " + df["Players"][x])


    #obsluga bledu wyboru
    choice = input() 
    while choice not in ["S","D","T"]:
        print("Wybierz S/D/T")
        choice = input()


    #sprawdzenie wyboru
    if (choice == "D" and df["Values"][x] < df["Values"][y]) or (choice == "S" and (df["Values"][x] == df["Values"][y])) or (choice == "T" and df["Values"][x] > df["Values"][y]): #jesli dobry wybor
        points += 1
        print("Zdobywasz punkt! " + df['Players'][y] + " jest warty " + str(df['Values'][y]) + " mln €. Twoja ilosc punktow to: " + str(points) + "\n")
    else: #jesli zly wybor
        print("Koniec gry :( " + df['Players'][y] + " jest warty " + str(df['Values'][y]) + " mln €. Zdobyles lacznie: " + str(points) + " punktow\n")
        break
    
    rounds += 1
    i += 1



#algorytm gry - rundy i gracze
excluded_values = []
rounds = 1
i = 0


rounds_choice = int(input('Wpisz liczbe rund od 1 do 50: '))

while rounds_choice not in range(1, 51):
    print("Liczba nie należy do przedziału 1-50")
    rounds_choice = int(input("Podaj inną liczbę: "))


num_players = int(input('Wpisz liczbe graczy od 2 do 10: '))

while num_players not in range(2, 11):
    print("Liczba nie należy do przedziału 2-10")
    num_players = int(input("Podaj inną liczbę: "))


points = [0] * num_players


while len(excluded_values) < len(df['Players']): #dopóki nie wyczerpie sie liczba wykorzystanych zawodników

    player = (i % (num_players)) + 1

    x = random.randint(0, len(df['Players']) - 1) #losujemy liczbe
    while x in excluded_values: #jesli x znajduje sie w wykluczonych liczbach
        x = random.randint(0, len(df['Players']) - 1) #losujemy ponownie
    excluded_values.append(x) #dopisujemy wylosowaną liczbe do liczb wykluczonych
    
    y = random.randint(0, len(df['Players']) - 1) #losujemy drugą liczbe
    while y in excluded_values: #jesli y znajduje sie w wykluczonych liczbach
        y = random.randint(0, len(df['Players']) - 1) #losujemy ponownie
    excluded_values.append(y) #dopisujemy do wykluczonych
    
    #numer rundy, zawodnicy w niej wystepujacy oraz instrukcja wyboru
    print("--------- RUNDA " + str(rounds) + " --------- Kolej gracza: " + str(player))
    print(df['Players'][x] + " " + str(df['Values'][x]) + " mln €   vs.   " + df['Players'][y] + " ??? mln € ")
    print("Czy " + df["Players"][y] + " jest drozszy (D)/ tanszy (T)/ ma taka sama wartosc (S) jak " + df["Players"][x])

    #obsluga bledu wyboru
    choice = input() 
    while choice not in ["S","D","T"]:
        print("Wybierz S/D/T")
        choice = input()

    #sprawdzenie wyboru
    if (choice == "D" and df["Values"][x] < df["Values"][y]) or (choice == "S" and (df["Values"][x] == df["Values"][y])) or (choice == "T" and df["Values"][x] > df["Values"][y]): #jesli dobry wybor
        points[player-1] += 1
        print("Zdobywasz punkt! " + df['Players'][y] + " jest warty " + str(df['Values'][y]) + " mln €. Twoja ilosc punktow to: " + str(points[player-1]) + "\n")
    else: #jesli zly wybor
        print("Zla odpowiedz! :( " + df['Players'][y] + " jest warty " + str(df['Values'][y]) + " mln €. Zdobyles lacznie: " + str(points[player-1]) + " punktow\n")

    if rounds == rounds_choice:
        break

    if player == num_players:
        rounds += 1

    print(points)

    i += 1



#26.07 - zawodnicy i ich wlasne punkty
#27.07 - tablica wyników i poprawić rundy, zeby nie konczyly sie na 1 zawodniku :)

#najlepszy wynik
#stop gry

