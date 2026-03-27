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
from db import (
    pridat_ukol, aktualizovat_ukol, odstranit_ukol, pripojeni_db,
    vytvoreni_databaze, vytvoreni_tabulky, zobrazit_ukoly
)
from dotenv import load_dotenv
load_dotenv()

#Příprava fixture pro testy.
#Zahrňuje vytvoření testovací databáze, tabulky a připojení (setup)
#a následný úklid po testu (teardown)
@pytest.fixture(scope="function")
def db_setup():
    vytvoreni_databaze(database="task_manager_test")
    vytvoreni_tabulky(database="task_manager_test")
    conn, cursor = pripojeni_db(database="task_manager_test")

    yield conn, cursor

    cursor.execute("DROP TABLE IF EXISTS ukoly")
    cursor.close()
    conn.close()

#Test funkce pridat_ukol()
#Pozitivni test - Pokus o správné vložení nového úkolu do databaze 
#Negativni test - Pokus o vložení prázdného vstupu do pole nazev
def test_pridat_ukol_validni(db_setup):
    _, cursor = db_setup
    pridat_ukol("Nový úkol", "Popis nového úkolu", date(2025, 1, 1), 
                database="task_manager_test")
    cursor.execute("SELECT * FROM ukoly WHERE nazev = 'Nový úkol'")
    result = cursor.fetchone()
    assert result is not None, "Záznam nebyl vložen do tabulky"
    assert result[0] is not None ,"ID nebylo vytvořeno"
    assert result[1] == "Nový úkol", "Název úkolu není správný"
    assert result[2] == "Popis nového úkolu", "Popis úkolu není správný"
    assert result[3] == "Nezahájeno", "Stav úkolu není správný"
    assert result[4] == date(2025, 1, 1), "Datum není správné"

def test_pridat_ukol_nevalidni(db_setup):
    with pytest.raises(ValueError):
        pridat_ukol("", "Popis úkolu", date(2025, 1, 1), 
                    database="task_manager_test")
        

#Test funkce zobrazit_ukoly()
#Pozitivní test - Pokus o správné zobrazení úkolů se stavem "probíhá" (volba 3).
#Negativní test - Pokus o zobrazení záznamů při použití neplatné volby filtru zobrazení.
#Fixture db_setup je jako parametr v test_zobrazit_ukoly_nevalidni(db_setup)
#je použita aby zajistila setup a teardown testu.
def test_zobrazit_ukoly_validni(db_setup):
    _, cursor = db_setup  
    pridat_ukol("Nový úkol", "Popis nového úkolu", date(2025, 1, 1), 
                database="task_manager_test")
    cursor.execute("SELECT id FROM ukoly WHERE nazev = 'Nový úkol'")
    ukol_id = cursor.fetchone()[0]
    aktualizovat_ukol(ukol_id,"Probíhá",database="task_manager_test")
    zobrazeni = zobrazit_ukoly(3, database="task_manager_test")
    print(zobrazeni)

def test_zobrazit_ukoly_nevalidni(db_setup):
    with pytest.raises(ValueError):
        zobrazit_ukoly(None, database="task_manager_test")


#Test funkce aktualizovat_ukol()
#Pozitivni test - Pokus o správné aktualizování nově přidaného úkolu
#Negativni test - Pokus o vložení prázdného vstupu do pole změny stavu úkolu.
def test_aktualizovat_ukol_validni(db_setup):
    _, cursor = db_setup
    pridat_ukol("Nový úkol", "Popis nového úkolu", date(2025, 1, 1), 
                database="task_manager_test")
    cursor.execute("SELECT id FROM ukoly WHERE nazev = 'Nový úkol'")
    ukol_id = cursor.fetchone()[0]
    aktualizovat_ukol(ukol_id,"Hotovo",database="task_manager_test")
    conn2, cursor2 = pripojeni_db(database = "task_manager_test")
    cursor2.execute("SELECT * FROM ukoly WHERE nazev = 'Nový úkol'")
    result = cursor2.fetchone()
    conn2.close()
    assert result[3] == "Hotovo", "Aktualizace stavu se nezdařila"

def test_aktualizovat_ukol_nevalidni(db_setup):
    _, cursor = db_setup
    pridat_ukol("Nový úkol", "Popis nového úkolu", date(2025, 1, 1), 
                database="task_manager_test")
    cursor.execute("SELECT id FROM ukoly WHERE nazev = 'Nový úkol'")
    ukol_id = cursor.fetchone()[0]
    with pytest.raises(ValueError):
        aktualizovat_ukol(ukol_id, "", database="task_manager_test")

#Test funkce odstranit_ukol()
#Pozitivni test - Pokus o správné odstranění nově přidaného úkolu
#Negativni test - Pokus o smazání úkolu v prázdné databázi.
#Fixture db_setup je jako parametr v test_odstranit_ukol_nevalidni(db_setup)
#je použita aby zajistila setup a teardown testu.

def test_odstranit_ukol_validni(db_setup):
    _, cursor = db_setup
    pridat_ukol("Nový úkol", "Popis nového úkolu", date(2025, 1, 1), 
                database="task_manager_test")
    cursor.execute("SELECT id FROM ukoly WHERE nazev = 'Nový úkol'")
    ukol_id = cursor.fetchone()[0]
    vysledek = odstranit_ukol(ukol_id, database="task_manager_test")
    conn2, cursor2 = pripojeni_db(database = "task_manager_test")
    cursor2.execute("SELECT * FROM ukoly WHERE nazev = 'Nový úkol'")
    result = cursor2.fetchone()
    conn2.close()
    assert vysledek is True, "Funkce měla vrátit True"
    assert result is None , "Úkol nebyl odstraňen"

def test_odstranit_ukol_nevalidni(db_setup):
    vysledek = odstranit_ukol(999, database="task_manager_test")
    assert vysledek is False, "Funkce měla vrátit False pro neexistující ID"
