"""Huvudfönster / Main application window."""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, GLib, Gio

from .breathing_view import BreathingView
from .techniques import TECHNIQUES, get_technique_name, get_technique_description, get_phase_action
from .settings import load_settings, save_settings
from .session import save_session, get_stats
from .i18n import STRINGS


class BreathingWindow(Adw.ApplicationWindow):
    """Main application window."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._settings = load_settings()
        self._lang = self._settings.get("language", "sv")

        # Session state
        self._is_running = False
        self._is_paused = False
        self._current_technique = self._settings.get("technique", "478")
        self._current_cycle = 0
        self._current_phase = 0
        self._phase_elapsed = 0.0
        self._total_cycles = self._settings.get("cycles", 4)
        self._timer_id = None
        self._session_seconds = 0.0
        self._countdown = 0

        self.set_title("BreathingBuddy")
        self.set_default_size(500, 700)

        self._build_ui()

    def _build_ui(self):
        """Build the complete UI."""
        # Main layout
        self._main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self._main_box)

        # Header bar
        header = Adw.HeaderBar()
        self._main_box.append(header)

        # Stats button
        stats_btn = Gtk.Button(icon_name="document-properties-symbolic")
        stats_btn.set_tooltip_text(STRINGS["statistics"])
        stats_btn.connect("clicked", self._on_stats_clicked)
        header.pack_start(stats_btn)

        # Settings button
        settings_btn = Gtk.Button(icon_name="emblem-system-symbolic")
        settings_btn.set_tooltip_text(STRINGS["settings"])
        settings_btn.connect("clicked", self._on_settings_clicked)
        header.pack_end(settings_btn)

        # Content stack
        self._stack = Gtk.Stack()
        self._stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self._main_box.append(self._stack)

        # --- Main breathing page ---
        breathing_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        breathing_page.set_margin_start(16)
        breathing_page.set_margin_end(16)
        breathing_page.set_margin_bottom(16)
        self._stack.add_named(breathing_page, "breathing")

        # Technique selector
        technique_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        technique_box.set_margin_top(8)
        breathing_page.append(technique_box)

        tech_label = Gtk.Label(label=STRINGS["choose_technique"])
        tech_label.add_css_class("title-4")
        technique_box.append(tech_label)

        self._technique_dropdown = Gtk.DropDown()
        tech_names = [get_technique_name(tid, self._lang) for tid in TECHNIQUES]
        self._tech_ids = list(TECHNIQUES.keys())
        string_list = Gtk.StringList.new(tech_names)
        self._technique_dropdown.set_model(string_list)

        # Set current technique
        if self._current_technique in self._tech_ids:
            self._technique_dropdown.set_selected(self._tech_ids.index(self._current_technique))

        self._technique_dropdown.connect("notify::selected", self._on_technique_changed)
        technique_box.append(self._technique_dropdown)

        # Description
        self._desc_label = Gtk.Label(wrap=True, xalign=0.0)
        self._desc_label.add_css_class("dim-label")
        self._desc_label.set_margin_top(4)
        self._update_description()
        technique_box.append(self._desc_label)

        # Cycles selector
        cycles_box = Gtk.Box(spacing=8)
        cycles_box.set_halign(Gtk.Align.CENTER)
        cycles_box.set_margin_top(4)
        cycles_label = Gtk.Label(label=STRINGS["cycles"] + ":")
        cycles_box.append(cycles_label)

        self._cycles_spin = Gtk.SpinButton.new_with_range(1, 20, 1)
        self._cycles_spin.set_value(self._total_cycles)
        self._cycles_spin.connect("value-changed", self._on_cycles_changed)
        cycles_box.append(self._cycles_spin)
        technique_box.append(cycles_box)

        # Breathing animation
        self._breathing_view = BreathingView()
        self._breathing_view.set_vexpand(True)
        self._breathing_view.set_hexpand(True)
        breathing_page.append(self._breathing_view)

        # Status label
        self._status_label = Gtk.Label(label=STRINGS["breathe"])
        self._status_label.add_css_class("title-2")
        breathing_page.append(self._status_label)

        # Progress label
        self._progress_label = Gtk.Label(label="")
        self._progress_label.add_css_class("dim-label")
        breathing_page.append(self._progress_label)

        # Control buttons
        btn_box = Gtk.Box(spacing=12, halign=Gtk.Align.CENTER)
        btn_box.set_margin_top(8)
        btn_box.set_margin_bottom(8)
        breathing_page.append(btn_box)

        self._start_btn = Gtk.Button(label=STRINGS["start"])
        self._start_btn.add_css_class("suggested-action")
        self._start_btn.add_css_class("pill")
        self._start_btn.set_size_request(130, -1)
        self._start_btn.connect("clicked", self._on_start_clicked)
        btn_box.append(self._start_btn)

        self._pause_btn = Gtk.Button(label=STRINGS["pause"])
        self._pause_btn.add_css_class("pill")
        self._pause_btn.set_size_request(130, -1)
        self._pause_btn.set_sensitive(False)
        self._pause_btn.connect("clicked", self._on_pause_clicked)
        btn_box.append(self._pause_btn)

        # --- Statistics page ---
        self._build_stats_page()

        # --- Settings page ---
        self._build_settings_page()

        # Show main page
        self._stack.set_visible_child_name("breathing")

    def _build_stats_page(self):
        """Build the statistics page."""
        stats_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        stats_page.set_margin_start(24)
        stats_page.set_margin_end(24)
        stats_page.set_margin_top(24)
        self._stack.add_named(stats_page, "stats")

        back_btn = Gtk.Button(icon_name="go-previous-symbolic", halign=Gtk.Align.START)
        back_btn.connect("clicked", lambda _: self._stack.set_visible_child_name("breathing"))
        stats_page.append(back_btn)

        title = Gtk.Label(label=STRINGS["statistics"])
        title.add_css_class("title-1")
        stats_page.append(title)

        self._stats_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        stats_page.append(self._stats_box)

    def _build_settings_page(self):
        """Build the settings page."""
        settings_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        settings_page.set_margin_start(24)
        settings_page.set_margin_end(24)
        settings_page.set_margin_top(24)
        self._stack.add_named(settings_page, "settings")

        back_btn = Gtk.Button(icon_name="go-previous-symbolic", halign=Gtk.Align.START)
        back_btn.connect("clicked", lambda _: self._stack.set_visible_child_name("breathing"))
        settings_page.append(back_btn)

        title = Gtk.Label(label=STRINGS["settings"])
        title.add_css_class("title-1")
        settings_page.append(title)

        # Language setting
        group = Adw.PreferencesGroup()
        settings_page.append(group)

        lang_row = Adw.ComboRow(title=STRINGS["language"])
        lang_model = Gtk.StringList.new(["Svenska", "English"])
        lang_row.set_model(lang_model)
        lang_row.set_selected(0 if self._lang == "sv" else 1)
        lang_row.connect("notify::selected", self._on_lang_changed)
        group.add(lang_row)

        # Notifications toggle
        notif_row = Adw.SwitchRow(title=STRINGS["notifications"])
        notif_row.set_active(self._settings.get("notifications_enabled", True))
        notif_row.connect("notify::active", self._on_notif_changed)
        group.add(notif_row)

    def _update_description(self):
        """Update technique description label."""
        desc = get_technique_description(self._current_technique, self._lang)
        self._desc_label.set_label(desc)

    def _on_technique_changed(self, dropdown, _pspec):
        """Handle technique selection change."""
        idx = dropdown.get_selected()
        if idx < len(self._tech_ids):
            self._current_technique = self._tech_ids[idx]
            tech = TECHNIQUES[self._current_technique]
            self._total_cycles = tech["default_cycles"]
            self._cycles_spin.set_value(self._total_cycles)
            self._update_description()

    def _on_cycles_changed(self, spin):
        """Handle cycles value change."""
        self._total_cycles = int(spin.get_value())

    def _on_start_clicked(self, _btn):
        """Start or stop a breathing session."""
        if self._is_running:
            self._stop_session()
        else:
            self._start_session()

    def _on_pause_clicked(self, _btn):
        """Pause or resume the session."""
        if self._is_paused:
            self._is_paused = False
            self._pause_btn.set_label(STRINGS["pause"])
            self._timer_id = GLib.timeout_add(50, self._tick)
            self._breathing_view.start_animation()
        else:
            self._is_paused = True
            self._pause_btn.set_label(STRINGS["resume"])
            if self._timer_id:
                GLib.source_remove(self._timer_id)
                self._timer_id = None
            self._breathing_view.stop_animation()

    def _start_session(self):
        """Begin a breathing session."""
        self._is_running = True
        self._is_paused = False
        self._current_cycle = 0
        self._current_phase = 0
        self._phase_elapsed = 0.0
        self._session_seconds = 0.0
        self._countdown = 3  # Countdown before start

        self._start_btn.set_label(STRINGS["stop"])
        self._start_btn.remove_css_class("suggested-action")
        self._start_btn.add_css_class("destructive-action")
        self._pause_btn.set_sensitive(True)
        self._technique_dropdown.set_sensitive(False)
        self._cycles_spin.set_sensitive(False)

        self._status_label.set_label(STRINGS["get_ready"])
        self._breathing_view.start_animation()

        # Start with countdown
        self._timer_id = GLib.timeout_add(1000, self._countdown_tick)

    def _countdown_tick(self):
        """Countdown before session starts."""
        if self._countdown > 0:
            self._breathing_view.set_timer_text(str(self._countdown))
            self._countdown -= 1
            return GLib.SOURCE_CONTINUE
        else:
            self._breathing_view.set_timer_text("")
            # Start the actual session
            self._timer_id = GLib.timeout_add(50, self._tick)
            return GLib.SOURCE_REMOVE

    def _tick(self):
        """Main session timer tick (50ms interval)."""
        if not self._is_running or self._is_paused:
            return GLib.SOURCE_REMOVE

        dt = 0.05  # 50ms
        self._session_seconds += dt
        self._phase_elapsed += dt

        tech = TECHNIQUES[self._current_technique]
        phases = tech["phases"]
        phase = phases[self._current_phase]
        duration = phase["duration"]

        # Progress within this phase
        progress = min(self._phase_elapsed / duration, 1.0)

        # Update animation
        action = get_phase_action(phase, self._lang)
        self._breathing_view.set_phase(action, progress)

        # Timer display
        remaining = max(0, duration - self._phase_elapsed)
        self._breathing_view.set_timer_text(str(int(remaining) + 1))

        # Status
        self._status_label.set_label(action)
        self._progress_label.set_label(
            f"{STRINGS['cycles']}: {self._current_cycle + 1} / {self._total_cycles}"
        )

        # Phase complete?
        if self._phase_elapsed >= duration:
            self._phase_elapsed = 0.0
            self._current_phase += 1

            # Cycle complete?
            if self._current_phase >= len(phases):
                self._current_phase = 0
                self._current_cycle += 1

                # All cycles done?
                if self._current_cycle >= self._total_cycles:
                    self._complete_session()
                    return GLib.SOURCE_REMOVE

        return GLib.SOURCE_CONTINUE

    def _complete_session(self):
        """Handle session completion."""
        self._is_running = False
        save_session(self._current_technique, self._total_cycles, self._session_seconds)

        self._status_label.set_label(STRINGS["well_done"])
        self._progress_label.set_label(
            f"{int(self._session_seconds)} s"
        )
        self._breathing_view.stop_animation()
        self._breathing_view.set_idle()

        self._reset_controls()
        self._send_notification()

    def _stop_session(self):
        """Stop session early."""
        self._is_running = False
        if self._timer_id:
            GLib.source_remove(self._timer_id)
            self._timer_id = None

        self._breathing_view.stop_animation()
        self._breathing_view.set_idle()
        self._status_label.set_label(STRINGS["breathe"])
        self._progress_label.set_label("")
        self._reset_controls()

    def _reset_controls(self):
        """Reset control buttons to initial state."""
        self._start_btn.set_label(STRINGS["start"])
        self._start_btn.remove_css_class("destructive-action")
        self._start_btn.add_css_class("suggested-action")
        self._pause_btn.set_sensitive(False)
        self._pause_btn.set_label(STRINGS["pause"])
        self._technique_dropdown.set_sensitive(True)
        self._cycles_spin.set_sensitive(True)

    def _send_notification(self):
        """Send a desktop notification on session complete."""
        app = self.get_application()
        if app:
            notif = Gio.Notification.new(STRINGS["session_complete"])
            notif.set_body(STRINGS["well_done"])
            app.send_notification("session-complete", notif)

    def _on_stats_clicked(self, _btn):
        """Show statistics page."""
        # Refresh stats
        child = self._stats_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self._stats_box.remove(child)
            child = next_child

        stats = get_stats()
        if stats["total_sessions"] == 0:
            lbl = Gtk.Label(label=STRINGS["no_sessions"])
            lbl.add_css_class("dim-label")
            self._stats_box.append(lbl)
        else:
            items = [
                (STRINGS["total_sessions"], str(stats["total_sessions"])),
                (STRINGS["total_minutes"], str(stats["total_minutes"])),
                (STRINGS["streak"], str(stats["streak_days"])),
            ]
            if stats["favorite_technique"]:
                fav = get_technique_name(stats["favorite_technique"], self._lang)
                items.append((STRINGS["favorite"], fav))

            for label_text, value_text in items:
                row = Gtk.Box(spacing=12)
                lbl = Gtk.Label(label=label_text, hexpand=True, xalign=0)
                lbl.add_css_class("title-4")
                val = Gtk.Label(label=value_text, xalign=1)
                val.add_css_class("title-2")
                row.append(lbl)
                row.append(val)
                self._stats_box.append(row)

        self._stack.set_visible_child_name("stats")

    def _on_settings_clicked(self, _btn):
        """Show settings page."""
        self._stack.set_visible_child_name("settings")

    def _on_lang_changed(self, row, _pspec):
        """Handle language change."""
        self._lang = "sv" if row.get_selected() == 0 else "en"
        self._settings["language"] = self._lang
        save_settings(self._settings)

    def _on_notif_changed(self, row, _pspec):
        """Handle notification toggle."""
        self._settings["notifications_enabled"] = row.get_active()
        save_settings(self._settings)
