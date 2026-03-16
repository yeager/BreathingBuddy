#!/usr/bin/env python3
"""BreathingBuddy - Guidad andningsträning."""

import sys
from breathingbuddy.app import BreathingBuddyApp


def main():
    app = BreathingBuddyApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
