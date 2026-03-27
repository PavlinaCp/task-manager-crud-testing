"""
projekt_2.py: druhý projekt do Engeto Online Testing Akademie
author: Pavlína Čepcová
email: cepcovap@gmail.com
"""
import mysql.connector
from datetime import date
from db import (
    pripojeni_db, vytvoreni_tabulky, pridat_ukol, zobrazit_ukoly,
    aktualizovat_ukol, odstranit_ukol, vytvoreni_databaze
)

def hlavni_menu() -> int:
    """
    Zobrazí hlavní menu a umožní uživateli vybrat jednu z dostupných možností.
    Funkce zajišťuje validaci vstupu uživatele.
        Returns:
            int: číslo zvolené možnosti (1-5)
    """
    vyber1 = "1. Přidat nový úkol"
    vyber2 = "2. Zobrazit úkoly"
    vyber3 = "3. Aktualizovat úkol"
    vyber4 = "4. Odstranit úkol"
    vyber5 = "5. Ukončit program"
    print("Správce úkolů - Hlavní menu")
    print(vyber1)
    print(vyber2)
    print(vyber3)
    print(vyber4)
    print(vyber5)
    while True:
        zvoleno = input("Vyberte možnost (1-5): ")
        print()
        if not zvoleno.isdigit():
            print("Neplatná volba - Zadejte číslo")
            continue
        zvoleno = int(zvoleno)
        if  zvoleno < 1 or zvoleno > 5:
            print("Neplatná volba - Zadejte číslo 1-5")
            continue
        return zvoleno
    
def pridat_ukol_user_input() -> tuple[str, str]:
    """
    Funkce si vyžádá dva vstupy od uživatele - "nazev" a "popis"
    úkolu. Oba vstupy validuje. Nakonec připraví proměnou "dnes"
    s aktuálním datem. Výstupy funkce jsou připraveny jako 
    argumenty pro funci pridat_ukol()
        Returns:
            str: nazev 
            str: popis
            date: dnes
    """
    while True:
        nazev = input("Zadejte název úkolu: ")
        if len(nazev) == 0:
            print("Nezadali jste název úkolu")
        else:
            break
    while True:
        popis = input("Zadejte popis úkolu: ")
        if len(popis) == 0:
            print("Nezadali jste popis úkolu")
        else:
            break
    return nazev, popis

def zobrazit_ukoly_user_input() -> int:
    """
    Zobrazí možnosti volby filtru zobrazení úkolů (1-3).
    Vstup uživatele validuje. Výstup funkce je připraven
    jako argument funkce zobrazit_ukoly()
        Returns:
            int: volba
    +"""
    while True:
        print("Které úkoly chcete zobrazit?")
        print("1. Všechny úkoly")
        print("2. Nezahájené úkoly")
        print("3. Probíhající úkoly")
        volba = input("Vyberte z možností 1-3: ")    
        if not volba.isdigit():
            print("Nesprávná volba")
            continue
        volba = int(volba)
        if volba not in [1,2,3]:
            print("Nesprávná volba")
            continue
        else:
            return volba
            

def aktualizovat_ukol_user_input(database="task_manager") -> tuple[int, str]:
    """
    Funkce si nejdříve vyžádá od uživatele ID úkolu,
    zjistí v databázi zda úkol pod zvoleným ID existuje.
    Poté uživatele vyzve k jedné ze dvou možností úpravy
    úkolu. Součástí funkce je validace vstupu a navázání 
    spojení s databází.
        Returns:
            int: volba_ID
            str: volba_stav
    """
    conn, cursor = pripojeni_db(database)
    if conn is None:
        return
    zobrazit_ukoly(1)
    print("-" * 100)
    print()
    try:
        while True: 
            volba_ID = input("Napiste ID úkolu k aktualizaci: ")
            if not volba_ID.isdigit():
                print("Spatna volba")
                continue
            volba_ID = int(volba_ID)
            try:
                cursor.execute("SELECT * FROM ukoly WHERE ID = %s", (volba_ID,))
                existujici_ID = cursor.fetchone()
                if existujici_ID is None:
                    print("Úkol pod tímto ID neexistuje.")
                    continue
            except mysql.connector.Error: 
                raise
            volba_stav = input('Změna stavu úkolu. Zvolte 1 - "Probíhá" nebo 2 - "Hotovo": ')
            if not volba_stav.isdigit():
                print("Spatna volba")
                continue
            if not volba_stav in ["1","2"]:
                print("Spatna volba")
                
                continue
            if volba_stav == "1":
                volba_stav = 'Probíhá'
            else:
                volba_stav = 'Hotovo'
            return volba_ID, volba_stav
    finally:
        conn.close()
        

def odstranit_ukol_user_input() -> int:
    """
    Funkce se dotáže uživatele na ID úkolu, ověří jeho existenci 
    a vrátí ID pro smazání, pokud uživatel potvrdí. 
    Součástí funkce je validace vstupu od uživatele a připojení
    k databázi.
        Returns:
            int: volba_ID
    """
    conn, cursor = pripojeni_db()
    if conn is None:
        return
    zobrazit_ukoly(1)
    print("-" * 100)
    print()
    try:
        while True: 
            volba_ID = input("Napiste ID úkolu který chcete odstranit: ")
            if not volba_ID.isdigit():
                print("Spatna volba")
                continue
            volba_ID = int(volba_ID)
            try:
                cursor.execute("SELECT * FROM ukoly WHERE ID = %s", (volba_ID,))
                existujici_ID = cursor.fetchone()
                if existujici_ID is None:
                    print("Úkol pod tímto ID neexistuje.")
                    continue
            except mysql.connector.Error:
                raise
            print(f"Opravdu chcete úkol s ID: {volba_ID} vymazat?" )
            print()
            potvrzeni = input("Zvolte: ANO, smazat - 1 nebo NE, ponechat - 2: ")
            if not potvrzeni.isdigit():
                print("Spatna volba")
                continue
            if not potvrzeni in ["1","2"]:
                print("Spatna volba")
                continue
            elif potvrzeni == "2":
                print()
                print(f"Úkol s ID: {volba_ID} nebyl smazán")
                break
            else:
                return volba_ID
    finally: 
        conn.close()
    

def hlavni_program():
    vytvoreni_databaze()
    vytvoreni_tabulky() 
    while True:
        volba = hlavni_menu()
        print("-" * 100)
        if volba == 1:
            dnes = date.today()
            nazev, popis = pridat_ukol_user_input()
            pridat_ukol(nazev, popis, dnes)
            print("-" * 100)
        elif volba == 2:
            volba = zobrazit_ukoly_user_input()
            zobrazit_ukoly(volba)
            print("-" * 100)
        elif volba == 3:
            volba_ID, volba_stav = aktualizovat_ukol_user_input()
            aktualizovat_ukol(volba_ID, volba_stav)
            print("-" * 100)
        elif volba == 4:
            volba_ID = odstranit_ukol_user_input()
            if volba_ID is not None:
                odstranit_ukol(volba_ID)
            print("-" * 100)
        else:
            break

if __name__ == "__main__":
    try:
        hlavni_program()
    except ValueError as e:
        print(f"Chyba konfigurace: {e}")
    except mysql.connector.Error as e:
        print(f"Chyba databáze: {e}")




   
    


    