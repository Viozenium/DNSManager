import json
import os
import platform
import shutil


def _config_dir() -> str:
    system = platform.system()
    if system == "Windows":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    elif system == "Darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    path = os.path.join(base, "DNSManager")
    os.makedirs(path, exist_ok=True)
    return path


CONFIG_FILE = os.path.join(_config_dir(), "config.json")

DEFAULT_DNS_LIST = [
    {"name": "Google", "primary": "8.8.8.8", "secondary": "8.8.4.4"},
    {"name": "Cloudflare", "primary": "1.1.1.1", "secondary": "1.0.0.1"},
    {"name": "OpenDNS", "primary": "208.67.222.222", "secondary": "208.67.220.220"},
    {"name": "Quad9", "primary": "9.9.9.9", "secondary": "149.112.112.112"},
    {"name": "AdGuard", "primary": "94.140.14.14", "secondary": "94.140.15.15"},
    {"name": "NextDNS", "primary": "45.90.28.0", "secondary": "45.90.30.0"},
    {"name": "Comodo Secure", "primary": "8.26.56.26", "secondary": "8.20.247.20"},
]

DEFAULT_CONFIG = {
    "theme": "dark",
    "dns_list": DEFAULT_DNS_LIST,
}


class ConfigManager:
    def __init__(self):
        self._data = self._load()

    # --------------------------------------------------------------------
    # I/O 

    def _load(self) -> dict:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                try:
                    shutil.copy(CONFIG_FILE, CONFIG_FILE + ".corrotto")
                except OSError:
                    pass
        return dict(DEFAULT_CONFIG)

    def save(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    # --------------------------------------------------------------------
    # Tema

    @property
    def theme(self) -> str:
        return self._data.get("theme", "dark")

    @theme.setter
    def theme(self, value: str):
        self._data["theme"] = value

    # --------------------------------------------------------------------
    # Lista DNS

    @property
    def dns_list(self) -> list:
        return self._data.setdefault("dns_list", [])

    def add_dns(self, entry: dict):
        self.dns_list.append(entry)
        self.save()

    def update_dns(self, idx: int, entry: dict):
        self.dns_list[idx] = entry
        self.save()

    def remove_dns(self, idx: int):
        self.dns_list.pop(idx)
        self.save()

    def reset_dns_list(self):
        self._data["dns_list"] = list(DEFAULT_DNS_LIST)
        self.save()
