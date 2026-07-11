import tkinter as tk
from tkinter import messagebox

from .base import BasePage
from dns.backend import apply_dns, get_current_dns, restore_default

FONT = "Segoe UI"
ICON = "🔄"


class ApplyPage(BasePage):
    def _build(self):
        self._sel = tk.StringVar()
        self._h1("Applica DNS")
        self._sub("Seleziona un server DNS dalla lista e applicalo al sistema")
        self._draw_banner()
        self._draw_list()
        self._draw_buttons()

    # --------------------------------------------------------------------
    # Banner DNS attivi

    def _draw_banner(self):
        t = self.t
        info = get_current_dns()
        f = self._card(padx=18, pady=12)
        f.pack(fill="x", padx=30, pady=(0, 10))

        header = tk.Frame(f, bg=t["card"])
        header.pack(fill="x")
        tk.Label(
            header,
            text="DNS Attualmente Attivi",
            bg=t["card"],
            fg=t["accent"],
            font=(FONT, 10, "bold"),
        ).pack(side="left", pady=(0, 6))
        tk.Button(
            header,
            text=ICON,
            bg=t["card"],
            fg=t["muted"],
            font=(FONT, 10),
            relief="flat",
            cursor="hand2",
            command=lambda: self.refresh_cb() if self.refresh_cb else None,
        ).pack(side="right")

        dns_row = tk.Frame(f, bg=t["card"])
        dns_row.pack(fill="x")
        for label, value in [
            ("Primario", info["primary"]),
            ("Secondario", info["secondary"]),
        ]:
            color = t["success"] if value != "—" else t["muted"]
            tk.Label(
                dns_row,
                text=label + ":",
                bg=t["card"],
                fg=t["muted"],
                font=(FONT, 9),
            ).pack(side="left", padx=(0, 4))
            tk.Label(
                dns_row,
                text=value,
                bg=t["card"],
                fg=color,
                font=(FONT, 11, "bold"),
            ).pack(side="left", padx=(0, 24))

        tk.Label(
            f,
            text=f"Fonte: {info['source']}",
            bg=t["card"],
            fg=t["muted"],
            font=(FONT, 8),
        ).pack(anchor="w", pady=(4, 0))

    # --------------------------------------------------------------------
    # Lista DNS

    def _draw_list(self):
        t = self.t
        outer = tk.Frame(self, bg=t["bg"])
        outer.pack(fill="both", expand=True, padx=30)

        canvas = tk.Canvas(outer, bg=t["bg"], highlightthickness=0)
        vsb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=t["bg"])
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        inner.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(win_id, width=canvas.winfo_width()),
        )
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
        )

        dns_list = self.cfg.dns_list
        if not dns_list:
            tk.Label(
                inner,
                text="Nessun DNS configurato. Vai su Gestisci Lista.",
                bg=t["bg"],
                fg=t["muted"],
                font=(FONT, 12),
            ).pack(pady=50)
        else:
            for entry in dns_list:
                self._dns_row(inner, entry)

    def _dns_row(self, parent, entry: dict):
        t = self.t
        f = tk.Frame(parent, bg=t["card"], cursor="hand2")
        f.pack(fill="x", pady=3)

        rb = tk.Radiobutton(
            f,
            variable=self._sel,
            value=entry["name"],
            bg=t["card"],
            activebackground=t["card"],
            selectcolor=t["accent"],
            relief="flat",
        )
        rb.pack(side="left", padx=(14, 6), pady=14)

        info = tk.Frame(f, bg=t["card"])
        info.pack(side="left", fill="x", expand=True, pady=10)
        tk.Label(
            info,
            text=entry["name"],
            bg=t["card"],
            fg=t["fg"],
            font=(FONT, 12, "bold"),
        ).pack(anchor="w")
        sec = entry.get("secondary") or "—"
        tk.Label(
            info,
            text=f"Primario: {entry['primary']}    Secondario: {sec}",
            bg=t["card"],
            fg=t["muted"],
            font=(FONT, 10),
        ).pack(anchor="w")

        def select(_e=None):
            self._sel.set(entry["name"])

        def h_on(_e):
            for w in (f, info, rb, *info.winfo_children()):
                try:
                    w.configure(bg=t["hover"])
                except Exception:
                    pass

        def h_off(_e):
            for w in (f, info, rb, *info.winfo_children()):
                try:
                    w.configure(bg=t["card"])
                except Exception:
                    pass

        for widget in (f, info, *info.winfo_children()):
            widget.bind("<Button-1>", select)
            widget.bind("<Enter>", h_on)
            widget.bind("<Leave>", h_off)

    # --------------------------------------------------------------------
    # Pulsanti

    def _draw_buttons(self):
        bf = tk.Frame(self, bg=self.t["bg"])
        bf.pack(fill="x", padx=30, pady=14)
        self._btn(bf, "Applica DNS Selezionato", self._apply).pack(
            side="left", padx=(0, 10)
        )
        self._btn(
            bf, "Ripristina DNS Default", self._restore, style="secondary"
        ).pack(side="left")

    def _apply(self):
        name = self._sel.get()
        if not name:
            messagebox.showwarning("Attenzione", "Seleziona un DNS dalla lista.")
            return
        entry = next((d for d in self.cfg.dns_list if d["name"] == name), None)
        if entry:
            self._do_apply(entry["primary"], entry.get("secondary", ""))

    def _restore(self):
        if not messagebox.askyesno(
            "Ripristina DNS",
            "Ripristinare i DNS automatici (DHCP)? \nIl sistema tornerà ai server della rete.",
        ):
            return
        try:
            restore_default()
            messagebox.showinfo(
                "Successo", "DNS ripristinati ai valori automatici (DHCP)."
            )
            if self.refresh_cb:
                self.refresh_cb()
        except PermissionError:
            messagebox.showerror("Permessi", "Esegui come Amministratore o con sudo.")
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def _do_apply(self, primary: str, secondary: str = ""):
        try:
            apply_dns(primary, secondary)
            messagebox.showinfo(
                "Successo",
                f"DNS applicato! \n \nPrimario: {primary} \nSecondario: {secondary or '—'}",
            )
            if self.refresh_cb:
                self.refresh_cb()
        except PermissionError:
            messagebox.showerror("Permessi", "Esegui come Amministratore o con sudo.")
        except Exception as e:
            messagebox.showerror("Errore", str(e))
