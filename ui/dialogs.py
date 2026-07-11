import tkinter as tk
from tkinter import messagebox
from dns.backend import validate_ip

FONT = "Segoe UI"

class DNSDialog(tk.Toplevel):

    def __init__(self, parent, title: str, t: dict, existing: dict | None = None):
        super().__init__(parent)
        self.t = t
        self.result = None
        self.title(title)
        self.configure(bg=t["bg"])
        self.resizable(False, False)
        self.geometry("420x310")
        self.transient(parent)
        self.grab_set()

        tk.Label(
            self, text=title, bg=t["bg"], fg=t["fg"], font=(FONT, 14, "bold")
        ).pack(pady=(22, 8))

        self.vars: dict[str, tk.StringVar] = {}
        for label, key in [
            ("Nome", "name"),
            ("DNS Primario", "primary"),
            ("DNS Secondario (opz.)", "secondary"),
        ]:
            tk.Label(
                self, text=label, bg=t["bg"], fg=t["muted"], font=(FONT, 10)
            ).pack(anchor="w", padx=35, pady=(8, 2))
            var = tk.StringVar(value=(existing or {}).get(key, ""))
            self.vars[key] = var
            tk.Entry(
                self,
                textvariable=var,
                bg=t["entry_bg"],
                fg=t["entry_fg"],
                font=(FONT, 11),
                relief="flat",
                insertbackground=t["fg"],
            ).pack(fill="x", padx=35, ipady=7)

        bf = tk.Frame(self, bg=t["bg"])
        bf.pack(pady=22)
        tk.Button(
            bf,
            text="Salva",
            bg=t["accent"],
            fg=t["accent_fg"],
            font=(FONT, 11, "bold"),
            relief="flat",
            padx=22,
            pady=9,
            cursor="hand2",
            command=self._save,
        ).pack(side="left", padx=6)
        tk.Button(
            bf,
            text="Annulla",
            bg=t["btn_2"],
            fg=t["btn_2_fg"],
            font=(FONT, 11),
            relief="flat",
            padx=22,
            pady=9,
            cursor="hand2",
            command=self.destroy,
        ).pack(side="left", padx=6)

    def _save(self):
        name = self.vars["name"].get().strip()
        primary = self.vars["primary"].get().strip()
        secondary = self.vars["secondary"].get().strip()
        if not name:
            messagebox.showerror("Errore", "Il nome è obbligatorio.", parent=self)
            return
        if not validate_ip(primary):
            messagebox.showerror("Errore", "DNS primario non valido.", parent=self)
            return
        if not validate_ip(secondary, allow_empty=True):
            messagebox.showerror("Errore", "DNS secondario non valido.", parent=self)
            return
        self.result = {"name": name, "primary": primary, "secondary": secondary}
        self.destroy()
