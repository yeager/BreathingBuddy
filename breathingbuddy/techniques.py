"""Andningstekniker / Breathing techniques."""


TECHNIQUES = {
    "478": {
        "name_sv": "4-7-8 Andning",
        "name_en": "4-7-8 Breathing",
        "description_sv": (
            "En lugnande teknik som hjälper dig att slappna av och somna. "
            "Andas in genom näsan i 4 sekunder, håll andan i 7 sekunder, "
            "och andas ut genom munnen i 8 sekunder."
        ),
        "description_en": (
            "A calming technique that helps you relax and fall asleep. "
            "Breathe in through your nose for 4 seconds, hold for 7 seconds, "
            "and breathe out through your mouth for 8 seconds."
        ),
        "phases": [
            {"action_sv": "Andas in", "action_en": "Breathe in", "duration": 4},
            {"action_sv": "Håll andan", "action_en": "Hold", "duration": 7},
            {"action_sv": "Andas ut", "action_en": "Breathe out", "duration": 8},
        ],
        "default_cycles": 4,
    },
    "box": {
        "name_sv": "Fyrkantsandning",
        "name_en": "Box Breathing",
        "description_sv": (
            "En teknik som används av militären för att hantera stress. "
            "Varje fas varar i 4 sekunder: andas in, håll, andas ut, håll."
        ),
        "description_en": (
            "A technique used by the military to manage stress. "
            "Each phase lasts 4 seconds: breathe in, hold, breathe out, hold."
        ),
        "phases": [
            {"action_sv": "Andas in", "action_en": "Breathe in", "duration": 4},
            {"action_sv": "Håll andan", "action_en": "Hold", "duration": 4},
            {"action_sv": "Andas ut", "action_en": "Breathe out", "duration": 4},
            {"action_sv": "Håll andan", "action_en": "Hold", "duration": 4},
        ],
        "default_cycles": 4,
    },
    "buteyko": {
        "name_sv": "Buteyko-andning",
        "name_en": "Buteyko Breathing",
        "description_sv": (
            "En teknik som fokuserar på lugn näsandning med reducerad volym. "
            "Andas in lugnt, andas ut avslappnat, och gör en kort paus."
        ),
        "description_en": (
            "A technique focusing on calm nasal breathing with reduced volume. "
            "Breathe in gently, breathe out relaxed, and make a short pause."
        ),
        "phases": [
            {"action_sv": "Andas in lugnt", "action_en": "Breathe in gently", "duration": 3},
            {"action_sv": "Andas ut", "action_en": "Breathe out", "duration": 3},
            {"action_sv": "Paus", "action_en": "Pause", "duration": 4},
        ],
        "default_cycles": 6,
    },
}


def get_technique_name(technique_id, lang="sv"):
    """Get technique name in specified language."""
    tech = TECHNIQUES[technique_id]
    return tech[f"name_{lang}"] if f"name_{lang}" in tech else tech["name_en"]


def get_technique_description(technique_id, lang="sv"):
    """Get technique description in specified language."""
    tech = TECHNIQUES[technique_id]
    key = f"description_{lang}"
    return tech[key] if key in tech else tech["description_en"]


def get_phase_action(phase, lang="sv"):
    """Get phase action text in specified language."""
    key = f"action_{lang}"
    return phase[key] if key in phase else phase["action_en"]


def total_cycle_duration(technique_id):
    """Get total duration of one cycle in seconds."""
    return sum(p["duration"] for p in TECHNIQUES[technique_id]["phases"])
