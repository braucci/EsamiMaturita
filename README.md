# Esami di Stato · Costruzioni Aeronautiche

Microsito statico contenente la raccolta delle prove di Esame di Stato per la disciplina **A038 — Struttura, Costruzione, Sistemi e Impianti del Mezzo Aereo** (indirizzo ITCT, opzione Costruzioni Aeronautiche).

Per ogni sessione (ordinaria, suppletiva, straordinaria) sono riportati i quesiti della seconda parte con risposte tecniche argomentate, dimostrazioni, riferimenti normativi e formule rese in KaTeX.

## Struttura

```
.
├── index.html            # Indice delle prove
├── esami/                # Una pagina per sessione
│   ├── 2015.html
│   ├── 2016.html
│   ├── 2017.html
│   ├── 2018.html
│   ├── 2018-suppletiva.html
│   ├── 2019.html
│   ├── 2023.html
│   ├── 2023-straordinaria.html
│   ├── 2024.html
│   ├── 2025.html
│   ├── 2025-suppletiva.html
│   ├── 2025-straordinaria.html
│   └── esempio-mim-2015.html
├── assets/
│   ├── style.css         # Sistema editoriale, palette aero
│   └── script.js         # Scroll-spy della TOC
└── README.md
```

## Tecnologie

- **HTML/CSS** statico, nessuna build necessaria
- **KaTeX** (CDN jsDelivr) per la matematica
- **Google Fonts** — Fraunces (display) + IBM Plex Sans/Mono (body)
- Responsivo (mobile-first), tema chiaro/scuro automatico (`prefers-color-scheme`)

## Pubblicazione su GitHub Pages

1. Crea un repository (es. `EsamiMaturita`).
2. Carica i file mantenendo la struttura.
3. **Settings → Pages → Source → main / root**.
4. Il sito sarà disponibile su `https://<utente>.github.io/EsamiMaturita/`.

## Aggiornamenti annuali

Per aggiungere una nuova sessione:
1. Scrivi il sorgente LaTeX `cap_esameYYYY.tex` mantenendo la struttura `\quesito{...}{...}` e gli ambienti `teoriabox`, `risultatibox`, ecc.
2. Aggiungi una entry alla lista `EXAMS` in `convert.py`.
3. Esegui `python3 generate.py` per rigenerare il sito completo.

## Licenza

© Prof. Ing. Raucci Biagio — ITIS E. Majorana, Cassino. Materiale didattico distribuibile con attribuzione.

## Rigenerare il sito da LaTeX

Il microsito è generato automaticamente dai sorgenti LaTeX dei capitoli del fascicolo principale (`opuscoletto-esami.tex`). Gli script Python in `scripts/` fanno il lavoro:

```bash
cd scripts/
# Posiziona i file cap_*.tex nella stessa cartella di convert.py (o aggiusta i path)
python3 generate.py
```

Output: tutti i file HTML in `../` (radice del sito) + assets aggiornati.

## Aggiungere un nuovo esame

1. Scrivi il sorgente `cap_esameYYYY.tex` mantenendo le strutture custom (`\quesito{N}{...}`, ambienti `teoriabox`, `risultatibox`, ecc.).
2. Aggiungi una entry in `EXAMS` in `convert.py`:
   ```python
   {"slug": "YYYY", "year": YYYY, "type": "Ordinaria",
    "file": "cap_esameYYYY.tex",
    "subtitle": "Riassunto degli argomenti..."}
   ```
3. Lancia `python3 generate.py`. Il sito si aggiorna automaticamente.
