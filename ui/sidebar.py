import tkinter as tk

FONT = "Segoe UI"
ICON = "ℹ️"  # Uso puramente estetico

NAV = [
    ("apply",    "   Applica DNS"),
    ("manage",   "   Gestisci Lista"),
    ("manual",   "   Modifica Manuale"),
    ("settings", "   Impostazioni"),
]

class Sidebar(tk.Frame):
    def __init__(self, parent, t: dict, on_navigate, on_info=None):
        super().__init__(parent, bg=t["sidebar"], width=210)
        self.pack_propagate(False)
        self.t = t
        self._btns: dict[str, tk.Button] = {}
        self._on_nav = on_navigate
        self._on_info = on_info
        self._build()

    def _build(self):
        t = self.t
        tk.Label(
            self, text="DNS Manager",
            bg=t["sidebar"], fg=t["accent"],
            font=(FONT, 13, "bold"), pady=22,
        ).pack(fill="x", padx=10)
        tk.Frame(self, bg=t["border"], height=1).pack(fill="x", padx=12, pady=4)

        for key, label in NAV:
            b = tk.Button(
                self, text=label,
                bg=t["sidebar"], fg=t["fg"],
                font=(FONT, 11), relief="flat",
                anchor="w", padx=18, pady=10, cursor="hand2", bd=0,
                activebackground=t["hover"], activeforeground=t["fg"],
                command=lambda k=key: self._on_nav(k),
            )
            b.pack(fill="x", pady=2)
            self._btns[key] = b

        # --------------------------------------------------------------------
        # fondo sidebar

        tk.Frame(self, bg=t["border"], height=1).pack(
            fill="x", padx=12, side="bottom", pady=(0, 4)
        )
        tk.Button(
            self, text=ICON + "v1.0.3",
            bg=t["sidebar"], fg=t["muted"],
            font=(FONT, 9), relief="flat", bd=0,
            cursor="hand2" if self._on_info else "",
            activebackground=t["sidebar"], activeforeground=t["accent"],
            command=self._on_info if self._on_info else lambda: None,
        ).pack(side="bottom", pady=10)

    def set_active(self, key: str):
        t = self.t
        for k, b in self._btns.items():
            b.configure(
                bg=t["accent"] if k == key else t["sidebar"],
                fg=t["accent_fg"] if k == key else t["fg"],
            )