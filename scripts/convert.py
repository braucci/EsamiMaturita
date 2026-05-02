#!/usr/bin/env python3
"""
Convertitore LaTeX → HTML per i capitoli dell'opuscoletto.
Preserva la matematica per KaTeX, traduce le environment custom in card HTML.
"""
import re
import os
import sys
from pathlib import Path

# ----------------------------------------------------------------------
# Mappa box LaTeX → classe CSS
# ----------------------------------------------------------------------
BOX_KINDS = {
    "teoriabox":     ("Teoria",            "box-teoria"),
    "ipotesibox":    ("Ipotesi e dati",    "box-ipotesi"),
    "datibox":       ("Dati",              "box-ipotesi"),
    "risultatibox":  ("Risultati",         "box-risultati"),
    "avvisobox":     ("Attenzione",        "box-avviso"),
    "esempiobox":    ("Esempio",           "box-esempio"),
    "fasebox":       ("Fase",              "box-fase"),
}

def protect_math(text):
    """Sostituisce i blocchi matematici con segnaposto, preservandoli per KaTeX."""
    placeholders = {}
    counter = [0]

    def store_str(s):
        idx = counter[0]
        counter[0] += 1
        key = f"@@MATH{idx}@@"
        placeholders[key] = s
        return key

    # equation environment → $$ ... $$
    def repl_equation(m):
        return store_str('$$' + m.group(1).strip() + '$$')
    text = re.sub(r'\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}', repl_equation, text, flags=re.DOTALL)

    def repl_align(m):
        return store_str('$$\\begin{aligned}' + m.group(1).strip() + '\\end{aligned}$$')
    text = re.sub(r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}', repl_align, text, flags=re.DOTALL)

    def repl_display(m):
        return store_str('$$' + m.group(1).strip() + '$$')
    text = re.sub(r'\\\[(.*?)\\\]', repl_display, text, flags=re.DOTALL)

    # $...$
    def repl_inline(m):
        return store_str('$' + m.group(1) + '$')
    text = re.sub(r'(?<!\\)\$(.+?)(?<!\\)\$', repl_inline, text)
    return text, placeholders

def restore_math(text, placeholders):
    for key, val in placeholders.items():
        text = text.replace(key, val)
    return text

def strip_latex_comments(text):
    """Rimuove i commenti LaTeX (% non escapato fino a fine riga)."""
    out = []
    for line in text.split('\n'):
        # trova % non preceduto da \
        i = 0
        while i < len(line):
            if line[i] == '%' and (i == 0 or line[i-1] != '\\'):
                line = line[:i]
                break
            i += 1
        out.append(line)
    return '\n'.join(out)

def parse_box(env_name, body):
    """Genera HTML per un box da una environment LaTeX."""
    title, css_class = BOX_KINDS.get(env_name, (env_name.title(), "box-default"))
    body_html = convert_inline(body.strip())
    return f'<aside class="callout {css_class}"><div class="callout-label">{title}</div><div class="callout-body">{body_html}</div></aside>\n'

def parse_quesito(num, text):
    """Render del macro quesito{N}{testo}."""
    return f'<div class="quesito"><span class="quesito-num">Quesito {num}</span><span class="quesito-text">{convert_inline(text)}</span></div>\n'

def convert_inline(text):
    """Converte tutte le sostituzioni inline (no environment, no display math)."""
    # Comandi da eliminare puramente
    text = re.sub(r'\\label\{[^}]*\}', '', text)
    text = re.sub(r'\\index\{[^}]*\}', '', text)
    text = re.sub(r'\\noindent\b\s*', '', text)
    text = re.sub(r'\\smallskip\b', '', text)
    text = re.sub(r'\\medskip\b', '', text)
    text = re.sub(r'\\bigskip\b', '<br>', text)
    text = re.sub(r'\\par\b', '', text)
    text = re.sub(r'\\centering\b', '', text)
    text = re.sub(r'\\small\b', '', text)
    text = re.sub(r'\\footnotesize\b', '', text)
    text = re.sub(r'\\scriptsize\b', '', text)
    text = re.sub(r'\\large\b', '', text)
    text = re.sub(r'\\Large\b', '', text)
    text = re.sub(r'\\sffamily\b', '', text)
    text = re.sub(r'\\renewcommand\{[^}]*\}\{[^}]*\}', '', text)

    # Riferimenti incrociati
    text = re.sub(r'\\ref\{([^}]+)\}', r'<span class="ref">§\1</span>', text)
    text = re.sub(r'\\eqref\{([^}]+)\}', r'<span class="ref">(\1)</span>', text)

    # Comandi tipografici
    text = re.sub(r'\\textbf\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', r'<strong>\1</strong>', text)
    text = re.sub(r'\\textit\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', r'<em>\1</em>', text)
    text = re.sub(r'\\emph\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', r'<em>\1</em>', text)
    text = re.sub(r'\\textsc\{([^{}]*)\}', r'<span class="sc">\1</span>', text)
    text = re.sub(r'\\textsf\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', r'<span class="sf">\1</span>', text)
    text = re.sub(r'\\texttt\{([^{}]*)\}', r'<code>\1</code>', text)
    text = re.sub(r'\\underline\{([^{}]*)\}', r'<u>\1</u>', text)
    text = re.sub(r'\\quad\b', '&ensp;', text)
    text = re.sub(r'\\qquad\b', '&emsp;', text)
    text = re.sub(r'\\,', '\u2009', text)
    text = re.sub(r'\\;', '\u2009', text)
    text = re.sub(r'\\:', '\u2009', text)

    # \texorpdfstring{tex}{pdf} → tex
    text = re.sub(r'\\texorpdfstring\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{[^{}]*\}', r'\1', text)

    # Caratteri speciali
    text = text.replace('\\&', '&amp;')
    text = text.replace('---', '—')
    text = text.replace('--', '–')
    text = text.replace("``", '"').replace("''", '"')
    text = text.replace("`", "'")
    text = re.sub(r'\\%', '%', text)
    text = re.sub(r'\\#', '#', text)
    text = re.sub(r'\\\$', '$', text)
    text = re.sub(r'\\_', '_', text)

    # paragraph (manuale)
    text = re.sub(r'\\paragraph\{([^{}]+)\}', r'<p class="para-head"><strong>\1</strong></p>', text)

    return text

def convert_lists(text):
    """Converte itemize/enumerate/description in <ul>/<ol>/<dl>."""
    def replace_env(env, tag, items_tag):
        pattern = re.compile(rf'\\begin\{{{env}\}}(?:\[[^\]]*\])?(.*?)\\end\{{{env}\}}', re.DOTALL)
        def repl(m):
            body = m.group(1)
            # rimuove eventuali leftmargin etc
            items_html = []
            # split by \item
            parts = re.split(r'\\item\b', body)
            for p in parts[1:]:
                p = p.strip()
                if p:
                    items_html.append(f'<{items_tag}>{p}</{items_tag}>')
            return f'<{tag}>{"".join(items_html)}</{tag}>'
        return pattern.sub(repl, text)

    text = replace_env('itemize', 'ul', 'li')
    text = replace_env('enumerate', 'ol', 'li')

    # description: \item[term] body
    pattern_desc = re.compile(r'\\begin\{description\}(?:\[[^\]]*\])?(.*?)\\end\{description\}', re.DOTALL)
    def repl_desc(m):
        body = m.group(1)
        items_html = []
        # match \item[...] until next \item or end
        for match in re.finditer(r'\\item\s*\[([^\]]*)\]\s*(.*?)(?=\\item|\Z)', body, re.DOTALL):
            term = match.group(1).strip()
            descr = match.group(2).strip()
            items_html.append(f'<dt>{term}</dt><dd>{descr}</dd>')
        return f'<dl>{"".join(items_html)}</dl>'
    text = pattern_desc.sub(repl_desc, text)
    return text

def remove_unsupported(text):
    """Rimuove environment che non possiamo rendere bene in HTML statico."""
    # tikzpicture
    text = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',
                  '<div class="figure-placeholder">[Figura tecnica disponibile nella versione PDF]</div>',
                  text, flags=re.DOTALL)
    # figure environments
    text = re.sub(r'\\begin\{figure\}(?:\[[^\]]*\])?(.*?)\\end\{figure\}',
                  lambda m: f'<figure class="block-figure">{m.group(1)}</figure>',
                  text, flags=re.DOTALL)
    # \caption{...} dentro figure
    text = re.sub(r'\\caption\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',
                  r'<figcaption>\1</figcaption>', text)
    # tables
    text = re.sub(r'\\begin\{table\}(?:\[[^\]]*\])?(.*?)\\end\{table\}',
                  lambda m: f'<div class="table-wrap">{m.group(1)}</div>',
                  text, flags=re.DOTALL)
    # tabular → table HTML
    def tabular_to_html(m):
        spec = m.group(1)
        body = m.group(2)
        # rimuovi \toprule \midrule \bottomrule
        body = re.sub(r'\\toprule|\\midrule|\\bottomrule|\\hline', '', body)
        rows_html = []
        for row in body.split('\\\\'):
            row = row.strip()
            if not row:
                continue
            cells = [c.strip() for c in row.split('&')]
            cells_html = ''.join(f'<td>{c}</td>' for c in cells)
            rows_html.append(f'<tr>{cells_html}</tr>')
        return f'<table>{chr(10).join(rows_html)}</table>'
    text = re.sub(r'\\begin\{tabular\}\{([^}]*)\}(.*?)\\end\{tabular\}',
                  tabular_to_html, text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{tabularx\}\{[^}]*\}\{([^}]*)\}(.*?)\\end\{tabularx\}',
                  tabular_to_html, text, flags=re.DOTALL)
    # axis/pgfplots → placeholder
    text = re.sub(r'\\begin\{axis\}.*?\\end\{axis\}',
                  '<div class="figure-placeholder">[Grafico disponibile nella versione PDF]</div>',
                  text, flags=re.DOTALL)
    # boxed{...} → mathstyle (lascialo a KaTeX, già supportato)
    return text

def parse_chapter(text):
    """Pipeline completa di conversione di un capitolo."""
    # 1. rimuovi commenti
    text = strip_latex_comments(text)
    # 2. proteggi la matematica
    text, math_ph = protect_math(text)
    # 3. estrai titolo capitolo
    chap_match = re.search(r'\\chapter(?:\*?)\{([^}]+)\}', text)
    chap_title = chap_match.group(1).strip() if chap_match else "Esame"
    chap_title = chap_title.replace('---', '—').replace('--', '–')
    text = re.sub(r'\\chapter(?:\*?)\{[^}]+\}', '', text)
    text = re.sub(r'\\chaptermark\{[^}]+\}', '', text)
    text = re.sub(r'\\label\{cap:[^}]+\}', '', text)

    # 4. environment box → HTML
    for env in BOX_KINDS:
        pattern = re.compile(rf'\\begin\{{{env}\}}(.*?)\\end\{{{env}\}}', re.DOTALL)
        text = pattern.sub(lambda m: parse_box(env, m.group(1)), text)

    # 5. quesito{N}{testo}
    text = re.sub(r'\\quesito\{([^}]+)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',
                  lambda m: parse_quesito(m.group(1), m.group(2)), text)

    # 6. liste
    text = convert_lists(text)

    # 7. environment non supportate → placeholder
    text = remove_unsupported(text)

    # 8. \section → <h2>, \subsection → <h3>
    text = re.sub(r'\\section\{([^}]+)\}', r'<h2>\1</h2>', text)
    text = re.sub(r'\\subsection\{([^}]+)\}', r'<h3>\1</h3>', text)
    text = re.sub(r'\\subsubsection\{([^}]+)\}', r'<h4>\1</h4>', text)

    # 9. paragraph
    # già convertito in inline

    # 10. inline conversions (su tutto il testo)
    text = convert_inline(text)

    # 11. paragrafi: doppio newline → <p>, single newline → spazio
    blocks = re.split(r'\n\s*\n', text)
    html_blocks = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        # se inizia con < (tag HTML), non avvolgere
        if re.match(r'^\s*<(h2|h3|h4|aside|div|p|figure|ul|ol|dl|table|figcaption)', b):
            html_blocks.append(b)
        else:
            # singoli newline → spazi
            b = re.sub(r'\n', ' ', b)
            b = re.sub(r'  +', ' ', b)
            html_blocks.append(f'<p>{b}</p>')
    body_html = '\n\n'.join(html_blocks)

    # 12. ripristina la matematica
    body_html = restore_math(body_html, math_ph)

    return chap_title, body_html


# ----------------------------------------------------------------------
# Mappa file → metadati
# ----------------------------------------------------------------------
EXAMS = [
    {"slug": "2015",            "year": 2015, "type": "Ordinaria", "file": "cap_esame2015.tex",
     "subtitle": "Velivolo da turismo · Sistema di pressurizzazione · Materiali compositi"},
    {"slug": "2016",            "year": 2016, "type": "Ordinaria", "file": "cap_esame2016.tex",
     "subtitle": "Aliante · Materiali per costruzioni aeronautiche · Strumentazione"},
    {"slug": "2017",            "year": 2017, "type": "Ordinaria", "file": "cap_esame2017.tex",
     "subtitle": "Velivolo bimotore · Impianto idraulico · Prove di laboratorio"},
    {"slug": "2018",            "year": 2018, "type": "Ordinaria", "file": "cap_esame2018ord.tex",
     "subtitle": "Comandi di volo · Quota di tangenza · Formazione di ghiaccio"},
    {"slug": "2018-suppletiva", "year": 2018, "type": "Suppletiva", "file": "cap_esame2018suppl.tex",
     "subtitle": "Autonomia oraria · Pressurizzazione · Stabilità longitudinale · Volo librato"},
    {"slug": "2019",            "year": 2019, "type": "Ordinaria", "file": "cap_esame2019ord.tex",
     "subtitle": "Inviluppo di volo · Impianto combustibile · Sollecitazione longherone · CND magnetoscopico"},
    {"slug": "2023",            "year": 2023, "type": "Ordinaria", "file": "cap_esame2023.tex",
     "subtitle": "Antincendio · Motorizzazione e serbatoio · Prove a terra · Corrosione"},
    {"slug": "2023-straordinaria", "year": 2023, "type": "Straordinaria", "file": "cap_esame2023straord.tex",
     "subtitle": "Compositi · Motore a reazione · Decollo · Certificazione aeromobili"},
    {"slug": "2024",            "year": 2024, "type": "Ordinaria", "file": "cap_esame2024.tex",
     "subtitle": "UAV elettrico · Quota di tangenza · Strumentazione di bordo · Sicurezza in cabina"},
    {"slug": "2025",            "year": 2025, "type": "Ordinaria", "file": "cap_esame2025.tex",
     "subtitle": "Esame di Stato 2025"},
    {"slug": "2025-suppletiva", "year": 2025, "type": "Suppletiva", "file": "cap_esame2025suppl.tex",
     "subtitle": "Esame di Stato 2025 — sessione suppletiva"},
    {"slug": "2025-straordinaria", "year": 2025, "type": "Straordinaria", "file": "cap_esame2025straord.tex",
     "subtitle": "Esame di Stato 2025 — sessione straordinaria"},
    {"slug": "esempio-mim-2015", "year": 2015, "type": "Esempio MIM", "file": "cap_esempioMIM.tex",
     "subtitle": "Traccia ministeriale di esempio (MIM)"},
]

if __name__ == '__main__':
    out_dir = Path('/home/claude/site')
    out_dir.mkdir(exist_ok=True)
    (out_dir / 'esami').mkdir(exist_ok=True)

    for ex in EXAMS:
        path = Path('/home/claude') / ex['file']
        if not path.exists():
            print(f"⚠ Missing: {path}")
            continue
        text = path.read_text(encoding='utf-8')
        title, html = parse_chapter(text)
        ex['title'] = title
        ex['html'] = html
        print(f"✓ {ex['slug']:25s} → {len(html):>6d} chars  ({title})")

    print(f"\nTotale: {len(EXAMS)} capitoli convertiti")
