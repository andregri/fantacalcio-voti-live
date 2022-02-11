import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
#db_string = "postgresql://fantallenatore:password@localhost:5432/fantacalcio_db"
db_string = os.environ.get('DB_PROD')
db = create_engine(db_string)

class Giocatore:
    def __init__(self, id, nome, ruolo, squadra):
        self.id = id
        self.nome = nome
        self.ruolo = ruolo
        self.squadra = squadra

class Voto:
    def __init__(self, id_giocatore, giornata, voto, eventi, timestamp):
        self.id_giocatore = id_giocatore
        self.giornata = giornata
        self.voto = voto
        self.eventi = eventi
        self.timestamp = timestamp
    
    def __eq__(self, other): 
        if not isinstance(other, Voto):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.voto == other.voto and self.eventi == other.eventi


def init_tables():
    db = create_engine(db_string)
    db.execute("""CREATE TABLE IF NOT EXISTS giocatore (
        id INT PRIMARY KEY,
        nome TEXT,
        ruolo TEXT,
        squadra TEXT
    )""")

    db.execute("""CREATE TABLE IF NOT EXISTS voto (
        id_giocatore INT NOT NULL,
        giornata INT,
        voto REAL,
        eventi TEXT,
        timestamp TIMESTAMP NOT NULL,
        PRIMARY KEY (id_giocatore, timestamp),
        FOREIGN KEY (id_giocatore) REFERENCES giocatore (id)
    )""")


def store_giocatore(giocatore):
    #db = create_engine(db_string)
    result_set = db.execute(text("""
        INSERT INTO giocatore (id, nome, ruolo, squadra) VALUES (
            :id, :nome, :ruolo, :squadra)
        ON CONFLICT DO NOTHING
    """), {
        "id": giocatore.id,
        "nome": giocatore.nome,
        "ruolo": giocatore.ruolo,
        "squadra": giocatore.squadra
    })


def store_voto(voto):
    #db = create_engine(db_string)
    result_set = db.execute(f"""
        INSERT INTO voto (id_giocatore, giornata, voto, eventi, timestamp) VALUES (
            '{voto.id_giocatore}', {voto.giornata}, {voto.voto}, '{voto.eventi}', '{voto.timestamp}')
        ON CONFLICT DO NOTHING
    """)


if __name__ == "__main__":
    init_tables()
