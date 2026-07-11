import os
import platform
import sys
import tkinter as tk

from .base import BasePage
from config.manager import CONFIG_FILE

THEME_BUTTONS = [
    ("light", "Chiaro", "#f0f2f5", "#1a1a2e"),
    ("dark", "Scuro", "#1e1e2e", "#cdd6f4"),
    ("colored", "Viola", "#12101e", "#a78bfa"),
]
ICON = "⚠️"  # Uso puramente estetico
FONT = "Segoe UI"


def get_os_label() -> str:
    """Rileva correttamente Windows 11 tramite build number (>= 22000)."""
    if platform.system() == "Windows":
        build = sys.getwindowsversion().build
        version = "11" if build >= 22000 else "10"
        return f"Windows {version} (build {build})"
    return f"{platform.system()} {platform.release()}"


class SettingsPage(BasePage):
    def _build(self):
        self._h1("⚙️  Impostazioni")
        self._sub("Personalizza l'aspetto dell'applicazione")
        self._theme_card()
        self._info_card()
        self._warn_card()

    # --------------------------------------------------------------------
    # Tema

    def _theme_card(self):
        t = self.t
        card = self._card()
        card.pack(fill="x", padx=30, pady=6)
        tk.Label(
            card,
            text="Tema interfaccia",
            bg=t["card"],
            fg=t["muted"],
            font=(FONT, 10),
        ).pack(anchor="w", padx=22, pady=(18, 10))

        row = tk.Frame(card, bg=t["card"])
        row.pack(padx=22, anchor="w", pady=(0, 20))
        for key, label, bg, fg in THEME_BUTTONS:
            relief = "sunken" if key == self.cfg.theme else "flat"
            tk.Button(
                row,
                text=label,
                bg=bg,
                fg=fg,
                font=(FONT, 11, "bold"),
                relief=relief,
                padx=22,
                pady=12,
                cursor="hand2",
                command=lambda k=key: self._change(k),
            ).pack(side="left", padx=(0, 12))

    # --------------------------------------------------------------------
    # Info

    def _info_card(self):
        t = self.t
        card = self._card()
        card.pack(fill="x", padx=30, pady=6)
        for label, value in [
            ("File di configurazione", os.path.abspath(CONFIG_FILE)),
            ("Sistema operativo", get_os_label()),
        ]:
            tk.Label(
                card, text=label, bg=t["card"], fg=t["muted"], font=(FONT, 10)
            ).pack(anchor="w", padx=22, pady=(14, 2))
            tk.Label(
                card, text=value, bg=t["card"], fg=t["fg"], font=(FONT, 10)
            ).pack(anchor="w", padx=22, pady=(0, 4))
        tk.Frame(card, bg=t["card"], height=8).pack()

    # --------------------------------------------------------------------
    # Avviso permessi

    def _warn_card(self):
        t = self.t
        card = self._card()
        card.pack(fill="x", padx=30, pady=6)
        tk.Label(
            card,
            text=(
                ICON
                + "  Per applicare le modifiche DNS è necessario eseguire il programma\n"
                "       come Amministratore (Windows) o con sudo (Linux/macOS)."
            ),
            bg=t["card"],
            fg=t["danger"],
            font=(FONT, 10),
            justify="left",
        ).pack(anchor="w", padx=22, pady=14)

    # --------------------------------------------------------------------
    # Cambio tema

    def _change(self, key: str):
        self.cfg.theme = key
        self.cfg.save()
        if self.refresh_cb:
            self.refresh_cb(key)
