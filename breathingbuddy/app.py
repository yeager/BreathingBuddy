"""Huvudapplikation / Main application."""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio

from . import __app_id__
from .window import BreathingWindow


class BreathingBuddyApp(Adw.Application):
    """Main GTK4/Adwaita application."""

    def __init__(self):
        super().__init__(
            application_id=__app_id__,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self._apply_css()

    def do_activate(self):
        """Handle application activation."""
        win = self.get_active_window()
        if not win:
            win = BreathingWindow(application=self)
        win.present()

    def _apply_css(self):
        """Apply custom CSS for calming design."""
        from gi.repository import Gtk, Gdk

        css = b"""
        window {
            background-color: #141519;
        }
        .breathing-title {
            font-size: 24px;
            font-weight: 300;
            color: #d9e6ea;
        }
        .pill {
            border-radius: 24px;
            padding: 8px 24px;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
