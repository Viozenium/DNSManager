import platform
import re
import subprocess

OS = platform.system()

IP_RE = re.compile(r"\d{1,3}(?:\.\d{1,3}){3}")

# --------------------------------------------------------------------
# Validazione

def validate_ip(ip: str, allow_empty: bool = False) -> bool:
    if not ip:
        return allow_empty
    parts = ip.strip().split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(p) <= 255 for p in parts)
    except ValueError:
        return False

# --------------------------------------------------------------------
# Lettura DNS corrente

def get_current_dns() -> dict:
    """Restituisce {"primary": str, "secondary": str, "source": str}"""
    try:
        if OS == "Windows":
            return _current_windows()
        elif OS == "Linux":
            return _current_linux()
        elif OS == "Darwin":
            return _current_macos()
    except Exception as e:
        return {"primary": "—", "secondary": "—", "source": f"Errore: {e}"}
    return {"primary": "—", "secondary": "—", "source": "OS non supportato"}


def _current_windows() -> dict:
    r = subprocess.run(
        ["netsh", "interface", "ip", "show", "dns"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    servers = IP_RE.findall(r.stdout)
    return {
        "primary": servers[0] if len(servers) > 0 else "—",
        "secondary": servers[1] if len(servers) > 1 else "—",
        "source": "netsh interface ip show dns",
    }


def _current_linux() -> dict:
    try:
        with open("/etc/resolv.conf", "r") as f:
            lines = f.readlines()
        servers = [
            l.split()[1]
            for l in lines
            if l.strip().startswith("nameserver") and len(l.split()) >= 2
        ]
        return {
            "primary": servers[0] if len(servers) > 0 else "—",
            "secondary": servers[1] if len(servers) > 1 else "—",
            "source": "/etc/resolv.conf",
        }
    except FileNotFoundError:
        return {
            "primary": "—",
            "secondary": "—",
            "source": "/etc/resolv.conf non trovato",
        }


def _current_macos() -> dict:
    servers = []
    for svc in _mac_services():
        r = subprocess.run(
            ["networksetup", "-getdnsservers", svc],
            capture_output=True,
            text=True,
        )
        for line in r.stdout.splitlines():
            line = line.strip()
            if IP_RE.match(line):
                servers.append(line)
        if servers:
            break
    return {
        "primary": servers[0] if len(servers) > 0 else "—",
        "secondary": servers[1] if len(servers) > 1 else "—",
        "source": "networksetup -getdnsservers",
    }

# --------------------------------------------------------------------
# Applicazione DNS

def apply_dns(primary: str, secondary: str = ""):
    if OS == "Windows":
        _apply_windows(primary, secondary)
    elif OS == "Linux":
        _apply_linux(primary, secondary)
    elif OS == "Darwin":
        _apply_macos(primary, secondary)
    else:
        raise RuntimeError(f"Sistema non supportato: {OS}")


def restore_default():
    if OS == "Windows":
        for iface in _win_interfaces():
            subprocess.run(
                ["netsh", "interface", "ip", "set", "dns", iface, "dhcp"],
                check=True,
                capture_output=True,
            )
    elif OS == "Linux":
        with open("/etc/resolv.conf", "w") as f:
            f.write("# generato automaticamente\n")
    elif OS == "Darwin":
        for svc in _mac_services():
            subprocess.run(
                ["networksetup", "-setdnsservers", svc, "empty"], capture_output=True
            )
    else:
        raise RuntimeError(f"Sistema non supportato: {OS}")

# --------------------------------------------------------------------
# Helpers per OS

def _win_interfaces() -> list:
    r = subprocess.run(
        ["netsh", "interface", "show", "interface"], capture_output=True, text=True
    )
    ifaces = []
    for line in r.stdout.splitlines()[3:]:
        parts = line.split()
        if len(parts) >= 4 and parts[1] == "Connected":
            ifaces.append(" ".join(parts[3:]))
    return ifaces or ["Wi-Fi", "Ethernet"]


def _apply_windows(primary: str, secondary: str):
    for iface in _win_interfaces():
        subprocess.run(
            ["netsh", "interface", "ip", "set", "dns", iface, "static", primary],
            check=True,
            capture_output=True,
        )
        if secondary:
            subprocess.run(
                ["netsh", "interface", "ip", "add", "dns", iface, secondary, "index=2"],
                check=True,
                capture_output=True,
            )


def _apply_linux(primary: str, secondary: str):
    with open("/etc/resolv.conf", "w") as f:
        f.write(f"nameserver {primary}\n")
        if secondary:
            f.write(f"nameserver {secondary}\n")


def _mac_services() -> list:
    r = subprocess.run(
        ["networksetup", "-listallnetworkservices"], capture_output=True, text=True
    )
    return [
        l.strip()
        for l in r.stdout.splitlines()[1:]
        if l.strip() and not l.startswith("*")
    ]


def _apply_macos(primary: str, secondary: str):
    args = [primary] + ([secondary] if secondary else [])
    for svc in _mac_services():
        subprocess.run(
            ["networksetup", "-setdnsservers", svc] + args,
            check=True,
            capture_output=True,
        ).lstrip()
