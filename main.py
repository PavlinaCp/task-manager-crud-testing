"""
projekt_2.py: druhý projekt do Engeto Online Testing Akademie
author: Pavlína Čepcová
email: cepcovap@gmail.com
"""
import mysql.connector
import os
from datetime import date

def pripojeni_db(database = "task_manager") -> tuple[any,any]:
    """
    Naváže spojení s databází. Pokud spojení selže 
    funkce vypíše chybovou hlášku a vrátí [None,None].
    Returns: 
        tuple: (conn, cursor) - úspěšné připojení
        tuple: (None, None) - pokud připojení selže
    """
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = os.getenv("DB_PASSWORD"),
            database = database
        )
        cursor = conn.cursor()
        return conn, cursor
        
    except mysql.connector.Error as Err:
        print(f" Nepodařilo se připojit k databázi: {Err}")
        return None, None

def vytvoreni_tabulky():
    """
    Vytvoří tabulku 'ukoly' v databázi - pokud již neexistuje. 
    Vypíše chybu, pokud pokus o vytvoření tabulky selže.
    """
    conn, cursor = pripojeni_db()
    if conn is None:
        return
    else:
        print("Připojeno k databázi..")

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ukoly (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   Nazev VARCHAR(100),
                   Popis TEXT,
                   Stav VARCHAR(50) DEFAULT 'Nezahájeno',
                   Datum DATE
        )
        """)
        print("Tabulka vytvořena..")
        print()
    except mysql.connector.Error as Err:
        print(f"Chyba při vytvoření tabulky: {Err}")
    finally:
        conn.close()

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
    
def pridat_ukol_user_input() -> tuple[str, str, date]:
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
    dnes = date.today()
    return nazev, popis, dnes

def pridat_ukol(nazev:str, popis:str, dnes:date, database = "task_manager") -> None:
    """
    Uloží nový úkol do databáze.
    Funkce příjmá název, popis a datum úkolu jako 
    argumenty a vytvoří nový záznam v databázi.
    """
    conn, cursor = pripojeni_db(database)
    if conn is None:
        return 
    try:
        cursor.execute("INSERT INTO ukoly (Nazev, Popis, Datum) VALUES (%s, %s, %s)", 
                       (nazev, popis, dnes))
        conn.commit()
        print(f"Úkol {nazev} byl přidán")
    except mysql.connector.Error:
        raise
    finally:
        conn.close()

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
            

def zobrazit_ukoly(volba:int):
    """
    Funkce zobrazí úkoly z databáze.
    Přijímá argument volba, na jehož základě filtruje
    zobrazení úkolů na stav: Nezahájeno, Probíhá nebo
    zobrazí všechny úkoly. Součástí funkce je připojení
    k databázi.
    """
    conn, cursor = pripojeni_db()
    if conn is None:
        return
    try:
        if volba == 1:
            cursor.execute("SELECT * FROM ukoly")
            rows = cursor.fetchall()
            if len(rows) == 0:
                print("Žádné úkoly nenalezeny")
            else:
                print()
                print("Všechny úkoly")
                for row in rows:
                    print(f"ID: {row[0]} - Název: {row[1]} - Popis: {row[2]} - Stav: {row[3]} - Datum: {row[4]}")
        if volba == 2:
            cursor.execute("SELECT * FROM ukoly WHERE Stav = 'Nezahájeno'")
            rows = cursor.fetchall()
            if len(rows) == 0:
                print("Žádné úkoly nenalezeny")
            else:
                print()
                print("Nezahájené úkoly")
                for row in rows:
                    print(f"ID: {row[0]} - Název: {row[1]} - Popis: {row[2]} - Stav: {row[3]} - Datum: {row[4]}")
        if volba == 3:
            cursor.execute("SELECT * FROM ukoly WHERE Stav = 'Probíhá'")
            rows = cursor.fetchall()
            if len(rows) == 0:
                print("Žádné úkoly nenalezeny")
            else:
                print()
                print("Probíhající úkoly")
                for row in rows:
                    print(f"ID: {row[0]} - Název: {row[1]} - Popis: {row[2]} - Stav: {row[3]} - Datum: {row[4]}")
    except mysql.connector.Error as Err:
        raise
    finally:
        conn.close()

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
            except mysql.connector.Error as Error: 
                print(f"Chyba při selektu úkolu ve funkci aktualizovat_ukol_user_input: {Error}")
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
        

def aktualizovat_ukol(volba_ID:int, volba_stav:str, database = "task_manager"):
    """
    Funkce aktualizuje stav úkolu v databázi podle ID úkolu.
    """
    conn, cursor = pripojeni_db(database)
    if conn is None:
        return
    try:
        cursor.execute("UPDATE ukoly SET Stav = %s WHERE ID = %s", (volba_stav, volba_ID))
        conn.commit()
        print(f"Úkol s ID: {volba_ID} byl úspěšně aktualizován")
    except mysql.connector.Error: 
        raise
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
            except mysql.connector.Error as Error:
                print(f"Chyba při selektu úkolu ve funkci odstranit_ukol: {Error}")
                continue
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
    
def odstranit_ukol(volba_ID:int, database = "task_manager") -> bool:
    """
    Funkce odstraní úkol z databáze podle ID. Vrátí hodnotu False, 
    pokud v databázi nebyl smazán záznam. True pokud v databázi došlo 
    k smazání úkolu. Součástí funkce je připojení k databázi.
        Returns:
            bool: False (Záznam nesmazán)
            bool: True (Záznam smazán)
    """
    conn, cursor = pripojeni_db(database)
    if conn is None:
        return
    try:
        cursor.execute("DELETE FROM ukoly WHERE ID = %s",(volba_ID,))
        conn.commit()
        print(f"Úkol s ID: {volba_ID} byl úspěšně smazán")
        if cursor.rowcount == 0:
            return False
        else:
            return True
    except mysql.connector.Error: 
        raise
    finally:
        conn.close()

def hlavni_program():
    vytvoreni_tabulky() 
    while True:
        volba = hlavni_menu()
        print("-" * 100)
        if volba == 1:
            try:
                nazev, popis, dnes = pridat_ukol_user_input()
                pridat_ukol(nazev, popis, dnes)
            except mysql.connector.Error as Err:
                print(f"Chyba při vložení úkolu: {Err}")
            print("-" * 100)
        elif volba == 2:
            try:
                volba = zobrazit_ukoly_user_input()
                zobrazit_ukoly(volba)
            except mysql.connector.Error as Err:
                print(f"Chyba při zobrazení úkolu: {Err}")
            print("-" * 100)
        elif volba == 3:
            try:
                zobrazit_ukoly(1)
                print("-" * 100)
                volba_ID, volba_stav = aktualizovat_ukol_user_input()
                aktualizovat_ukol(volba_ID, volba_stav)
            except mysql.connector.Error as Err:
                print(f"Chyba při aktualizaci úkolu: {Err}")
            print("-" * 100)
        elif volba == 4:
            try:
                zobrazit_ukoly(1)
                print("-" * 100)
                volba_ID = odstranit_ukol_user_input()
                if volba_ID is not None:
                    odstranit_ukol(volba_ID)
            except mysql.connector.Error as Err:
                print(f"Chyba při odstranění úkolu: {Err}")
            print("-" * 100)
        else:
            break

if __name__ == "__main__":
    hlavni_program()




   
    


    