from enum import Enum
from typing import List

class FORBIDDEN_STATES(Enum):
    FORBIDDEN = 0
    LIMITED = 1
    SEMI_LIMITED = 2
    UNLIMITED = 3
                         

class ForbiddenCardsList:
    def __init__(self, name:str):
        self.name = name
        self.forbidden_states = {}    

    def add_card(self, card_id: str, forbidden_state: FORBIDDEN_STATES):
        self.forbidden_states[card_id] = forbidden_state
    
    def get_card_status(self, card_id: str) -> FORBIDDEN_STATES:
        return self.forbidden_states.get(card_id, FORBIDDEN_STATES.UNLIMITED)

DEFAULT_FP = "./forbidden_cards_lists/lflist.conf"

class ForbiddenCardsParser:
    def __init__(self, file_path:str = None):
        if not file_path:
            file_path = DEFAULT_FP
        
        self.file_path = file_path
        self.forbidden_lists = {}

        self.load_contents_from_file()

    def load_contents_from_file(self):
        with open(self.file_path) as file:
            current_list: ForbiddenCardsList = None
            for line in file.readlines():
                if "#" in line:
                    continue

                if "!" in line:
                    line = line.strip()[1:]
                    self.forbidden_lists[line] = ForbiddenCardsList(line)
                    current_list = self.forbidden_lists[line]
                    continue
                
                line = line.strip()
                line_parts = line.split()
                if len(line_parts) != 2:
                    continue

                current_list.add_card(line_parts[0], FORBIDDEN_STATES(int(line_parts[1])))
    
    def get_forbidden_list_names(self) -> List[str]:
        return self.forbidden_lists.keys()

    def get_card_forbidden_status(self, list_name:str, card_id:str) -> FORBIDDEN_STATES:
        return self.forbidden_lists[list_name].get_card_status(card_id)


print(ForbiddenCardsParser().get_forbidden_list_names())
print(ForbiddenCardsParser().get_card_forbidden_status("TCG 01.12.2022", "2295440"))