# DNS Manager

## Italiano

Applicazione Python con interfaccia grafica per gestire i server DNS di sistema su Windows, Linux e macOS.
Permette di applicare DNS predefiniti da una lista configurabile, inserirne di manuali e ripristinare i valori automatici.

### Descrizione

L'applicazione utilizza una GUI realizzata con Tkinter per consentire all'utente di:
- Selezionare un server DNS da una lista personalizzabile e applicarlo al sistema con un click.
- Visualizzare i DNS attualmente attivi direttamente nell'interfaccia, con aggiornamento in tempo reale.
- Inserire manualmente indirizzi DNS primari e secondari, con suggerimenti rapidi cliccabili.
- Aggiungere, modificare o rimuovere voci dalla lista DNS tramite un'interfaccia dedicata, le modifiche vengono salvate automaticamente nel `config.json`.
- Ripristinare i DNS automatici (DHCP) con un singolo pulsante.
- Cambiare l'aspetto dell'app tra tre temi (Chiaro, Scuro, Viola) con effetto immediato.

Il modulo `dns/backend.py` gestisce tutta la logica di sistema (lettura e scrittura DNS) in modo separato dalla UI, con supporto nativo per `netsh` (Windows), `/etc/resolv.conf` (Linux) e `networksetup` (macOS).

### Funzionalità principali

- Applicazione DNS con un click dalla lista configurabile
- Visualizzazione dei DNS attivi in tempo reale
- Modifica manuale con validazione degli indirizzi IP
- Gestione completa della lista (aggiunta, modifica, rimozione, ripristino predefiniti)
- Salvataggio automatico su `config.json`
- Ripristino DNS automatici (DHCP)
- Tre temi grafici selezionabili a runtime (Chiaro / Scuro / Viola)
- Rilevamento corretto di Windows 11 tramite build number
- Nessuna dipendenza esterna, solo librerie standard Python

### Struttura del progetto

```
dns_manager/
├── main.py               # punto di ingresso
├── themes.py             # palette colori dei 3 temi
├── pyproject.toml        # metadati e tool config
├── config.json           # generato automaticamente al primo avvio
├── config/
│   └── manager.py        # lettura/scrittura config.json
├── dns/
│   └── backend.py        # logica di sistema (lettura e applicazione DNS)
└── ui/
    ├── app.py             # finestra principale e routing
    ├── sidebar.py         # componente navigazione laterale
    ├── dialogs.py         # finestra modale aggiunta / modifica DNS
    └── pages/
        ├── base.py        # classe base con helper UI condivisi
        ├── apply.py       # pagina selezione e applicazione DNS
        ├── manage.py      # pagina gestione lista DNS
        ├── manual.py      # pagina inserimento manuale
        └── settings.py    # pagina tema e informazioni
```

### Requisiti

1. Python >= 3.10
2. Privilegi di amministratore o root per applicare le modifiche DNS

#### Librerie necessarie

Nessuna libreria esterna richiesta.
Il progetto usa esclusivamente la libreria standard Python:
`tkinter`, `json`, `os`, `subprocess`, `platform`, `sys`, `re`

### Utilizzo

```bash
python main.py
sudo python main.py
```

### Note

- Su **Windows** le modifiche vengono applicate a tutte le interfacce di rete attive tramite `netsh`.
- Su **Linux** viene riscritto `/etc/resolv.conf`.
- Su **macOS** vengono aggiornati tutti i servizi di rete tramite `networksetup`.
- Il `config.json` viene creato automaticamente al primo avvio con una lista DNS predefinita. Può essere modificato anche manualmente.

---

## English

A Python GUI application for managing system DNS servers on Windows, Linux and macOS.
Apply DNS from a configurable list, enter custom addresses, or restore automatic settings, all without touching the code.

### Description

The application uses a Tkinter based GUI to let the user:
- Select a DNS server from a customizable list and apply it to the system in one click.
- View currently active DNS addresses directly in the interface, with real time refresh.
- Manually enter primary and secondary DNS addresses, with quick fill suggestions.
- Add, edit or remove entries from the DNS list, changes are saved automatically to `config.json`.
- Restore automatic DNS (DHCP) with a single button.
- Switch between three themes (Light, Dark, Violet) instantly, without restarting the app.

### Main features

- One-click DNS apply from a configurable list
- Real-time display of currently active DNS
- Manual input with IP address validation
- Full list management (add, edit, remove, reset to defaults)
- Automatic save to `config.json`
- DHCP restore
- Three runtime-switchable themes (Light / Dark / Violet)
- Correct Windows 11 detection via build number
- No external dependencies, standard library only

### Requirements

1. Python >= 3.10
2. Administrator or root privileges to apply DNS changes

#### Required libraries

No external libraries required.
Uses only Python's standard library:
`tkinter`, `json`, `os`, `subprocess`, `platform`, `sys`, `re`

### Usage

```bash
python main.py
sudo python main.py
```

---

## Changelog

### v1.0.0
- Prima release pubblica
- GUI completa con 4 sezioni: Applica DNS, Gestisci Lista, Modifica Manuale, Impostazioni
- Visualizzazione DNS attivi in tempo reale con pulsante di refresh
- Lista DNS configurabile salvata su `config.json`
- Tre temi grafici selezionabili a runtime (Chiaro / Scuro / Viola)
- Supporto multi-OS: Windows (`netsh`), Linux (`/etc/resolv.conf`), macOS (`networksetup`)
- Rilevamento corretto di Windows 11 tramite build number