from pydantic import BaseModel
from typing import List, Dict
import json

class BrailleCharacter(BaseModel):
    corresponding_character: str
    punchHoleBitmap: List[List[bool]] 

    @classmethod
    def chars_as_dict(cls, chars: List["BrailleCharacter"]) -> Dict[str, List[List[bool]]]:
        return {
            char.corresponding_character: char.punchHoleBitmap
            for char in chars
        }

    def as_int_array(self) -> list[int]:
        array = []
        for row in self.punchHoleBitmap:
            array += [
                1 if row[1] else 0,
                1 if row[0] else 0
            ]
        return array

    def as_bits(self) -> str:
        s=""
        for c in self.as_int_array():
            s += str(c)
        return s

allCharacters = []
with open("BrailleCharacters.json") as fp:
    brailleCharacters = json.load(fp)
    allCharacters = [
        BrailleCharacter.model_validate(character)
        for character in brailleCharacters
    ]
    
def get_all_braille_characters():
    return allCharacters

