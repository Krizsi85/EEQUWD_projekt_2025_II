# Krizsán Tamás EEQUWD DUE Szkript nyelvek - DUEL-ISR-116-HU - 2025-2026-1 - Levelező Projekt feladat

WatchDog Agent – ReadMe.txt

---

1. Rövid áttekintés

A WatchDog Agent egy Windows-szolgáltatásként futó Python program, amely egy külső konfigurációs fájlban megadott futtatható állományokat (programokat) figyel, és ha bármelyik nem aktív, megkísérli újraindítani

A szolgáltatás periodikusan ellenőrzi a célfolyamatokat, naplózza az eseményeket, és biztosítja, hogy ne történjen gyors egymásutáni (100+/perc) újraindítási ciklus.

A konfigurációs fájl (programs.txt) minden sora egy futtatható alkalmazás teljes elérési útja. Kivéve a #-el kezdődö sorok.

A program Windows alatt fut, és a pywin32 csomaggal regisztrálható szolgáltatásként.

---

2. Könyvtárstruktúra

main.py – a szolgáltatás belépési pontja

programs.txt – figyelt programok listája

C:\Watchdog\logs\watchdog.log – a szolgáltatás naplófájlja

---

3. Használt modulok

Beépített Python modulok:

os – fájl- és útvonalkezelés

time – késleltetés, ciklusidő

subprocess – programok indítása

logging – naplózás

logging.handlers – RotatingFileHandler log-rotációhoz

threading – leállítás/vezérlés támogatása

sys – szolgáltatás entry point kezelése

Telepítendő külső modulok:

psutil – folyamatok ellenőrzése, PID-listák kezelése

pywin32 – Windows Service API (win32service, win32serviceutil, win32event)

---

4. Fő osztályok és függvények

4.1 WatchdogService (Windows-szolgáltatás osztály)

Metódusok:

SvcDoRun() – a szolgáltatás indítási logikája, fő ciklus meghívása

SvcStop() – szolgáltatás leállítása, esemény jelzése Windows felé

main() – a pywin32 szolgáltatás belépési pontja

4.2 load_programs()

Beolvassa a programs.txt tartalmát, listává alakítja, üres sorokat kiszűri.

4.3 is_process_running(exe_name)

A psutil segítségével ellenőrzi, hogy a megadott futtatható névvel fut-e folyamat a rendszerben.

4.4 start_process(path)

Megkísérli elindítani a hiányzó programot.
Naplózza a sikeres vagy sikertelen indítást.

4.5 monitor_loop()

A szolgáltatás fő ciklusa:

programok ellenőrzése

hiányzó folyamatok indítása

restart-throttling (újraindítási limit) kezelése

ciklusidő: 5–10 másodperc

---

5. Logolási rendszer

A program RotatingFileHandler-t használ:

Log fájl: C:\Watchdog\logs\watchdog.log

Maximum méret: 5 MB

Backup fájlok: 5 db

A log tartalmazza:

szolgáltatás indulási/leállási eseményeket

futó vagy hiányzó processzeket

újraindítási próbálkozásokat

hibákat és kivételeket

6. Telepítés és futtatás

Telepítés:
pip install pywin32
pip install psutil
A szolgáltatás telepítése:
python main.py install
Indítás:
python main.py start
Leállítás:
python main.py stop
Eltávolítás:
python main.py remove

---

7. Megjegyzések

A programs.txt minden sora egy teljes útvonalú .exe vagy futtatható fájl.

A szolgáltatás automatikusan létrehozza a log-könyvtárat, ha nem létezik.

Az újraindítási logika védi a rendszert a túl gyors ciklusoktól.
