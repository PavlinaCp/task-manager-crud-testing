"""
projekt_2.py: testovací skript pro druhý projekt  
do Engeto Online Testing Akademie
Obsahuje ukázky automatizovaných testů funkcí 
s CRUD operacemi databáze ze souboru main.py.
author: Pavlína Čepcová
email: cepcovap@gmail.com
"""
import pytest
import mysql.connector
import os
from datetime import date
from main import pridat_ukol, aktualizovat_ukol, odstranit_ukol, pripojeni_db

@pytest.fixture(scope="function")
def db_setup():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password = os.getenv("DB_PASSWORD"),
        database="task_manager_test"
    )
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Nazev VARCHAR(100),
                Popis TEXT,
                Stav VARCHAR(50) DEFAULT 'Nezahájeno',
                Datum DATE
                )
            """)
    conn.commit()
    yield conn, cursor

    cursor.execute("DROP TABLE IF EXISTS ukoly")
    cursor.close()
    conn.close()

#Test funkce pridat_ukol()
#Pozitivni test - Pokus o správné vložení nového úkolu do databaze
#Negativni test - Pokus o vložení příliš dlouhého vstupu (a * 101) do pole Nazev
def test_pridat_ukol_validni(db_setup):
    _, cursor = db_setup
    pridat_ukol("Nový úkol", "Popis nového úkolu", date(2025, 1, 1), 
                database="task_manager_test")
    cursor.execute("SELECT * FROM ukoly WHERE Nazev = 'Nový úkol'")
    result = cursor.fetchone()
    assert result is not None, "Záznam nebyl vložen do tabulky"
    assert result[0] is not None ,"ID nebylo vytvořeno"
    assert result[1] == "Nový úkol", "Název úkolu není správný"
    assert result[2] == "Popis nového úkolu", "Popis úkolu není správný"
    assert result[3] == "Nezahájeno", "Stav úkolu není správný"
    assert result[4] == date(2025, 1, 1), "Datum není správné"

def test_pridat_ukol_nevalidni(db_setup):
    dlouhy_text = "a" * 101
    with pytest.raises(mysql.connector.Error):
        pridat_ukol(dlouhy_text, "Popis úkolu", date(2025, 1, 1), 
                    database="task_manager_test")

#Test funkce aktualizovat_ukol()
#Pozitivni test - Pokus o správné aktualizování nově přidaného úkolu
#Negativni test - Pokus o vložení příliš dlouhého vstupu (a * 101) 
#do pole stavu úkolu.
def test_aktualizovat_ukol_validni(db_setup):
    _, cursor = db_setup
    pridat_ukol("Nový úkol", "Popis nového úkolu", date(2025, 1, 1), 
                database="task_manager_test")
    cursor.execute("SELECT id FROM ukoly WHERE Nazev = 'Nový úkol'")
    ukol_id = cursor.fetchone()[0]
    aktualizovat_ukol(ukol_id,"Hotovo",database="task_manager_test")
    conn2, cursor2 = pripojeni_db(database = "task_manager_test")
    cursor2.execute("SELECT * FROM ukoly WHERE Nazev = 'Nový úkol'")
    result = cursor2.fetchone()
    conn2.close()
    assert result[3] == "Hotovo", "Aktualizace stavu se nezdařila"

def test_aktualizovat_ukol_nevalidni(db_setup):
    _, cursor = db_setup
    pridat_ukol("Nový úkol", "Popis nového úkolu", date(2025, 1, 1), 
                database="task_manager_test")
    cursor.execute("SELECT id FROM ukoly WHERE Nazev = 'Nový úkol'")
    ukol_id = cursor.fetchone()[0]
    spatny_vstup = "a" * 51
    with pytest.raises(mysql.connector.Error):
        aktualizovat_ukol(ukol_id, spatny_vstup, database="task_manager_test")

#Test funkce odstranit_ukol()
#Pozitivni test - Pokus o správné odstranění nově přidaného úkolu
#Negativni test - Pokus o smazání úkolu v prázdné databázi.
def test_odstranit_ukol_validni(db_setup):
    _, cursor = db_setup
    pridat_ukol("Nový úkol", "Popis nového úkolu", date(2025, 1, 1), 
                database="task_manager_test")
    cursor.execute("SELECT id FROM ukoly WHERE Nazev = 'Nový úkol'")
    ukol_id = cursor.fetchone()[0]
    vysledek = odstranit_ukol(ukol_id, database="task_manager_test")
    conn2, cursor2 = pripojeni_db(database = "task_manager_test")
    cursor2.execute("SELECT * FROM ukoly WHERE Nazev = 'Nový úkol'")
    result = cursor2.fetchone()
    conn2.close()
    assert vysledek is True, "Funkce měla vrátit True"
    assert result is None , "Úkol nebyl odstraňen"

def test_odstranit_ukol_nevalidni(db_setup):
    vysledek = odstranit_ukol(999, database="task_manager_test")
    assert vysledek is False, "Funkce měla vrátit False pro neexistující ID"

    








    
