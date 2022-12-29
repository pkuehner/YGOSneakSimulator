import time
from typing import List
import json
import random
from forbidden_cards_parser import ForbiddenCardsParser
from load_sets import get_all_sets
from PIL import Image, ImageTk
import tkinter as tk
from ui import run_ui
from logging import Logger

logger = Logger(__name__)


configuration = {}
try:
    with open("configuration.json") as configuration_file:
        configuration = json.load(configuration_file)
except:
    logger.warning("No configuration file found, going for defaults")
packs = {}


set_codes = get_all_sets()

root = tk.Tk()
root.title("Configure")

save_button = tk.Button(root, text="GO")
save_button.pack(side=tk.RIGHT)
save_button.bind("<Button-1>", lambda e: save())

forbidden_cards_parser = ForbiddenCardsParser()
ban_list_var = tk.StringVar(root)
ban_list_var.set(configuration.get("banlist", "No Banlist"))# default value
ban_list_option_menu = tk.OptionMenu(root, ban_list_var, *forbidden_cards_parser.get_forbidden_list_names())
ban_list_option_menu.pack(side=tk.RIGHT)

#Scrolling
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
### Scrollbar End

set_entries = []
labelframe_packs = tk.LabelFrame(scrollable_frame, text="Packs")
iter = 0
frame = tk.Frame(labelframe_packs)
for set_code in set_codes:
    if iter%10 == 0:
        frame.pack()
        frame = tk.Frame(labelframe_packs)
    iter+=1
    tk.Label(frame, text=set_code).pack(side=tk.LEFT)
    variable = tk.IntVar(labelframe_packs)
    variable.set(configuration.get("packs", {}).get(set_code, 0)) # default value
    set_entries.append((set_code, variable))
    w = tk.OptionMenu(frame, variable, *list(range(100)))
    w.pack(side=tk.LEFT)
frame.pack()
labelframe_packs.pack(fill="both", expand="yes")

rarities = [
        ("C", "2"),
        ("R", "1"),
        ("SP", "1"),
        ("SSP", "1"),
        ("SR", "1"),
        ("UR", "1"),
        ("UtR", "1"),
        ("ScR", "1"),
]

entries = []
labelframe = tk.LabelFrame(scrollable_frame, text="Weights for Rarities")
labelframe.pack(fill="both", expand="yes")
for rarity, weight in rarities:
    frame = tk.Frame(labelframe)
    tk.Label(frame, text=rarity).pack()
    text = tk.StringVar(frame, weight)
    w = tk.Entry(frame, textvariable=text)
    w.pack()
    entries.append((text, rarity))
    frame.pack(side=tk.LEFT)


frame = tk.Frame(scrollable_frame)
frame.pack()
tk.Label(frame, text="Seed").pack()
seed_text = tk.StringVar(frame, configuration.get("seed", random.randint(1, 100)))
seed_entry = tk.Entry(frame, textvariable=seed_text)
seed_entry.pack(side=tk.RIGHT)


def save():
    prob_weights = {}
    for var, rarity in entries:
        prob_weights[rarity] = int(var.get())
    print(prob_weights)

    sets_and_nums = []
    for set_code, var in set_entries:
        sets_and_nums.append((set_code, var.get()))

    print(sets_and_nums)
    root.destroy()
    run_ui(sets_and_nums, prob_weights, int(seed_text.get()), ban_list_var.get())


root.mainloop()
