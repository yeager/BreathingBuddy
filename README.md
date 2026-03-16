# BreathingBuddy

Guidad andningsträning med visuella animationer och haptic feedback.
*Guided breathing exercises with visual animations.*

![GTK4](https://img.shields.io/badge/GTK4-Adwaita-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## Funktioner / Features

- **Andningstekniker / Breathing techniques:**
  - 4-7-8 Andning — lugnande teknik för avslappning och sömn
  - Fyrkantsandning (Box Breathing) — stresshantering
  - Buteyko-andning — lugn näsandning med reducerad volym

- **Visuella animationer** — pulserande cirkel som guider andningsrytmen
- **Timer och nedräkning** — tydlig visuell guide för varje fas
- **Progressspårning** — sparar sessionshistorik och visar statistik
- **Svenska/Engelska** — i18n med gettext
- **Desktop-notifikationer** — påminnelse när sessionen är klar
- **Lugn, meditativ design** — mörkt tema med lugnande färgpalett

## Installation

### Förutsättningar / Prerequisites

**Debian/Ubuntu:**
```bash
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1
```

**Fedora:**
```bash
sudo dnf install python3 python3-gobject gtk4 libadwaita
```

**Arch Linux:**
```bash
sudo pacman -S python python-gobject gtk4 libadwaita
```

**macOS (Homebrew):**
```bash
brew install gtk4 libadwaita pygobject3
```

### Kör direkt / Run directly

```bash
git clone https://github.com/yourusername/BreathingBuddy.git
cd BreathingBuddy
python3 main.py
```

### Installera som paket / Install as package

```bash
pip install .
breathingbuddy
```

## Användning / Usage

1. Välj andningsteknik i rullgardinsmenyn
2. Ställ in antal cykler
3. Tryck **Starta** och följ den visuella guiden
4. Andas i takt med den pulserande cirkeln
5. Se din statistik via knappen i verktygsfältet

## Projektstruktur / Project Structure

```
BreathingBuddy/
├── main.py                  # Startpunkt / Entry point
├── breathingbuddy/
│   ├── __init__.py
│   ├── app.py               # GTK Application
│   ├── window.py            # Huvudfönster / Main window
│   ├── breathing_view.py    # Animerad DrawingArea
│   ├── techniques.py        # Andningstekniker
│   ├── settings.py          # JSON-inställningar
│   ├── session.py           # Sessionshantering
│   └── i18n.py              # Internationalisering
├── po/
│   ├── breathingbuddy.pot   # Översättningsmall
│   └── sv/LC_MESSAGES/
│       └── breathingbuddy.po  # Svenska översättningen
├── data/
│   └── com.github.breathingbuddy.desktop
├── setup.py
├── requirements.txt
└── README.md
```

## Teknik / Technology

- **GTK4 + libadwaita** — modernt Linux-desktop UI
- **Python 3** med PyGObject
- **cairo** — 2D-vektorgrafik för andningsanimationer
- **JSON** — inställningar och sessionsdata
- **gettext** — i18n/lokalisering

## Licens / License

MIT
