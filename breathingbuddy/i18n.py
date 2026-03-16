"""Internationalisering / i18n helpers."""

import gettext
import locale
import os

_DOMAIN = "breathingbuddy"
_LOCALE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "po")

# Try to set up gettext
try:
    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    pass

_translation = gettext.translation(
    _DOMAIN, localedir=_LOCALE_DIR, languages=["sv"], fallback=True
)

_ = _translation.gettext


def set_language(lang):
    """Switch language at runtime."""
    global _, _translation
    _translation = gettext.translation(
        _DOMAIN, localedir=_LOCALE_DIR, languages=[lang], fallback=True
    )
    _ = _translation.gettext
    return _


# UI strings with Swedish as default, English fallback via gettext
STRINGS = {
    "app_name": "BreathingBuddy",
    "start": "Starta",
    "stop": "Stoppa",
    "pause": "Pausa",
    "resume": "Fortsätt",
    "settings": "Inställningar",
    "statistics": "Statistik",
    "choose_technique": "Välj andningsteknik",
    "cycles": "Cykler",
    "session_complete": "Sessionen klar!",
    "total_sessions": "Totala sessioner",
    "total_minutes": "Totala minuter",
    "streak": "Svit (dagar)",
    "favorite": "Favoritteknik",
    "language": "Språk",
    "notifications": "Påminnelser",
    "theme": "Tema",
    "dark": "Mörkt",
    "light": "Ljust",
    "about": "Om",
    "get_ready": "Gör dig redo...",
    "well_done": "Bra jobbat!",
    "no_sessions": "Inga sessioner ännu",
    "breathe": "Andas",
}
