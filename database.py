import sqlite3
import datetime
from dictionary import Word
from typing import Sequence

'''
- CURRENT_TIMESTAMP
    is a sqlite built-in function that is invoked when no values is passed.
- self.db_file = ':memory:'
    creates temporary database in RAM.
- with self.connection
    works as a context manager in Python to open, commit, and rollback an sql statement.
- sqlite3.register
    register the function to apply before inserting or extracting an instance from table. 
- CREATED_AT TIMESTAMP DEFAULT (DATE ('now'))
    we can use any keyword in place of 'TIMESTAMP' as long as we define its conversion and register it. 
- DATE ('now')
    create datatime object of format: yyyy-mm-dd
'''

def adapt_datetime(dt: datetime):
    return dt.date().isoformat()

def convert_datetime(s):
    return datetime.datetime.fromisoformat(s.decode())

sqlite3.register_adapter(datetime.datetime, adapt_datetime) # python -> sqlite3
sqlite3.register_converter("TIMESTAMP", convert_datetime) # sqlite3 -> python


class Database(object):

    def __init__(self):
        self.db_file = 'sqldb.py'
        self.table_name = 'DICTIONARY'
        self.connection = sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()
        if not self.table_exists:
            self.create_table()

    def create_table(self):
        with self.connection:
            self.cursor.execute("""
                                CREATE TABLE DICTIONARY (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                WORD TEXT,
                                DEFINITION TEXT,
                                TYPE TEXT,
                                CREATED_AT TIMESTAMP DEFAULT (DATE ('now'))
                            )""")

    def drop_table(self):
        with self.connection:
            self.cursor.execute(" DROP TABLE IF EXISTS DICTIONARY ")

    def table_exists(self) -> bool:
        return self.cursor.fetchone() is not None

    def get_all_records(self) -> Sequence[Word]:
        with self.connection:
            self.cursor.execute(" SELECT * FROM DICTIONARY ")
            return list(map(lambda w: Word(*w), self.cursor.fetchall()))
    
    def get_record_by_word(self, record: str) -> Sequence[Word] :
        with self.connection:
            self.cursor.execute(" SELECT * FROM DICTIONARY WHERE WORD=? ", (record,))
            return Word(*self.cursor.fetchone())
        
    def get_record_by_type(self, phrase: str) -> Sequence[Word]:
        with self.connection:
            self.cursor.execute(" SELECT * FROM DICTIONARY WHERE TYPE=? ", (phrase,))
            return list(map(lambda w: Word(*w), self.cursor.fetchall()))

    def get_record_by_date(self, date: datetime) -> Sequence[Word] :
        with self.connection:
            self.cursor.execute(" SELECT * FROM DICTIONARY WHERE CREATED_AT=?", (date,))
            return list(map(lambda w: Word(*w), self.cursor.fetchall()))
        
    def get_record_by_date_range(self, start_date: datetime, end_date: datetime) -> Sequence[Word]:
        with self.connection:
            self.cursor.execute(" SELECT * FROM DICTIONARY WHERE CREATED_AT BETWEEN ? AND ?",
                                (start_date, end_date,))
            return list(map(lambda w: Word(*w), self.cursor.fetchall()))

    def get_record_by_filter(self, _type, start_date, end_date) -> Sequence[Word]:
        with self.connection:
            if not _type:
                self.cursor.execute(""" SELECT * FROM DICTIONARY WHERE CREATED_AT BETWEEN ? AND ? """,
                                    (start_date, end_date,))
            else:
                self.cursor.execute(""" SELECT * FROM DICTIONARY WHERE TYPE=? AND CREATED_AT BETWEEN ? AND ? """,
                                    (_type, start_date, end_date,))
            return list(map(lambda w: Word(*w), self.cursor.fetchall()))

    def remove_record_by_id(self, id: str):
        with self.connection:
            self.cursor.execute(" DELETE FROM DICTIONARY WHERE ID=? ", (id,))
    
    def update_record(self, record: Word):
        with self.connection:
            self.cursor.execute(" UPDATE DICTIONARY SET WORD=?, DEFINITION=?, TYPE=? WHERE ID = ? ", 
                                (record.word, record.definition, record.type, record.id))
            
    def insert_record(self, record: Word):
        with self.connection:
            if record.created_at:
                self.cursor.execute(""" INSERT INTO DICTIONARY (WORD, DEFINITION, TYPE, CREATED_AT) VALUES 
                                    (?, ?, ?, ?) """, 
                                    (record.word, record.definition, record.type, record.created_at,))
            else:
                self.cursor.execute(""" INSERT INTO DICTIONARY (WORD, DEFINITION, TYPE) VALUES
                                    (?, ?, ?) """, 
                                    (record.word, record.definition, record.type,))


if __name__ == '__main__':
    w1 = Word('Auf Wiedersehen', 'Goodbye.', 'Phrase', datetime.datetime(2025, 6, 1))
    w2 = Word('Guten Morgen', 'Good morning.', 'Phrase', datetime.datetime(2025, 7, 1))
    w3 = Word('es tut mir leid', 'I am sorry.', 'Phrase', datetime.datetime(2025, 8, 1))
    w4 = Word('Hallo', 'Hello.', 'Word')
    w5 = Word('Guten Nact', 'Good night.', 'Phrase')
    
    db = Database()
    # db.insert_word(w1); db.insert_word(w2); db.insert_word(w3); db.insert_word(w4); db.insert_word(w5)
    # rows = db.get_records_by_filter('', datetime.datetime(2025, 11, 27), datetime.datetime(2025, 12,1))
    rows = db.get_all_records()
    for r in rows:
        print(r) 
