import tkinter as tk
from tkinter import messagebox, simpledialog

from .base import BasePage
from dns.backend import apply_dns, validate_ip

HINTS = [
    ("Google", "8.8.8.8", "8.8.4.4"),
    ("Cloudflare", "1.1.1.1", "1.0.0.1"),
    ("Quad9", "9.9.9.9", "149.112.112.112"),
    ("AdGuard", "94.140.14.14", "94.140.15.15"),
]


class ManualPage(BasePage):
    def _build(self):
        self._h1("Modifica Manuale")
        self._sub("Inserisci manualmente gli indirizzi DNS da applicare al sistema")
        self._draw_form()
        self._draw_hints()

    # --------------------------------------------------------------------
    # Form

    def _draw_form(self):
        t = self.t
        card = self._card()
        card.pack(fill="x", padx=30, pady=4)

        self._vars: dict[str, tk.StringVar] = {}
        for label, key in [
            ("DNS Primario", "primary"),
            ("DNS Secondario  (opzionale)", "secondary"),
        ]:
            tk.Label(
                card, text=label, bg=t["card"], fg=t["muted"], font=("Segoe UI", 10)
            ).pack(anchor="w", padx=22, pady=(16, 3))
            var = tk.StringVar()
            self._vars[key] = var
            tk.Entry(
                card,
                textvariable=var,
                bg=t["entry_bg"],
                fg=t["entry_fg"],
                font=("Segoe UI", 12),
                relief="flat",
                insertbackground=t["fg"],
            ).pack(fill="x", padx=22, ipady=8)

        tk.Frame(card, bg=t["card"], height=6).pack()
        bf = tk.Frame(card, bg=t["card"])
        bf.pack(fill="x", padx=22, pady=(4, 20))
        self._btn(bf, "Applica", self._apply).pack(side="left", padx=(0, 10))
        self._btn(bf, "Salva in Lista", self._save_to_list, style="secondary").pack(
            side="left"
        )

    # --------------------------------------------------------------------
    # Suggerimenti rapidi

    def _draw_hints(self):
        t = self.t
        card = self._card()
        card.pack(fill="x", padx=30, pady=10)
        tk.Label(
            card,
            text="Suggerimenti rapidi",
            bg=t["card"],
            fg=t["accent"],
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=22, pady=(14, 6))

        for name, p, s in HINTS:
            row = tk.Frame(card, bg=t["card"], cursor="hand2")
            row.pack(fill="x", padx=22, pady=3)

            lbl_name = tk.Label(
                row,
                text=f"{name}:",
                bg=t["card"],
                fg=t["fg"],
                font=("Segoe UI", 10, "bold"),
                width=12,
                anchor="w",
            )
            lbl_name.pack(side="left")

            lbl_dns = tk.Label(
                row,
                text=f"{p}  /  {s}",
                bg=t["card"],
                fg=t["muted"],
                font=("Segoe UI", 10),
            )
            lbl_dns.pack(side="left")
            all_widgets = (row, lbl_name, lbl_dns)

            def fill(_e=None, pi=p, si=s):
                self._vars["primary"].set(pi)
                self._vars["secondary"].set(si)

            def h_on(_e, ws=all_widgets):
                for w in ws:
                    w.configure(bg=t["hover"])

            def h_off(_e, ws=all_widgets):
                for w in ws:
                    w.configure(bg=t["card"])

            for widget in all_widgets:
                widget.bind("<Button-1>", fill)
                widget.bind("<Enter>", h_on)
                widget.bind("<Leave>", h_off)

        tk.Frame(card, bg=t["card"], height=12).pack()

    # --------------------------------------------------------------------
    # Azioni

    def _apply(self):
        p = self._vars["primary"].get().strip()
        s = self._vars["secondary"].get().strip()
        if not validate_ip(p):
            messagebox.showerror("Errore", "DNS primario non valido.")
            return
        if not validate_ip(s, allow_empty=True):
            messagebox.showerror("Errore", "DNS secondario non valido.")
            return
        try:
            apply_dns(p, s)
            messagebox.showinfo(
                "Successo",
                f"DNS applicato!\n\nPrimario:    {p}\nSecondario: {s or '—'}",
            )
            if self.refresh_cb:
                self.refresh_cb()
        except PermissionError:
            messagebox.showerror("Permessi", "Esegui come Amministratore o con sudo.")
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def _save_to_list(self):
        p = self._vars["primary"].get().strip()
        s = self._vars["secondary"].get().strip()
        if not validate_ip(p):
            messagebox.showerror("Errore", "DNS primario non valido.")
            return
        if not validate_ip(s, allow_empty=True):
            messagebox.showerror("Errore", "DNS secondario non valido.")
            return
        name = simpledialog.askstring(
            "Nome DNS", "Inserisci un nome per questo DNS:", parent=self
        )
        if not name:
            return
        self.cfg.add_dns({"name": name.strip(), "primary": p, "secondary": s})
        messagebox.showinfo("Salvato", f"DNS '{name}' aggiunto alla lista.")
