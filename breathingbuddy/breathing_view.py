"""Andningsanimation / Breathing animation widget."""

import math
import cairo
from gi.repository import Gtk, GLib


# Phase types for animation behavior
PHASE_INHALE = "in"
PHASE_HOLD = "hold"
PHASE_EXHALE = "out"

# Map action keywords to phase types
_ACTION_MAP = {
    "andas in": PHASE_INHALE,
    "breathe in": PHASE_INHALE,
    "håll": PHASE_HOLD,
    "hold": PHASE_HOLD,
    "paus": PHASE_HOLD,
    "pause": PHASE_HOLD,
    "andas ut": PHASE_EXHALE,
    "breathe out": PHASE_EXHALE,
}


def _classify_phase(action_text):
    """Classify a phase action into inhale/hold/exhale."""
    lower = action_text.lower()
    for keyword, phase_type in _ACTION_MAP.items():
        if keyword in lower:
            return phase_type
    return PHASE_HOLD


class BreathingView(Gtk.DrawingArea):
    """Custom drawing area for breathing animation."""

    def __init__(self):
        super().__init__()
        self.set_content_width(400)
        self.set_content_height(400)
        self.set_draw_func(self._draw)

        # Animation state
        self._progress = 0.0  # 0.0 to 1.0 within current phase
        self._circle_size = 0.3  # Current circle radius (fraction of area)
        self._target_size = 0.3
        self._phase_type = PHASE_HOLD
        self._action_text = ""
        self._timer_text = ""
        self._is_active = False
        self._tick_id = None

        # Colors (calming blue/teal palette)
        self._bg_color = (0.08, 0.09, 0.12)
        self._circle_color = (0.30, 0.65, 0.75, 0.6)
        self._circle_glow = (0.35, 0.75, 0.85, 0.15)
        self._text_color = (0.85, 0.90, 0.92)

    def start_animation(self):
        """Start the animation loop."""
        self._is_active = True
        if self._tick_id is None:
            self._tick_id = self.add_tick_callback(self._on_tick)

    def stop_animation(self):
        """Stop the animation loop."""
        self._is_active = False
        if self._tick_id is not None:
            self.remove_tick_callback(self._tick_id)
            self._tick_id = None

    def set_phase(self, action_text, progress):
        """Update the current phase and progress."""
        self._action_text = action_text
        self._progress = progress
        self._phase_type = _classify_phase(action_text)

        if self._phase_type == PHASE_INHALE:
            self._target_size = 0.25 + 0.20 * progress
        elif self._phase_type == PHASE_EXHALE:
            self._target_size = 0.45 - 0.20 * progress
        else:  # hold
            pass  # Keep current size

        self.queue_draw()

    def set_timer_text(self, text):
        """Set the countdown timer text."""
        self._timer_text = text
        self.queue_draw()

    def set_idle(self):
        """Set to idle state."""
        self._action_text = ""
        self._timer_text = ""
        self._target_size = 0.3
        self._circle_size = 0.3
        self._progress = 0.0
        self.queue_draw()

    def _on_tick(self, widget, frame_clock):
        """Smooth animation tick."""
        # Ease circle_size toward target
        diff = self._target_size - self._circle_size
        self._circle_size += diff * 0.08
        self.queue_draw()
        return GLib.SOURCE_CONTINUE

    def _draw(self, area, cr, width, height):
        """Draw the breathing visualization."""
        # Background
        cr.set_source_rgb(*self._bg_color)
        cr.paint()

        cx, cy = width / 2, height / 2
        max_r = min(width, height) / 2

        # Outer glow rings
        for i in range(3):
            r = max_r * (self._circle_size + 0.02 * (i + 1))
            alpha = self._circle_glow[3] * (1 - i * 0.3)
            cr.set_source_rgba(
                self._circle_glow[0],
                self._circle_glow[1],
                self._circle_glow[2],
                alpha,
            )
            cr.arc(cx, cy, r, 0, 2 * math.pi)
            cr.fill()

        # Main breathing circle with gradient
        r = max_r * self._circle_size
        pattern = cairo.RadialGradient(cx, cy, 0, cx, cy, r)
        pattern.add_color_stop_rgba(
            0,
            self._circle_color[0] + 0.15,
            self._circle_color[1] + 0.15,
            self._circle_color[2] + 0.10,
            self._circle_color[3] + 0.2,
        )
        pattern.add_color_stop_rgba(
            1,
            self._circle_color[0],
            self._circle_color[1],
            self._circle_color[2],
            self._circle_color[3],
        )
        cr.set_source(pattern)
        cr.arc(cx, cy, r, 0, 2 * math.pi)
        cr.fill()

        # Inner subtle particles / shimmer
        time_val = self._progress * math.pi * 2
        for i in range(8):
            angle = (i / 8) * math.pi * 2 + time_val
            dist = r * 0.5
            px = cx + math.cos(angle) * dist
            py = cy + math.sin(angle) * dist
            pr = 2.5
            alpha = 0.3 + 0.2 * math.sin(time_val + i)
            cr.set_source_rgba(0.8, 0.9, 1.0, alpha)
            cr.arc(px, py, pr, 0, 2 * math.pi)
            cr.fill()

        # Action text
        if self._action_text:
            cr.set_source_rgba(*self._text_color, 0.9)
            cr.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.set_font_size(22)
            ext = cr.text_extents(self._action_text)
            cr.move_to(cx - ext.width / 2, cy - 10)
            cr.show_text(self._action_text)

        # Timer text
        if self._timer_text:
            cr.set_source_rgba(*self._text_color, 0.7)
            cr.set_font_size(42)
            ext = cr.text_extents(self._timer_text)
            cr.move_to(cx - ext.width / 2, cy + 40)
            cr.show_text(self._timer_text)
