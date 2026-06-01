"""
LocalDataManager - Singleton local storage for the Vor application.
Persists user preferences, CV drafts, and UI state across sessions
using a JSON file stored in the project directory.
"""

import json
import os
import threading


class LocalDataManager:
    """
    Thread-safe Singleton that manages local JSON-based persistence.
    
    Usage:
        from modules.local_storage import local_data
        local_data.save("cv_draft.name", "Bùi Lê Công Hậu")
        name = local_data.get("cv_draft.name", "Default Name")
    """

    _instance = None
    _lock = threading.Lock()
    _DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".app_data.json")

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._data = {}
        self._load_from_disk()

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def save(self, key: str, value) -> None:
        """
        Save a value under a dot-notation key.
        Example: save("cv_draft.name", "John") stores {"cv_draft": {"name": "John"}}
        """
        keys = key.split(".")
        target = self._data
        for k in keys[:-1]:
            if k not in target or not isinstance(target[k], dict):
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    def get(self, key: str, default=None):
        """
        Retrieve a value using dot-notation key.
        Returns `default` if the key path does not exist.
        """
        keys = key.split(".")
        target = self._data
        for k in keys:
            if not isinstance(target, dict) or k not in target:
                return default
            target = target[k]
        return target

    def delete(self, key: str) -> bool:
        """Remove a key. Returns True if successfully deleted."""
        keys = key.split(".")
        target = self._data
        for k in keys[:-1]:
            if not isinstance(target, dict) or k not in target:
                return False
            target = target[k]
        if isinstance(target, dict) and keys[-1] in target:
            del target[keys[-1]]
            return True
        return False

    def get_all(self) -> dict:
        """Return a copy of the entire data store."""
        return dict(self._data)

    # ------------------------------------------------------------------
    # Disk I/O
    # ------------------------------------------------------------------

    def save_to_disk(self) -> None:
        """Flush the in-memory data to the JSON file on disk."""
        try:
            filepath = os.path.normpath(self._DATA_FILE)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            print(f"LocalDataManager: Saved to {filepath}")
        except Exception as e:
            print(f"LocalDataManager: Error saving to disk — {e}")

    def _load_from_disk(self) -> None:
        """Load existing data from the JSON file, or start fresh."""
        try:
            filepath = os.path.normpath(self._DATA_FILE)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
                print(f"LocalDataManager: Loaded from {filepath}")
            else:
                self._data = {}
                print("LocalDataManager: No existing data file, starting fresh.")
        except json.JSONDecodeError:
            print("LocalDataManager: Corrupted JSON file detected, resetting data.")
            self._data = {}
        except Exception as e:
            print(f"LocalDataManager: Error loading from disk — {e}")
            self._data = {}


# Module-level convenience instance (Singleton)
local_data = LocalDataManager()
