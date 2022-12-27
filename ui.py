from typing import List
import json
import random

packs = {}

from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()
root.title("Join")
root.configure(background="grey")

sets = [("RP01", 4), ("RP02", 4), ("LOB", 5), ("LON", 5), ("MRD", 5), ("MRL", 5), ("PSV", 5), ("LOD", 5)]


save_button = tk.Button(root, text="SAVE")
save_button.pack(side=tk.TOP)
num_card_label = tk.Label(root, text="Num Cards: ")
num_card_label.pack(side=tk.TOP)
card_effect_label = tk.Label(root, text="")
card_effect_label.pack(side=tk.TOP)

container = tk.Frame(root)
canvas = tk.Canvas(container)
canvas.config(width=1000, height=1000)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def button_click(card_id, photo):
    print(card_id)
    photo.convert("L")


def on_enter(card_id):
    card_effect_label.configure(text=cards_dict[str(card_id)]["desc"])


def on_leave(card_id):
    card_effect_label.configure(text="")


with open("card_info.json") as cards_file, open("pack_matching.json") as pack_file:
    packs_dict = json.load(pack_file)
    cards_dict = json.load(cards_file)
    cards = []
    random.seed(0)
    probability_map = {
        "C": 64,
        "R": 48,
        "SP": 32,
        "SSP": 16,
        "SR": 16,
        "UR": 8,
        "UtR": 8,
        "ScR": 8,
    }
    for set_id, num_packs in sets:
        card_ids = [card[0] for card in packs_dict[set_id]]
        for iteration in range(num_packs):
            weights = [probability_map[card[1]] for card in packs_dict[set_id]]
            cards.extend(
                random.choices([card[0] for card in packs_dict[set_id]], k=9, weights=weights)
            )

    cards = sorted(
        cards, key=lambda card_id: (cards_dict[str(card_id)]["type"], card_id)
    )

    images = ["pics/" + str(card_id) + ".jpg" for card_id in cards]

    selected = [False] * len(images)
    labels = [None] * len(images)
    photos = [None] * len(images)
    photos_2 = [None] * len(images)

    def save():
        print("Saving")
        file_contents = ""
        for index, val in enumerate(selected):
            if val:
                file_contents += str(cards[index]) + "\n"
        with open("deck.ydk", "w") as file:
            file.write(file_contents)

    save_button.bind("<Button-1>", lambda e: save())

    def create_label_for_photo(index):
        r, c = divmod(index, 5)
        image = Image.open(images[index])
        if selected[index]:
            image = image.convert("L")
        photos[index] = image
        photos_2[index] = ImageTk.PhotoImage(photos[index])
        if not labels[index]:
            labels[index] = tk.Label(
                scrollable_frame,
                image=photos_2[index],
            )
        else:
            labels[index].configure(image=photos_2[index])
        labels[index].photo = photos[index]
        labels[index].grid(row=r, column=c)
        labels[index].bind("<Button-1>", lambda e: button_click(index))
        labels[index].bind("<Enter>", lambda e: on_enter(cards[index]))
        labels[index].bind("<Leave>", lambda e: on_leave(cards[index]))

    def button_click(index):
        print(cards[index])
        selected[index] = not selected[index]
        num_card_label.configure(text="Num cards: " + str(selected.count(True)))
        create_label_for_photo(index)

    for i in range(len(images)):
        create_label_for_photo(i)

    root.mainloop()
