'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import tkinter as tk
from tkinter import messagebox

# Web scraping and data processing

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

PlayersList = []
ValuesList = []

for pagenum in range(1, 11):
    page = "https://www.transfermarkt.pl/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page=" + str(pagenum)
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    Players = pageSoup.find_all("td", {"class": "hauptlink"})
    Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})

    for i in range(0, 50, 2):
        PlayersList.append(Players[i].text)
    for i in range(0, 25):
        ValuesList.append(Values[i].text)


df = pd.DataFrame({"Players": PlayersList, "Values": ValuesList})
df['Values'] = df['Values'].str.replace(' mln €', '').str.replace(',', '.').astype(float).astype(int)

# Game logic with Tkinter
def sudden_death():
    global rounds, points

    x = random.randint(0, len(df['Players']) - 1)
    while x in excluded_values:
        x = random.randint(0, len(df['Players']) - 1)
    excluded_values.append(x)

    y = random.randint(0, len(df['Players']) - 1)
    while y in excluded_values:
        y = random.randint(0, len(df['Players']) - 1)
    excluded_values.append(y)

    # Display players and create buttons for user choice
    message = (
        "Round " + str(rounds) + "\n" +
        df['Players'][x] + " " + str(df['Values'][x]) + " mln €   vs.   " + df['Players'][y] + " ??? mln €\n" +
        "Is " + df["Players"][y] + " more expensive (Yes)/ cheaper (No)/ has the same value (Same) as " + df["Players"][x]
    )
    message_label.config(text=message)


    # Destroy previous buttons
    for button in root.winfo_children():
        if isinstance(button, tk.Button):
            button.destroy()


    # Create buttons for user choice
    play_round_button = tk.Button(root, text=df['Players'][y], command=lambda: evaluate_choice("yes"))
    play_round_button.pack(pady=10)

    play_round_button = tk.Button(root, text=df['Players'][x], command=lambda: evaluate_choice("no"))
    play_round_button.pack(pady=10)

    same_value_button = tk.Button(root, text="Same Value", command=lambda: evaluate_choice("same"))
    same_value_button.pack(pady=10)


    def evaluate_choice(choice):
        global rounds, points

        if (choice == "yes" and df["Values"][x] < df["Values"][y]) or \
           (choice == "no" and df["Values"][x] > df["Values"][y]) or \
           (choice == "same" and df["Values"][x] == df["Values"][y]):
            points += 1
            messagebox.showinfo("Correct", "You earned a point! " + df['Players'][y] + " is worth " + str(df['Values'][y]) + " mln €.\nYour total points: " + str(points))
        else:
            messagebox.showinfo("Game Over", "Game over :( " + df['Players'][y] + " is worth " + str(df['Values'][y]) + " mln €.\nTotal points: " + str(points))
            root.quit()  # Terminate the Tkinter main loop

        rounds += 1
        sudden_death()  # Proceed to the next round


root = tk.Tk()
root.title("Player Value Game")

message_label = tk.Label(root, text="Witaj w grze!")
message_label.pack(pady=20)

play_button = tk.Button(root, text="Nagla smierc", command=sudden_death)
play_button.pack(pady=20)

rounds = 1
points = 0
excluded_values = []

root.mainloop()


"""

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

    if rounds == rounds_choice:
        print("Koniec gry! Wyniki prezentuja sie nastepujaco: ")
        print(points)
        break

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

    if player == num_players:
        rounds += 1

    print(points)

    i += 1



#26.07 - zawodnicy i ich wlasne punkty
#27.07 - tablica wyników i poprawić rundy, zeby nie konczyly sie na 1 zawodniku :)

#najlepszy wynik
#stop gry

"""
"""
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

# Web scraping and data processing

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

PlayersList = []
ValuesList = []

for pagenum in range(1, 11):
    page = "https://www.transfermarkt.pl/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page=" + str(pagenum)
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    Players = pageSoup.find_all("td", {"class": "hauptlink"})
    Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})

    for i in range(0, 50, 2):
        PlayersList.append(Players[i].text)
    for i in range(0, 25):
        ValuesList.append(Values[i].text)

df = pd.DataFrame({"Players": PlayersList, "Values": ValuesList})
df['Values'] = df['Values'].str.replace(' mln €', '').str.replace(',', '.').astype(float).astype(int)


excluded_values = []
rounds = 0
i = 0
points = 0

def start_multiplayer():
    global rounds, i, rounds_choice, num_players, points
    rounds_choice = simpledialog.askinteger("Input", 'Wpisz liczbe rund od 1 do 50: ', minvalue=1, maxvalue=50)
    num_players = simpledialog.askinteger("Input", 'Wpisz liczbe graczy od 2 do 10: ', minvalue=2, maxvalue=10)
    points = [0] * num_players
    multiplayer()


def multiplayer():
    global i, rounds, rounds_choice, num_players, points

    if rounds == rounds_choice:
        messagebox.showinfo("Game Over", "Koniec gry! Wyniki prezentuja sie nastepujaco:\n" + str(points))
        return

    player = (i % (num_players)) + 1

    x = random.randint(0, len(df['Players']) - 1)
    while x in excluded_values:
        x = random.randint(0, len(df['Players']) - 1)
    excluded_values.append(x)

    y = random.randint(0, len(df['Players']) - 1)
    while y in excluded_values:
        y = random.randint(0, len(df['Players']) - 1)
    excluded_values.append(y)

    choice = simpledialog.askstring("Input", "Czy " + df["Players"][y] + " jest drozszy (D)/ tanszy (T)/ ma taka sama wartosc (S) jak " + df["Players"][x])

    while choice not in ["S", "D", "T"]:
        choice = simpledialog.askstring("Input", "Wybierz S/D/T")

    if (choice == "D" and df["Values"][x] < df["Values"][y]) or (choice == "S" and (df["Values"][x] == df["Values"][y])) or (choice == "T" and df["Values"][x] > df["Values"][y]):
        points[player - 1] += 1
        messagebox.showinfo("Correct", "Zdobywasz punkt! " + df['Players'][y] + " jest warty " + str(
            df['Values'][y]) + " mln €. Twoja ilosc punktow to: " + str(points[player - 1]))
    else:
        messagebox.showinfo("Incorrect", "Zla odpowiedz! :( " + df['Players'][y] + " jest warty " + str(
            df['Values'][y]) + " mln €. Zdobyles lacznie: " + str(points[player - 1]) + " punktow")

    if player == num_players:
        rounds += 1

    i += 1
    multiplayer()



def sudden_death():
    global rounds, points

    x = random.randint(0, len(df['Players']) - 1)
    while x in excluded_values:
        x = random.randint(0, len(df['Players']) - 1)
    excluded_values.append(x)

    y = random.randint(0, len(df['Players']) - 1)
    while y in excluded_values:
        y = random.randint(0, len(df['Players']) - 1)
    excluded_values.append(y)

    # Display players and create buttons for user choice
    message = (
        "Round " + str(rounds) + "\n" +
        df['Players'][x] + " " + str(df['Values'][x]) + " mln €   vs.   " + df['Players'][y] + " ??? mln €\n" +
        "Is " + df["Players"][y] + " more expensive (Yes)/ cheaper (No)/ has the same value (Same) as " + df["Players"][x]
    )
    message_label.config(text=message)


    # Destroy previous buttons
    for button in root.winfo_children():
        if isinstance(button, tk.Button):
            button.destroy()


    # Create buttons for user choice
    play_round_button = tk.Button(root, text=df['Players'][y], command=lambda: evaluate_choice("yes"))
    play_round_button.pack(pady=10)

    play_round_button = tk.Button(root, text=df['Players'][x], command=lambda: evaluate_choice("no"))
    play_round_button.pack(pady=10)

    same_value_button = tk.Button(root, text="Same Value", command=lambda: evaluate_choice("same"))
    same_value_button.pack(pady=10)


    def evaluate_choice(choice):
        global rounds, points

        if (choice == "yes" and df["Values"][x] < df["Values"][y]) or \
           (choice == "no" and df["Values"][x] > df["Values"][y]) or \
           (choice == "same" and df["Values"][x] == df["Values"][y]):
            points += 1
            messagebox.showinfo("Correct", "You earned a point! " + df['Players'][y] + " is worth " + str(df['Values'][y]) + " mln €.\nYour total points: " + str(points))
        else:
            messagebox.showinfo("Game Over", "Game over :( " + df['Players'][y] + " is worth " + str(df['Values'][y]) + " mln €.\nTotal points: " + str(points))
            root.quit()  # Terminate the Tkinter main loop

        rounds += 1
        sudden_death()  # Proceed to the next round



root = tk.Tk()
root.title("Player Value Game")

message_label = tk.Label(root, text="Witaj w grze!")
message_label.pack(pady=20)

play_button = tk.Button(root, text="Nagla smierc", command=sudden_death)
play_button.pack(pady=20)

play_multiplayer_button = tk.Button(root, text="Nagla smierc", command=start_multiplayer)
play_multiplayer_button.pack(pady=20)

root.mainloop()