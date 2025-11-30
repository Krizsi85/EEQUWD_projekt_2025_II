# Krizsán Tamás EEQUWD DUE Szkript nyelvek - DUEL-ISR-116-HU - 2025-2026-1 - Levelező Projekt feladat

# WatchDog program agent

import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import time
import os
import logging
from logging.handlers import RotatingFileHandler

from process_checker import ProcessChecker, ProcessStatus
from program_loader import ProgramLoader


# --- CONFIG ---
PROGRAM_LIST_FILE = r"C:\Watchdog\programs.txt"
CHECK_INTERVAL = 5                       # másodperc
RESTART_COOLDOWN = 30                    # másodperc – legalább ennyit vár egy sikertelen restart után
LOG_PATH = r"C:\Watchdog\logs\watchdog.log"
LOG_MAX_BYTES = 1024 * 1024              # 1 MB rotálás
LOG_BACKUP_COUNT = 5


# --- LOGGER ---
logger = logging.getLogger("Watchdog")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_PATH, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class WatchdogService(win32serviceutil.ServiceFramework):
    _svc_name_ = "WatchdogService"
    _svc_display_name_ = "Python Watchdog Service"
    _svc_description_ = "Folyamatosan felügyeli és újraindítja a kijelölt alkalmazásokat."

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 1, 0, None)
        self.stop_requested = False
        self.last_restart = {}  # path → timestamp

    def SvcStop(self):
        logger.info("WatchdogService stop requested.")
        self.stop_requested = True
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        logger.info("WatchdogService started.")
        servicemanager.LogInfoMsg("WatchdogService started")

        if not os.path.exists(PROGRAM_LIST_FILE):
            msg = f"Program list not found: {PROGRAM_LIST_FILE}"
            logger.error(msg)
            servicemanager.LogErrorMsg(msg)
            return

        paths = ProgramLoader.load_paths(PROGRAM_LIST_FILE)
        checkers = [ProcessChecker(p) for p in paths]

        logger.info(f"Loaded {len(paths)} programs from TXT.")

        while not self.stop_requested:
            now = time.time()

            for checker in checkers:
                status, info = checker.check()
                exe = checker.exe_path

                if status == ProcessStatus.ONLINE:
                    continue

                elif status == ProcessStatus.MULTIPLE:
                    logger.warning(f"Multiple instances running: {exe}")
                    continue

                elif status == ProcessStatus.OFFLINE:
                    last = self.last_restart.get(exe, 0)

                    if now - last < RESTART_COOLDOWN:
                        logger.info(f"Restart cooldown active for {exe}, waiting...")
                        continue

                    logger.info(f"Starting: {exe}")
                    try:
                        subprocess.Popen([exe])
                        self.last_restart[exe] = now
                    except Exception as e:
                        logger.error(f"Failed to start {exe}: {e}")

            time.sleep(CHECK_INTERVAL)

        logger.info("WatchdogService stopped.")
        servicemanager.LogInfoMsg("WatchdogService stopped")


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(WatchdogService)


