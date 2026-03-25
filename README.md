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
- Negativní testy (Neplatné vstupy)
Testují se CRUD operace databáze.

## Technologie:
- Python
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
pip install pytest mysql-connector-python
```
### 3. Nastavení databáze
Je potřeba mít běžící MySQL server a vytvořenou databázi task_manager - pro hlavní program
a task_manager_test pro testování programu.

### 4. Nastavení přístupového hesla
Projekt využívá enviromentální proměnnou DB_PASSWORD. Pro připojení do databáze.
Ve windows se na staví:
```bash
setx DB_PASSWORD "Tvoje_heslo"
```
### 5. Spuštění aplikace
```bash
python main.py
```
### 5. Spuštění testů
```bash
pytest
```
## Poznámka
Po provedení testů se obsah
testovací databáze task_manager_test sám smaže.





