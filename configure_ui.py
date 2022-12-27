import time
from typing import List
import json
import random

packs = {}

from PIL import Image, ImageTk
import tkinter as tk


set_codes = ["RP01", "RP02", "LOB"]

root = tk.Tk()
root.title("Configure")

set_entries = []

for set_code in set_codes:
    tk.Label(root, text=set_code).pack()
    variable = tk.IntVar(root)
    variable.set(0) # default value
    set_entries.append((set_code, variable))
    w = tk.OptionMenu(root, variable, *list(range(100)))
    w.pack()

rarities = [
        ("C", "64"),
        ("R", "48"),
        ("SP", "48"),
        ("SSP", "32"),
        ("SR", "16"),
        ("UR", "8"),
        ("UtR", "8"),
        ("ScR", "8"),
]

entries = []
labelframe = tk.LabelFrame(root, text="Weights for Rarities")
labelframe.pack(fill="both", expand="yes")
for rarity, weight in rarities:
    frame = tk.Frame(labelframe)
    frame.pack()
    tk.Label(frame, text=rarity).pack()
    text = tk.StringVar(frame, weight)
    w = tk.Entry(frame, textvariable=text)
    w.pack(side=tk.BOTTOM)
    entries.append((text, rarity))

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


save_button = tk.Button(root, text="GO")
save_button.pack(side=tk.BOTTOM)
save_button.bind("<Button-1>", lambda e: save())

root.mainloop()
