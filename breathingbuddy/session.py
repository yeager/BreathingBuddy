"""Sessionshantering / Session tracking."""

import json
import os
from datetime import datetime


def _data_dir():
    xdg = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
    path = os.path.join(xdg, "breathingbuddy")
    os.makedirs(path, exist_ok=True)
    return path


def _sessions_path():
    return os.path.join(_data_dir(), "sessions.json")


def load_sessions():
    """Load all saved sessions."""
    path = _sessions_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return []


def save_session(technique_id, cycles, duration_seconds):
    """Save a completed session."""
    sessions = load_sessions()
    sessions.append({
        "date": datetime.now().isoformat(),
        "technique": technique_id,
        "cycles": cycles,
        "duration_seconds": round(duration_seconds, 1),
    })
    path = _sessions_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)


def get_stats():
    """Get summary statistics."""
    sessions = load_sessions()
    if not sessions:
        return {
            "total_sessions": 0,
            "total_minutes": 0,
            "streak_days": 0,
            "favorite_technique": None,
        }

    total_seconds = sum(s.get("duration_seconds", 0) for s in sessions)

    # Count technique usage
    tech_counts = {}
    for s in sessions:
        t = s.get("technique", "unknown")
        tech_counts[t] = tech_counts.get(t, 0) + 1
    favorite = max(tech_counts, key=tech_counts.get) if tech_counts else None

    # Calculate streak
    dates = set()
    for s in sessions:
        try:
            d = datetime.fromisoformat(s["date"]).date()
            dates.add(d)
        except (KeyError, ValueError):
            pass

    streak = 0
    if dates:
        today = datetime.now().date()
        check = today
        from datetime import timedelta
        while check in dates:
            streak += 1
            check -= timedelta(days=1)

    return {
        "total_sessions": len(sessions),
        "total_minutes": round(total_seconds / 60, 1),
        "streak_days": streak,
        "favorite_technique": favorite,
    }
