from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}


# ---------------------------- CREATE NEW FLASHCARDS ----------------------------------------------- #
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')


def next_cards():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=f"{current_card['French']}", fill="black")
    canvas.itemconfig(card_background, image=french_img)
    flip_timer = window.after(3000, func=flip_cards)


def flip_cards():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=f"{current_card['English']}", fill="white")
    canvas.itemconfig(card_background, image=english_img)


def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    print(len(data))
    data.to_csv("data/words_to_learn.csv", index=False)
    next_cards()


# ---------------------------- UI SETUP ------------------------------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_cards)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
english_img = PhotoImage(file="images/card_back.png")
french_img = PhotoImage(file="images/card_front.png")
card_background = canvas.create_image(400, 263, image=french_img)
canvas.grid(row=0, column=0, columnspan=2)

title = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 30, "italic"))

word = canvas.create_text(400, 263, text=f"", fill="black",
                          font=("Ariel", 45, "bold"))

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_cards)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

next_cards()

window.mainloop()
