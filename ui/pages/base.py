import threading
import tkinter as tk

FONT = "Segoe UI"


class BasePage(tk.Frame):

    def __init__(self, parent, t: dict, cfg, refresh_cb=None):
        super().__init__(parent, bg=t["bg"])
        self.t = t
        self.cfg = cfg
        self.refresh_cb = refresh_cb
        self._build()

    def _build(self):
        raise NotImplementedError

    # --------------------------------------------------------------------
    # Esecuzione asincrona (evita di bloccare la UI durante le chiamate di sistema)

    def _run_bg(self, work, on_done):
        def runner():
            try:
                result = work()
                error = None
            except Exception as e:
                result = None
                error = e
            self.after(0, lambda: on_done(result, error))

        threading.Thread(target=runner, daemon=True).start()

    # --------------------------------------------------------------------
    # Helper UI

    def _h1(self, text: str):
        tk.Label(
            self,
            text=text,
            bg=self.t["bg"],
            fg=self.t["fg"],
            font=(FONT, 18, "bold"),
        ).pack(anchor="w", padx=30, pady=(26, 3))

    def _sub(self, text: str):
        tk.Label(
            self, text=text, bg=self.t["bg"], fg=self.t["muted"], font=(FONT, 10)
        ).pack(anchor="w", padx=30, pady=(0, 14))

    def _card(self, parent=None, **kw) -> tk.Frame:
        return tk.Frame(parent or self, bg=self.t["card"], **kw)

    def _btn(self, parent, text: str, command, style="accent", **kw) -> tk.Button:
        t = self.t
        colors = {
            "accent": (t["accent"], t["accent_fg"]),
            "danger": (t["danger"], "#ffffff"),
            "secondary": (t["btn_2"], t["btn_2_fg"]),
        }
        bg, fg = colors.get(style, colors["accent"])
        return tk.Button(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=(FONT, 10, "bold"),
            relief="flat",
            padx=16,
            pady=9,
            cursor="hand2",
            command=command,
            **kw,
        )
