#___________________________________________________ Biblioteki
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

#___________________________________________________ Webscraping i obrobka danych

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

PlayersList = []
ValuesList = []
ImagesList = []

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


#___________________________________________________ Zmienne do obu trybow

excluded_values = []
i = 0
points = 0
rounds = 1

#___________________________________________________ Singleplayer

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

     # Ustaw rozmiar okna na 480x480
    root.geometry("600x320")

    # Display players and create buttons for user choice
    message = (
        "Round " + str(rounds) + "\n" +
        df['Players'][x] + " " + str(df['Values'][x]) + " mln €   vs.   " + df['Players'][y] + " ??? mln €\n" +
        "Kto jest drozszy? "
    )
    message_label.config(text=message)


    # Destroy previous buttons
    for button in root.winfo_children():
        if isinstance(button, tk.Button):
            button.destroy()

    button_font = ("Trebuchet MS", 12)
    button_bg_color = '#add8e6'

    # Create buttons for user choice
    play_round_button = tk.Button(root, text=df['Players'][y], command=lambda: evaluate_choice("yes"), font=button_font, bg=button_bg_color)
    play_round_button.pack(pady=10)

    play_round_button = tk.Button(root, text=df['Players'][x], command=lambda: evaluate_choice("no"), font=button_font, bg=button_bg_color)
    play_round_button.pack(pady=10)

    same_value_button = tk.Button(root, text="Same Value", command=lambda: evaluate_choice("same"), font=button_font, bg=button_bg_color)
    same_value_button.pack(pady=10)


    def evaluate_choice(choice):
        global rounds, points

        if (choice == "yes" and df["Values"][x] < df["Values"][y]) or \
           (choice == "no" and df["Values"][x] > df["Values"][y]) or \
           (choice == "same" and df["Values"][x] == df["Values"][y]):
            points += 1
            messagebox.showinfo("Correct", "Zdobywasz punkt! " + df['Players'][y] + " jest warty " + str(df['Values'][y]) + " mln €.\nTwoja liczba punktow: " + str(points))
        else:
            messagebox.showinfo("Game Over", "Koniec gry :( " + df['Players'][y] + " jest warty " + str(df['Values'][y]) + " mln €.\nZdobyles lacznie: " + str(points) + " punktow")
            root.quit()  # Terminate the Tkinter main loop

        rounds += 1
        sudden_death()  # Proceed to the next round


#___________________________________________________ Multiplayer
users_names = []

def start_multiplayer():
    global rounds, i, rounds_choice, num_players, points, users_names
    rounds_choice = simpledialog.askinteger("Input", 'Wpisz liczbe rund od 1 do 50: ', minvalue=1, maxvalue=50)
    num_players = simpledialog.askinteger("Input", 'Wpisz liczbe graczy od 2 do 10: ', minvalue=2, maxvalue=10)
    points = [0] * num_players
    rounds = 0

    # Utwórz listę z imionami graczy
    for player in range(1, num_players + 1):
        user_name = simpledialog.askstring("Input", f'Wpisz imię gracza {player}: ')
        users_names.append(user_name)

    multiplayer()


def multiplayer():
    global i, rounds, rounds_choice, num_players, points, users_names

    if rounds == rounds_choice:
        results = "\n".join([f"{users_names[player]}: {points[player]}" for player in range(num_players)])
        messagebox.showinfo("Game Over", "Koniec gry! Wyniki prezentują się następująco:\n" + results)
        root.quit()
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

    # Ustaw rozmiar okna na 600x320
    root.geometry("600x500")
    if(num_players > 7):
        root.geometry("600x700")
    

    round_counting = rounds + 1

    # Display players and create buttons for user choice
    message = (
        f"Runda {round_counting} | Kolej gracza {users_names[player - 1]}\n" +
        f"{df['Players'][x]} {df['Values'][x]} mln €   vs.   {df['Players'][y]} ??? mln €\n" +
        "Kto jest droższy? "
    )
    message_label.config(text=message)

    # Destroy previous buttons
    for button in root.winfo_children():
        if isinstance(button, tk.Button):
            button.destroy()

    button_font = ("Trebuchet MS", 12)
    button_bg_color = '#add8e6'

    # Create buttons for user choice
    play_round_button = tk.Button(root, text=df['Players'][y], command=lambda: evaluate_choice("yes"), font=button_font, bg=button_bg_color)
    play_round_button.pack(pady=10)

    play_round_button = tk.Button(root, text=df['Players'][x], command=lambda: evaluate_choice("no"), font=button_font, bg=button_bg_color)
    play_round_button.pack(pady=10)

    same_value_button = tk.Button(root, text="Same Value", command=lambda: evaluate_choice("same"), font=button_font, bg=button_bg_color)
    same_value_button.pack(pady=10)

    update_score_label()
    
    def evaluate_choice(choice):
        global rounds, points, i

        if (choice == "yes" and df["Values"][x] < df["Values"][y]) or \
           (choice == "no" and df["Values"][x] > df["Values"][y]) or \
           (choice == "same" and df["Values"][x] == df["Values"][y]):
            points[player - 1] += 1
            messagebox.showinfo("Correct", f"Zdobywasz punkt! {df['Players'][y]} jest wart {df['Values'][y]} mln €.\n{users_names[player - 1]}, twoja aktualna ilość punktów to: {points[player - 1]}")
        else:
            messagebox.showinfo("Incorrect", f"Zła odpowiedź! :( {df['Players'][y]} jest wart {df['Values'][y]} mln €.\n{users_names[player - 1]}, zdobyłeś łącznie dotychczas: {points[player - 1]} punktów")

        if player == num_players:
            rounds += 1

        i += 1
        multiplayer()  # Proceed to the next round
    
def update_score_label():
    global points, users_names
    scores = "\n".join([f"{users_names[player]}: {points[player]}" for player in range(num_players)])
    score_label.config(text=scores)


#___________________________________________________ Tworzenie okien dialogowych

root = tk.Tk()
root.title("Player Value Game")

# Ustaw rozmiar okna na 480x480
root.geometry("600x320")

main_text_font = ("Trebuchet MS", 14)
message_label = tk.Label(root, text="Witaj w grze!", font=main_text_font)
message_label.pack(pady=20)

button_font = ("Trebuchet MS", 12)
button_bg_color = '#add8e6'

score_label = tk.Label(root, text="", font=main_text_font)
score_label.pack(pady=10)

play_button = tk.Button(root, text="Singleplayer", command=sudden_death, font=button_font, bg=button_bg_color)
play_button.pack(pady=20)

play_multiplayer_button = tk.Button(root, text="Multiplayer", command=start_multiplayer, font=button_font, bg=button_bg_color)
play_multiplayer_button.pack(pady=20)

root.mainloop()

