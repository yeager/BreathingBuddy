"""Användarinställningar / User settings management."""

import json
import os


DEFAULT_SETTINGS = {
    "language": "sv",
    "technique": "478",
    "cycles": 4,
    "notifications_enabled": True,
    "reminder_interval_minutes": 60,
    "theme": "dark",
}


def _settings_dir():
    xdg = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    path = os.path.join(xdg, "breathingbuddy")
    os.makedirs(path, exist_ok=True)
    return path


def _settings_path():
    return os.path.join(_settings_dir(), "settings.json")


def load_settings():
    """Load settings from JSON file, returning defaults for missing keys."""
    settings = dict(DEFAULT_SETTINGS)
    path = _settings_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                stored = json.load(f)
            settings.update(stored)
        except (json.JSONDecodeError, OSError):
            pass
    return settings


def save_settings(settings):
    """Save settings to JSON file."""
    path = _settings_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
