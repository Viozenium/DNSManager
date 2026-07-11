import tkinter as tk
from tkinter import ttk, messagebox

from .base import BasePage
from ui.dialogs import DNSDialog


class ManagePage(BasePage):
    def _build(self):
        self._h1("Gestisci Lista DNS")
        self._sub("Aggiungi, modifica o rimuovi server DNS dalla configurazione")
        self._apply_style()
        self._draw_tree()
        self._draw_buttons()

    # --------------------------------------------------------------------
    # Stile Treeview

    def _apply_style(self):
        t = self.t
        s = ttk.Style()
        s.theme_use("default")
        s.configure(
            "DNS.Treeview",
            background=t["card"],
            foreground=t["fg"],
            rowheight=36,
            fieldbackground=t["card"],
            font=("Segoe UI", 10),
        )
        s.configure(
            "DNS.Treeview.Heading",
            background=t["sidebar"],
            foreground=t["fg"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        s.map(
            "DNS.Treeview",
            background=[("selected", t["select_bg"])],
            foreground=[("selected", t["fg"])],
        )

    # --------------------------------------------------------------------
    # Treeview

    def _draw_tree(self):
        tf = tk.Frame(self, bg=self.t["card"])
        tf.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        self._tree = ttk.Treeview(
            tf,
            columns=("name", "primary", "secondary"),
            show="headings",
            style="DNS.Treeview",
        )
        for col, heading, width in [
            ("name", "Nome", 210),
            ("primary", "DNS Primario", 190),
            ("secondary", "DNS Secondario", 190),
        ]:
            self._tree.heading(col, text=heading)
            self._tree.column(col, width=width)

        vsb = ttk.Scrollbar(tf, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self._refresh_tree()

    def _refresh_tree(self):
        self._tree.delete(*self._tree.get_children())
        for e in self.cfg.dns_list:
            self._tree.insert(
                "", "end", values=(e["name"], e["primary"], e.get("secondary", ""))
            )

    # --------------------------------------------------------------------
    # Pulsanti

    def _draw_buttons(self):
        bf = tk.Frame(self, bg=self.t["bg"])
        bf.pack(fill="x", padx=30, pady=10)
        self._btn(bf, "Aggiungi", self._add).pack(side="left", padx=(0, 8))
        self._btn(bf, "Modifica", self._edit, style="secondary").pack(
            side="left", padx=(0, 8)
        )
        self._btn(bf, "Rimuovi", self._remove, style="danger").pack(side="left")
        self._btn(
            bf, "Ripristina Predefiniti", self._reset, style="secondary"
        ).pack(side="right")

    def _add(self):
        d = DNSDialog(self, "Aggiungi DNS", self.t)
        self.wait_window(d)
        if d.result:
            self.cfg.add_dns(d.result)
            self._refresh_tree()

    def _edit(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Attenzione", "Seleziona un DNS da modificare.")
            return
        idx = self._tree.index(sel[0])
        vals = self._tree.item(sel[0])["values"]
        existing = {"name": vals[0], "primary": vals[1], "secondary": vals[2]}
        d = DNSDialog(self, "Modifica DNS", self.t, existing)
        self.wait_window(d)
        if d.result:
            self.cfg.update_dns(idx, d.result)
            self._refresh_tree()

    def _remove(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Attenzione", "Seleziona un DNS da rimuovere.")
            return
        idx = self._tree.index(sel[0])
        name = self._tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Conferma", f"Rimuovere '{name}'?"):
            self.cfg.remove_dns(idx)
            self._refresh_tree()

    def _reset(self):
        if messagebox.askyesno(
            "Ripristina Lista",
            "Ripristinare la lista DNS predefinita? \nTutte le modifiche verranno perse.",
        ):
            self.cfg.reset_dns_list()
            self._refresh_tree()
