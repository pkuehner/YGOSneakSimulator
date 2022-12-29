from typing import List


def get_standard_card_ids() -> List[int]:
    with open("./assets/standard_cards") as file:
        return [int(line) for line in file.readlines()]