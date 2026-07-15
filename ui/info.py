import tkinter as tk
import webbrowser

AUTHOR = "Mizu"
VERSION = "1.0.4"
GITHUB_LABEL = "Viozenium"
GITHUB_URL = "https://github.com/Viozenium"

FONT = "Segoe UI"


def _darken(hex_color, factor=0.85):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"#{max(0,int(r*factor)):02x}{max(0,int(g*factor)):02x}{max(0,int(b*factor)):02x}"

def show_info_window(parent, t: dict):
    bg = t["bg"]
    fg = t["fg"]
    divider = t["border"]
    highlight = t["accent"]
    highlight_fg = t["accent_fg"]
    muted = t["muted"]
    win = tk.Toplevel(parent)
    win.title("Info")
    win.geometry("360x260")
    win.resizable(False, False)
    win.configure(bg=bg)
    win.transient(parent)
    win.grab_set()

    def close():
        win.grab_release()
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", close)

    tk.Frame(win, bg=highlight, height=3).pack(fill="x")

    hdr = tk.Frame(win, bg=bg, padx=28, pady=18)
    hdr.pack(fill="x")
    tk.Label(hdr, text="◈  ABOUT", font=(FONT, 16, "bold"), bg=bg, fg=highlight).pack(
        anchor="w"
    )

    tk.Frame(win, bg=divider, height=1).pack(fill="x", padx=28)

    body = tk.Frame(win, bg=bg, padx=28, pady=20)
    body.pack(fill="both", expand=True)

    def row(label, value):
        f = tk.Frame(body, bg=bg)
        f.pack(fill="x", pady=5)
        tk.Label(
            f, text=label, font=(FONT, 10), bg=bg, fg=muted, width=10, anchor="w"
        ).pack(side="left")
        tk.Label(f, text=value, font=(FONT, 10, "bold"), bg=bg, fg=fg, anchor="w").pack(
            side="left"
        )

    row("Author", AUTHOR)
    row("Version", VERSION)

    f = tk.Frame(body, bg=bg)
    f.pack(fill="x", pady=5)
    tk.Label(
        f, text="GitHub", font=(FONT, 10), bg=bg, fg=muted, width=10, anchor="w"
    ).pack(side="left")
    link = tk.Label(
        f,
        text=GITHUB_LABEL,
        font=(FONT, 10, "bold"),
        bg=bg,
        fg=highlight,
        cursor="hand2",
        anchor="w",
    )
    link.pack(side="left")
    link.bind("<Button-1>", lambda e: webbrowser.open(GITHUB_URL))
    link.bind("<Enter>", lambda e: link.config(fg=fg))
    link.bind("<Leave>", lambda e: link.config(fg=highlight))

    tk.Frame(win, bg=divider, height=1).pack(fill="x")
    tk.Button(
        win,
        text="Chiudi",
        font=(FONT, 10, "bold"),
        bg=highlight,
        fg=highlight_fg,
        activebackground=_darken(highlight),
        activeforeground=highlight_fg,
        relief="flat",
        bd=0,
        padx=20,
        pady=8,
        command=close,
    ).pack(pady=12)

    return win
