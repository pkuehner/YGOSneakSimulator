import json

packs = {}

with open("cards.json") as cards_file, open("card_info.json", "w") as card_info_file:
    cards_dict = json.load(cards_file)
    cards_new_dict = {}
    cards_list = cards_dict["data"]
    cnt = 0
    for card in cards_list:
        card_id: str = card["id"]
        cards_new_dict[card_id] = card
        
    json.dump(cards_new_dict, card_info_file)
