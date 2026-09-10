import json
import os
import shutil
import sqlite3
import zipfile
from datetime import datetime

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_DIR, "data")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
DB_FILE = os.path.join(DATA_DIR, "app_data.sqlite3")


def _ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)


def default_state():
    return {
        "records": [],
        "labor_records": [],
        "payroll_expenses": [],
        "planner_tasks": [],
        "budget": 0,
        "budget_history": [],
        "remaining_money": 0,
        "view": "home",
        "receipt_archive": [],
        "project": {"name": "Ailyn House Project", "status": "Active"},
        "scanner_photos": [],
        "dark_mode": False,
        "client_notes": "",
        "app_settings": {},
        "messages": [],
        "dashboard_tracker": {},
        "puzzle_level": 1,
        "puzzle_score": 0,
        "puzzle_streak": 0,
        "puzzle_seed": 1,
        "math_level": 1,
        "math_score": 0,
        "math_streak": 0,
        "math_seed": 1,
        "financial_closes": {},
        "offline_mode": True,
    }


def load_state():
    _ensure_dirs()
    path = os.path.join(DATA_DIR, "app_state.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, dict):
                merged = default_state()
                merged.update(data)
                return merged
        except (json.JSONDecodeError, OSError):
            pass
    return default_state()


def save_state(state):
    _ensure_dirs()
    if state is None:
        state = default_state()
    path = os.path.join(DATA_DIR, "app_state.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, default=str)
    return state


def create_backup():
    _ensure_dirs()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"app_backup_{timestamp}.zip")
    with zipfile.ZipFile(backup_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for root, _, files in os.walk(DATA_DIR):
            for filename in files:
                full_path = os.path.join(root, filename)
                if full_path == backup_path:
                    continue
                arcname = os.path.relpath(full_path, DATA_DIR)
                archive.write(full_path, arcname)
    return backup_path


def restore_backup(backup_path):
    if not backup_path or not os.path.exists(backup_path):
        return default_state()
    if backup_path.endswith(".zip"):
        target_dir = os.path.join(DATA_DIR, "restore_tmp")
        shutil.rmtree(target_dir, ignore_errors=True)
        with zipfile.ZipFile(backup_path, "r") as archive:
            archive.extractall(target_dir)
        state_path = os.path.join(target_dir, "app_state.json")
        if os.path.exists(state_path):
            with open(state_path, "r", encoding="utf-8") as handle:
                return json.load(handle)
    return default_state()


def save_scanner_photo(photo_bytes, mime_type, photo_id):
    _ensure_dirs()
    folder = os.path.join(DATA_DIR, "scanner_photos")
    os.makedirs(folder, exist_ok=True)
    file_name = f"{photo_id}.{mime_type.split('/')[-1] if '/' in mime_type else 'jpg'}"
    path = os.path.join(folder, file_name)
    with open(path, "wb") as handle:
        handle.write(photo_bytes)
    return os.path.relpath(path, DATA_DIR)


def delete_scanner_photo(path):
    if not path:
        return
    full_path = os.path.join(DATA_DIR, path)
    if os.path.exists(full_path):
        os.remove(full_path)


def history_count():
    return 0


def load_sqlite_state():
    return load_state()


def save_sqlite_state(state):
    return save_state(state)
