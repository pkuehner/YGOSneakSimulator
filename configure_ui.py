import time
from typing import List
import json
import random

from ui import run_ui

packs = {}

from PIL import Image, ImageTk
import tkinter as tk


set_codes = ["RP01", "RP02", "LOB", "MRD", "LON", "SDY", "SDJ", "SDP", "SDK"]

root = tk.Tk()
root.title("Configure")

set_entries = []
labelframe_packs = tk.LabelFrame(root, text="Packs")
iter = 0
frame = tk.Frame(labelframe_packs)
for set_code in set_codes:
    if iter == 10:
        frame.pack()
        frame = tk.Frame(labelframe_packs)
    iter+=1
    tk.Label(frame, text=set_code).pack(side=tk.LEFT)
    variable = tk.IntVar(labelframe_packs)
    variable.set(0) # default value
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
labelframe = tk.LabelFrame(root, text="Weights for Rarities")
labelframe.pack(fill="both", expand="yes")
for rarity, weight in rarities:
    frame = tk.Frame(labelframe)
    tk.Label(frame, text=rarity).pack()
    text = tk.StringVar(frame, weight)
    w = tk.Entry(frame, textvariable=text)
    w.pack()
    entries.append((text, rarity))
    frame.pack(side=tk.LEFT)


frame = tk.Frame(root)
frame.pack()
tk.Label(frame, text="Seed").pack()
seed_text = tk.StringVar(frame, random.randint(1, 100))
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
    run_ui(sets_and_nums, prob_weights, int(seed_text.get()))

save_button = tk.Button(root, text="GO")
save_button.pack(side=tk.BOTTOM)
save_button.bind("<Button-1>", lambda e: save())


root.mainloop()
