
from random import shuffle
from typing import Sequence
from datetime import datetime

class Word:
    def __init__(self, id: int, word: str, definition: str, type: str, created_at: datetime=None):
        self.id = id
        self.word = word
        self.definition = definition
        self.type = type
        self.created_at = created_at

        
class Dictionary:
    def __init__(self, collection: Sequence[Word]):
        self.collection = collection
        self.len_collection = len(self.collection)
        self.types = ['', 'Phrase', 'Verb', 'Noun', 'Irregular Verb', 'Regular verb', 'Adjective']

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self) -> Word:
        if self._index >= self.len_collection:
            self._index = 0
            shuffle(self.collection)
        word: Word = self.collection[self._index]
        self._index += 1
        return word


if __name__ == '__main__':
    from database import Database
    db = Database()
    dic  = Dictionary(db.get_all_words())
    step = 0
    dic_itr = dic.__iter__()
    for _ in range(10):
        word, info = next(dic_itr)
        print(word)
        print(info)