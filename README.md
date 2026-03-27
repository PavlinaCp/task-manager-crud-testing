# Task Manager s testováním
Jednoduchý CLI správce úkolů v pythonu s napojením na MySQL databázi a automatizovanými testy pomocí pytest.
Projekt vznikl jako součást Online Testing akademie (Engeto)

## Funkce
- Přidání úkolu
- Zobrazení úkolu
- Aktualizace úkolu
- Odstanění úkolu

## Testování
Projekt obsahuje automatizované testy pomocí pytest:
- Pozitivní testy (správné vstupy)
- Negativní testy (neplatné vstupy)
Testují se CRUD operace databáze.

## Technologie:
- python
- MySQL
- pytest

## Instrukce ke spuštění a instalaci
### 1. Klonování repozitáře
```bash
git clone https://github.com/PavlinaCp/task-manager-crud-testing.git
cd task-manager-crud-testing
```
### 2. Instalace knihoven
```bash
pip install -r requirements.txt
```
### 3. Nastavení souboru .env
Vytvořte soubor `.env` v kořenové složce projektu a nastavte:
```bash
DB_HOST=localhost                     #volitelné (default localhost)
DB_USER=root                          #volitelné (default root)
DB_PASSWORD=vaše_heslo                #povinné
DB_PORT=3306                          #volitelné (default 3306)
DB_NAME=task_manager                  #volitelné (default task_manager)
```

### 3. Spuštění aplikace
```bash
python main.py
```
### 4. Spuštění testů
```bash
pytest
```
## Poznámky
- Před spuštěním projektu je nutné mít nainstalovaný a spuštěný MySQL server.
- Databáze a tabulka 'ukoly' se při spuštění automaticky vytvoří, pokud ještě neexistují.
- Po provedení testů se obsah testovací databáze task_manager_test automaticky smaže.
  





