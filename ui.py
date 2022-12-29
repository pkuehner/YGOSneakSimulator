from tkinter import filedialog
from typing import List
import json
import random

from PIL import Image, ImageTk
import tkinter as tk

from forbidden_cards_parser import FORBIDDEN_STATES, ForbiddenCardsParser

def run_ui(sets, probability_map, seed):
    root = tk.Tk()
    root.title("Join")
    root.configure(background="grey")
    save_button = tk.Button(root, text="SAVE")
    save_button.pack(side=tk.TOP)
    num_card_label = tk.Label(root, text="Num Cards: ")
    num_card_label.pack(side=tk.TOP)
    card_effect_label = tk.Label(root, text="")
    card_effect_label.pack(side=tk.TOP)
    
    forbidden_cards_parser = ForbiddenCardsParser()
    forbidden_cards_list_name = "TCG 01.12.2022"

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
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    root.bind_all("<MouseWheel>", _on_mousewheel)

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

    packs_dict = {}
    cards_dict = {}
    with open("card_info.json") as cards_file, open("pack_matching.json") as pack_file:
        packs_dict = json.load(pack_file)
        cards_dict = json.load(cards_file)
    cards = []
    random.seed(seed)


    for set_id, num_packs in sets:
        if num_packs > 0:
            card_ids = [card[0] for card in packs_dict[set_id]]
            for iteration in range(num_packs):
                weights = []
                for card in packs_dict[set_id]:
                    if card[1] in probability_map:
                        weights.append(probability_map[card[1]])
                    else:
                        weights.append(probability_map["UR"])
                cards.extend(
                    random.choices([card[0] for card in packs_dict[set_id]], k=9, weights=weights)
                )

    cards = sorted(
        cards, key=lambda card_id: (cards_dict[str(card_id)]["type"], card_id)
    )

    images = ["pics/" + str(card_id) + ".jpg" for card_id in cards]

    forbidden_img = Image.open("assets/forbidden.jpg")
    limited_img = Image.open("assets/limited.jpg")
    semi_limited_img = Image.open("assets/semi-limited.jpg")


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

        f = filedialog.asksaveasfile(mode='w')
        if f is None:
            return
        f.write(file_contents)
        f.close()

    save_button.bind("<Button-1>", lambda e: save())

    def create_label_for_photo(index):
        r, c = divmod(index, 5)
        image = Image.open(images[index])

        forbidden_cards_status: FORBIDDEN_STATES = forbidden_cards_parser.get_card_forbidden_status(forbidden_cards_list_name, str(cards[index]))
        if forbidden_cards_status == FORBIDDEN_STATES.FORBIDDEN:
            image = Image.blend(image, forbidden_img, alpha=0.75)
        elif forbidden_cards_status == FORBIDDEN_STATES.LIMITED:
            image = Image.blend(image, limited_img, alpha=0.75)
        if forbidden_cards_status == FORBIDDEN_STATES.SEMI_LIMITED:
            image = Image.blend(image, semi_limited_img, alpha=0.75)

        print(cards[index])

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
