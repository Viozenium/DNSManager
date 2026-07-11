import tkinter as tk

from themes import THEMES
from config.manager import ConfigManager
from ui.sidebar import Sidebar
from ui.pages.apply import ApplyPage
from ui.info import show_info_window
from ui.pages.manage import ManagePage
from ui.pages.manual import ManualPage
from ui.pages.settings import SettingsPage

PAGE_MAP = {
    "apply": ApplyPage,
    "manage": ManagePage,
    "manual": ManualPage,
    "settings": SettingsPage,
}


class DNSManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cfg = ConfigManager()
        self.t = THEMES[self.cfg.theme]
        self._active_page = "apply"
        self._info_win = None

        self.title("DNS Manager")
        self.geometry("960x600")
        self.minsize(820, 520)
        self.configure(bg=self.t["sidebar"])

        self._sidebar = Sidebar(self, self.t, self._navigate, self._open_info)
        self._sidebar.pack(side="left", fill="y")

        self._content = tk.Frame(self, bg=self.t["bg"])
        self._content.pack(side="right", fill="both", expand=True)

        self._navigate("apply")

    # --------------------------------------------------------------------
    # Info

    def _open_info(self):
        if self._info_win and self._info_win.winfo_exists():
            self._info_win.lift()
            return
        self._info_win = show_info_window(self, self.t)

    # --------------------------------------------------------------------
    # Navigazione

    def _navigate(self, key: str):
        self._active_page = key
        self._sidebar.set_active(key)
        for w in self._content.winfo_children():
            w.destroy()
        page = PAGE_MAP[key](
            self._content, self.t, self.cfg, refresh_cb=self._on_refresh
        )
        page.pack(fill="both", expand=True)

    def _on_refresh(self, new_theme: str | None = None):
        if new_theme:
            if self._info_win and self._info_win.winfo_exists():
                self._info_win.grab_release()
                self._info_win.destroy()
            self._info_win = None

            self.t = THEMES[new_theme]
            self.configure(bg=self.t["sidebar"])
            self._sidebar.destroy()
            self._sidebar = Sidebar(self, self.t, self._navigate, self._open_info)
            self._sidebar.pack(side="left", fill="y")
            self._content.configure(bg=self.t["bg"])
        self._navigate(self._active_page)
