import mysql.connector
import os
from datetime import date
from dotenv import load_dotenv
load_dotenv()

def vytvoreni_databaze(database = None):
    try:
        conn_params = {
                "host": os.getenv("DB_HOST", "localhost"),
                "user":  os.getenv("DB_USER", "root"),
                "password": os.getenv("DB_PASSWORD"),
                "port": int(os.getenv("DB_PORT", "3306")),
            }
        
        if not conn_params["password"]:
            raise ValueError("DB_PASSWORD nebylo nastaveno")
        db_name = database or os.getenv("DB_NAME", "task_manager")
        conn = mysql.connector.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.close()
        conn.close()
    except mysql.connector.Error:
        raise
        

def pripojeni_db(database = None ) -> tuple[any,any]:
    """  
    Naváže spojení s databází. Pokud spojení selže 
    funkce vypíše chybovou hlášku a vrátí [None,None].
    Returns: 
        tuple: (conn, cursor) - úspěšné připojení
        tuple: (None, None) - pokud připojení selže
    """
    try:
        conn_params = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user":  os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD"),
            "port": int(os.getenv("DB_PORT", "3306")),
        }
        if database:
            conn_params["database"] = database
        else:
            conn_params["database"] = os.getenv("DB_NAME", "task_manager")
        
        if not conn_params["password"]:
            raise ValueError("DB_PASSWORD nebylo nastaveno")
        conn = mysql.connector.connect(**conn_params)
        cursor = conn.cursor()
        return conn, cursor
        
    except mysql.connector.Error as Err:
        raise

def vytvoreni_tabulky(database=None):
    """
    Vytvoří tabulku 'ukoly' v databázi - pokud již neexistuje. 
    Vypíše chybu, pokud pokus o vytvoření tabulky selže.
    """
    conn, cursor = pripojeni_db(database)
    print("Připojeno k databázi..")

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ukoly (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   nazev VARCHAR(100),
                   popis TEXT,
                   stav VARCHAR(50) DEFAULT 'Nezahájeno',
                   datum DATE
        )
        """)
        print("Tabulka vytvořena..")
        print()
    except mysql.connector.Error:
        raise
    finally:
        conn.close()

def pridat_ukol(nazev:str, popis:str, dnes:date, database = "task_manager") -> None:
    """
    Uloží nový úkol do databáze.
    Funkce příjmá název, popis a datum úkolu jako 
    argumenty a vytvoří nový záznam v databázi.
    """
    if not nazev.strip():
        raise ValueError ("Název úkolu nesmí být prázdný")
    conn, cursor = pripojeni_db(database)
    try:
        cursor.execute("INSERT INTO ukoly (nazev, popis, datum) VALUES (%s, %s, %s)", 
                       (nazev, popis, dnes))
        conn.commit()
        print(f"Úkol {nazev} byl přidán")
    except mysql.connector.Error:
        raise
    finally:
        conn.close()

def zobrazit_ukoly(volba:int, database = "task_manager"):
    """
    Funkce zobrazí úkoly z databáze.
    Přijímá argument volba, na jehož základě filtruje
    zobrazení úkolů na stav: Nezahájeno, Probíhá nebo
    zobrazí všechny úkoly. Součástí funkce je připojení
    k databázi.
    """
    conn, cursor = pripojeni_db(database)

    try:
        if volba == 1:
            cursor.execute("SELECT * FROM ukoly")
        elif volba == 2:
            cursor.execute("SELECT * FROM ukoly WHERE stav = 'Nezahájeno'")
        elif volba == 3:
            cursor.execute("SELECT * FROM ukoly WHERE stav = 'Probíhá'")
        else:
            raise ValueError("Neplatná volba zobrazení úkolů")

        rows = cursor.fetchall()

        if len(rows) == 0:
            print("Žádné úkoly nenalezeny")
        else:
            if volba == 1:
                print("\nVšechny úkoly")
            elif volba == 2:
                print("\nNezahájené úkoly")
            elif volba == 3:
                print("\nProbíhající úkoly")

            for row in rows:
                print(f"ID: {row[0]} - Název: {row[1]} - Popis: {row[2]} - Stav: {row[3]} - Datum: {row[4]}")

        return rows

    except mysql.connector.Error:
        raise

    finally:
        cursor.close()
        conn.close()


def aktualizovat_ukol(volba_ID:int, volba_stav:str, database = "task_manager"):
    """
    Funkce aktualizuje stav úkolu v databázi podle ID úkolu.
    """
    if not volba_ID or not volba_stav:
        raise ValueError("ID a volba změny stavu musí být vyplněny")
    conn, cursor = pripojeni_db(database)
    try:
        cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (volba_stav, volba_ID))
        conn.commit()
        print(f"Úkol s ID: {volba_ID} byl úspěšně aktualizován")
    except mysql.connector.Error: 
        raise
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
    if not volba_ID:
        raise ValueError("ID musí být vyplněno")
    conn, cursor = pripojeni_db(database)
    try:
        cursor.execute("DELETE FROM ukoly WHERE id = %s",(volba_ID,))
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

