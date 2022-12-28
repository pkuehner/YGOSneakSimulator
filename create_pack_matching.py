import json

packs = {}

with open("cards.json") as cards_file, open("pack_matching.json", "w") as pack_file:
    cards_dict = json.load(cards_file)
    cards_list = cards_dict["data"]
    cnt = 0
    for card in cards_list:
        card_id: str = card["id"]
        for set_dict in card.get("card_sets", []):
            print(cnt)
            cnt+=1
            set_code: str = "-".join(set_dict["set_code"].split("-")[:-1])
            if not set_code in packs:
                packs[set_code] = list()
            packs.get(set_code).append([card_id, set_dict["set_rarity_code"][1:-1]])
    print(len(packs))
    for pack_id, pack_set in packs.items():
        packs[pack_id] = list(pack_set)
    json.dump(packs, pack_file)
