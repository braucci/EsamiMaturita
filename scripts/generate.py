#!/usr/bin/env python3
"""
Genera l'intero sito statico:
- index.html (menu)
- esami/<slug>.html (una pagina per esame)
- assets/style.css, assets/script.js
- README.md
"""
import sys
sys.path.insert(0, '/home/claude')
from convert import EXAMS, parse_chapter
from pathlib import Path

OUT = Path('/home/claude/site')
OUT.mkdir(exist_ok=True)
(OUT / 'esami').mkdir(exist_ok=True)
(OUT / 'assets').mkdir(exist_ok=True)

# ----------------------------------------------------------------------
# 1. CSS — sistema editoriale-tecnico, palette aero raffinata
# ----------------------------------------------------------------------
CSS = r"""
/* =================================================================
   ESAMI · Costruzioni Aeronautiche
   Sistema editoriale-tecnico · palette aero
   ================================================================= */

@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,300..900,0..100&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400;1,500&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
  /* Palette: parchment + deep aero blue + warm rust */
  --paper: #f7f2e8;
  --paper-2: #efe9dc;        /* card background */
  --paper-3: #e6dfcf;        /* deeper accent surface */
  --ink: #1a1d24;            /* near-black with slight blue tint */
  --ink-2: #3a3f4a;
  --ink-3: #6c7180;
  --rule: #d4ccba;           /* hairline */
  --rule-soft: #e1dac8;
  --aero: #1d3557;           /* bluaero */
  --aero-2: #2c4a70;
  --rust: #a8412c;           /* rossoavv refined */
  --emerald: #2d6a4f;        /* verdeok refined */
  --gold: #a8884a;           /* understated brass */
  --amber: #c89438;
  --shadow-1: 0 1px 0 rgba(26,29,36,0.04), 0 4px 14px -4px rgba(26,29,36,0.08);
  --shadow-2: 0 2px 0 rgba(26,29,36,0.05), 0 12px 32px -8px rgba(26,29,36,0.16);

  /* Tipografia */
  --serif: 'Fraunces', 'EB Garamond', Georgia, serif;
  --sans: 'IBM Plex Sans', system-ui, -apple-system, sans-serif;
  --mono: 'IBM Plex Mono', 'JetBrains Mono', Consolas, monospace;

  /* Spacing scale */
  --s-1: 0.25rem;
  --s-2: 0.5rem;
  --s-3: 0.75rem;
  --s-4: 1rem;
  --s-5: 1.5rem;
  --s-6: 2rem;
  --s-7: 3rem;
  --s-8: 4.5rem;
  --s-9: 6rem;

  /* Misure */
  --measure: 68ch;
  --max-w: 1280px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --paper: #161a20;
    --paper-2: #1e232b;
    --paper-3: #262c36;
    --ink: #f0eadb;
    --ink-2: #c4bfb0;
    --ink-3: #8a8678;
    --rule: #2a3038;
    --rule-soft: #232830;
    --aero: #6fa0d8;
    --aero-2: #4a82bf;
    --rust: #d6633f;
    --emerald: #6abe92;
    --gold: #d4ad6a;
    --amber: #e8b35a;
    --shadow-1: 0 1px 0 rgba(0,0,0,0.3), 0 4px 14px -4px rgba(0,0,0,0.5);
    --shadow-2: 0 2px 0 rgba(0,0,0,0.4), 0 12px 32px -8px rgba(0,0,0,0.6);
  }
}

* { box-sizing: border-box; }

html {
  font-size: 16px;
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
}

body {
  margin: 0;
  font-family: var(--sans);
  font-feature-settings: 'ss01', 'cv11';
  font-size: 1rem;
  line-height: 1.6;
  color: var(--ink);
  background: var(--paper);
  background-image:
    radial-gradient(ellipse at top, rgba(168, 136, 74, 0.05), transparent 60%),
    radial-gradient(ellipse at bottom right, rgba(29, 53, 87, 0.04), transparent 60%);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* =====  Header globale  ===== */
.site-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: color-mix(in srgb, var(--paper) 92%, transparent);
  backdrop-filter: blur(12px) saturate(140%);
  -webkit-backdrop-filter: blur(12px) saturate(140%);
  border-bottom: 1px solid var(--rule);
}

.site-header-inner {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: var(--s-4) var(--s-5);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--s-4);
}

.brand {
  display: flex;
  align-items: baseline;
  gap: var(--s-3);
  text-decoration: none;
  color: var(--ink);
  font-family: var(--serif);
  font-weight: 500;
  font-size: 1.15rem;
  font-variation-settings: 'opsz' 144;
  letter-spacing: -0.01em;
}

.brand-mark {
  display: inline-flex;
  align-items: center;
  gap: 0.4em;
  color: var(--aero);
}

.brand-mark::before {
  content: '';
  display: inline-block;
  width: 1.6em;
  height: 1.6em;
  background: linear-gradient(135deg, var(--aero), var(--aero-2));
  -webkit-mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M2 16l9-1.5 4.5 5L17 19l-2-7 6-2.5L19 8l-7 2-3.5-6-1.5.5L9 11 2 13z' fill='black'/></svg>") no-repeat center/contain;
          mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M2 16l9-1.5 4.5 5L17 19l-2-7 6-2.5L19 8l-7 2-3.5-6-1.5.5L9 11 2 13z' fill='black'/></svg>") no-repeat center/contain;
}

.brand-sub {
  font-family: var(--sans);
  font-size: 0.78rem;
  font-weight: 400;
  color: var(--ink-3);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.site-nav {
  display: flex;
  align-items: center;
  gap: var(--s-5);
}

.site-nav a {
  color: var(--ink-2);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.15s;
}

.site-nav a:hover {
  color: var(--aero);
}

@media (max-width: 720px) {
  .site-header-inner { padding: var(--s-3) var(--s-4); }
  .brand-sub { display: none; }
  .site-nav { gap: var(--s-3); }
  .site-nav a { font-size: 0.85rem; }
}

/* =====  Container  ===== */
.container {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 var(--s-5);
}

@media (max-width: 720px) {
  .container { padding: 0 var(--s-4); }
}

/* =====  HOMEPAGE: hero  ===== */
.hero {
  padding: var(--s-9) 0 var(--s-7);
  border-bottom: 1px solid var(--rule);
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 30%;
  right: -10%;
  width: 50%;
  height: 200%;
  background: radial-gradient(ellipse, rgba(29, 53, 87, 0.08), transparent 65%);
  pointer-events: none;
  z-index: 0;
}

.hero-inner {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 var(--s-5);
  position: relative;
  z-index: 1;
}

.hero-eyebrow {
  font-family: var(--mono);
  font-size: 0.78rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--rust);
  margin-bottom: var(--s-5);
  display: flex;
  align-items: center;
  gap: var(--s-3);
}

.hero-eyebrow::before {
  content: '';
  width: 2.5rem;
  height: 1px;
  background: var(--rust);
}

.hero-title {
  font-family: var(--serif);
  font-weight: 350;
  font-size: clamp(2.4rem, 6.5vw, 5.5rem);
  line-height: 0.95;
  letter-spacing: -0.025em;
  color: var(--ink);
  margin: 0 0 var(--s-5);
  font-variation-settings: 'opsz' 144, 'SOFT' 30;
}

.hero-title em {
  font-style: italic;
  color: var(--aero);
  font-variation-settings: 'opsz' 144, 'SOFT' 60;
}

.hero-lede {
  font-family: var(--serif);
  font-size: clamp(1.05rem, 1.7vw, 1.35rem);
  line-height: 1.5;
  font-weight: 350;
  color: var(--ink-2);
  max-width: 60ch;
  margin: 0 0 var(--s-6);
  font-variation-settings: 'opsz' 24;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--s-6);
  padding-top: var(--s-5);
  border-top: 1px solid var(--rule);
  font-size: 0.85rem;
  color: var(--ink-3);
}

.hero-meta strong {
  color: var(--ink);
  font-family: var(--mono);
  font-weight: 500;
  letter-spacing: -0.02em;
  font-size: 0.95rem;
  display: block;
  margin-bottom: 0.25rem;
}

@media (max-width: 720px) {
  .hero { padding: var(--s-7) 0 var(--s-6); }
  .hero-meta { gap: var(--s-4); }
}


/* =====  HOMEPAGE: premessa didattica  ===== */
.purpose-section {
  padding: var(--s-8) 0 0;
}

.purpose-card {
  max-width: 920px;
  background: var(--paper-2);
  border: 1px solid var(--rule);
  border-left: 4px solid var(--aero);
  border-radius: 6px;
  padding: var(--s-5) var(--s-6);
  box-shadow: var(--shadow-soft);
}

.purpose-card p {
  font-family: var(--serif);
  font-size: 1.05rem;
  line-height: 1.65;
  color: var(--ink-2);
  margin: 0 0 var(--s-4);
  font-variation-settings: 'opsz' 24;
}

.purpose-card p:last-child { margin-bottom: 0; }

@media (max-width: 720px) {
  .purpose-card { padding: var(--s-4); }
}

/* =====  HOMEPAGE: indice esami  ===== */
.exams-section {
  padding: var(--s-8) 0;
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: var(--s-6);
  flex-wrap: wrap;
  gap: var(--s-3);
}

.section-title {
  font-family: var(--serif);
  font-weight: 400;
  font-size: clamp(1.5rem, 2.5vw, 2rem);
  margin: 0;
  letter-spacing: -0.01em;
  font-variation-settings: 'opsz' 96;
}

.section-title-sub {
  font-family: var(--mono);
  font-size: 0.78rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ink-3);
}

.exams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--s-4);
}

.exam-card {
  position: relative;
  background: var(--paper-2);
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: var(--s-5);
  text-decoration: none;
  color: var(--ink);
  display: flex;
  flex-direction: column;
  gap: var(--s-3);
  transition: transform 0.2s ease, border-color 0.2s, background 0.2s;
  overflow: hidden;
}

.exam-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--aero);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.exam-card:hover {
  transform: translateY(-2px);
  border-color: var(--aero);
  background: var(--paper);
  box-shadow: var(--shadow-1);
}

.exam-card:hover::before {
  transform: scaleX(1);
}

.exam-card.is-suppl::before { background: var(--gold); }
.exam-card.is-suppl:hover { border-color: var(--gold); }

.exam-card.is-straord::before { background: var(--rust); }
.exam-card.is-straord:hover { border-color: var(--rust); }

.exam-card.is-mim::before { background: var(--emerald); }
.exam-card.is-mim:hover { border-color: var(--emerald); }

.exam-year {
  font-family: var(--serif);
  font-size: 3rem;
  font-weight: 350;
  line-height: 0.9;
  letter-spacing: -0.04em;
  color: var(--aero);
  font-variation-settings: 'opsz' 144, 'SOFT' 50;
}

.is-suppl .exam-year { color: var(--gold); }
.is-straord .exam-year { color: var(--rust); }
.is-mim .exam-year { color: var(--emerald); }

.exam-type {
  font-family: var(--mono);
  font-size: 0.75rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ink-3);
}

.exam-subtitle {
  font-size: 0.92rem;
  color: var(--ink-2);
  line-height: 1.5;
  margin: 0;
}

.exam-arrow {
  margin-top: auto;
  font-family: var(--mono);
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  color: var(--ink-3);
  display: flex;
  align-items: center;
  gap: 0.4em;
  transition: color 0.2s, gap 0.2s;
}

.exam-card:hover .exam-arrow {
  color: var(--aero);
  gap: 0.7em;
}

.exam-arrow::after {
  content: '→';
  font-size: 1rem;
}

/* =====  PAGINA SINGOLA: layout  ===== */
.exam-page {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: var(--s-6);
  padding: var(--s-7) 0 var(--s-9);
}

@media (min-width: 980px) {
  .exam-page {
    grid-template-columns: minmax(0, 1fr) 18rem;
    gap: var(--s-7);
  }
}

.exam-header {
  border-bottom: 1px solid var(--rule);
  padding-bottom: var(--s-6);
  margin-bottom: var(--s-6);
}

.exam-back {
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
  font-family: var(--mono);
  font-size: 0.78rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--ink-3);
  text-decoration: none;
  margin-bottom: var(--s-5);
  transition: color 0.15s;
}

.exam-back:hover { color: var(--aero); }

.exam-back::before {
  content: '←';
  font-size: 1rem;
}

.exam-eyebrow {
  display: flex;
  align-items: center;
  gap: var(--s-3);
  font-family: var(--mono);
  font-size: 0.78rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--rust);
  margin-bottom: var(--s-3);
}

.exam-eyebrow span { color: var(--ink-3); }
.exam-eyebrow .dot { color: var(--rule); }

.exam-title {
  font-family: var(--serif);
  font-weight: 350;
  font-size: clamp(2rem, 4.5vw, 3.5rem);
  line-height: 1.05;
  letter-spacing: -0.025em;
  margin: 0 0 var(--s-3);
  font-variation-settings: 'opsz' 144, 'SOFT' 30;
}

.exam-deck {
  font-family: var(--serif);
  font-style: italic;
  font-size: 1.1rem;
  color: var(--ink-2);
  line-height: 1.5;
  font-weight: 350;
  font-variation-settings: 'opsz' 24, 'SOFT' 60;
  margin: 0;
}

/* =====  Sidebar TOC  ===== */
.exam-aside {
  position: relative;
}

@media (min-width: 980px) {
  .exam-aside-inner {
    position: sticky;
    top: 5rem;
    padding-left: var(--s-5);
    border-left: 1px solid var(--rule);
  }
}

.toc-label {
  font-family: var(--mono);
  font-size: 0.72rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--ink-3);
  margin-bottom: var(--s-3);
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.88rem;
}

.toc-list a {
  color: var(--ink-2);
  text-decoration: none;
  display: block;
  padding: 0.3em 0;
  border-bottom: 1px dotted transparent;
  transition: color 0.15s, border-color 0.15s;
  line-height: 1.4;
}

.toc-list a:hover {
  color: var(--aero);
  border-bottom-color: var(--aero);
}

.toc-list a.active {
  color: var(--aero);
  font-weight: 500;
}

.toc-num {
  font-family: var(--mono);
  font-size: 0.78em;
  color: var(--ink-3);
  margin-right: 0.5em;
}

@media (max-width: 979px) {
  .exam-aside-inner {
    background: var(--paper-2);
    border: 1px solid var(--rule);
    padding: var(--s-4);
    border-radius: 4px;
  }
  .toc-list { font-size: 0.92rem; }
}

/* =====  Article: tipografia di lettura  ===== */
.exam-article {
  max-width: var(--measure);
  font-size: 1.02rem;
  line-height: 1.7;
}

.exam-article > p {
  margin: 0 0 1.1em;
  hyphens: auto;
  -webkit-hyphens: auto;
  text-align: justify;
  text-justify: inter-word;
}

.exam-article p:first-of-type::first-letter {
  /* drop cap on first paragraph after header */
}

.exam-article h2 {
  font-family: var(--serif);
  font-weight: 400;
  font-size: clamp(1.4rem, 2.4vw, 1.8rem);
  letter-spacing: -0.015em;
  margin: 2.2em 0 0.6em;
  padding-bottom: 0.3em;
  border-bottom: 1px solid var(--rule);
  font-variation-settings: 'opsz' 96, 'SOFT' 30;
  scroll-margin-top: 5rem;
}

.exam-article h2::before {
  content: '§';
  color: var(--aero);
  font-style: italic;
  margin-right: 0.4em;
  font-weight: 350;
}

.exam-article h3 {
  font-family: var(--serif);
  font-weight: 500;
  font-size: 1.2rem;
  margin: 1.8em 0 0.5em;
  letter-spacing: -0.005em;
  font-variation-settings: 'opsz' 36;
  color: var(--aero);
  scroll-margin-top: 5rem;
}

.exam-article h4 {
  font-family: var(--sans);
  font-weight: 600;
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 1.5em 0 0.4em;
  color: var(--ink-2);
}

.exam-article .para-head {
  margin: 1.2em 0 0.3em;
}

.exam-article strong {
  font-weight: 600;
  color: var(--ink);
}

.exam-article em {
  font-style: italic;
}

.exam-article a {
  color: var(--aero);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
}

.exam-article ul,
.exam-article ol {
  padding-left: 1.4em;
  margin: 0 0 1.1em;
}

.exam-article ul li,
.exam-article ol li {
  margin-bottom: 0.4em;
}

.exam-article ul {
  list-style: none;
  padding-left: 0;
}

.exam-article ul li {
  position: relative;
  padding-left: 1.4em;
}

.exam-article ul li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.8em;
  width: 0.6em;
  height: 1px;
  background: var(--aero);
}

.exam-article ol {
  list-style: none;
  counter-reset: item;
  padding-left: 0;
}

.exam-article ol > li {
  counter-increment: item;
  position: relative;
  padding-left: 2.2em;
}

.exam-article ol > li::before {
  content: counter(item);
  position: absolute;
  left: 0;
  top: 0;
  font-family: var(--mono);
  font-weight: 500;
  font-size: 0.85em;
  color: var(--aero);
  background: var(--paper-2);
  width: 1.6em;
  height: 1.6em;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--rule);
  margin-top: 0.15em;
}

.exam-article dl {
  margin: 0 0 1.1em;
}

.exam-article dt {
  font-weight: 600;
  color: var(--aero);
  font-family: var(--sans);
  margin-top: 0.7em;
}

.exam-article dd {
  margin-left: 0;
  margin-bottom: 0.5em;
  padding-left: 1em;
  border-left: 2px solid var(--rule-soft);
}

.exam-article code {
  font-family: var(--mono);
  font-size: 0.92em;
  background: var(--paper-3);
  padding: 0.08em 0.35em;
  border-radius: 2px;
}

.exam-article u { text-decoration: none; border-bottom: 1px solid currentColor; }
.exam-article .sc { font-variant: small-caps; letter-spacing: 0.05em; }
.exam-article .sf { font-family: var(--sans); }
.exam-article .ref { color: var(--ink-3); font-family: var(--mono); font-size: 0.9em; }

/* =====  Quesito: il blocco distintivo  ===== */
.quesito {
  margin: var(--s-6) 0 var(--s-5);
  padding: var(--s-4) var(--s-5);
  background: linear-gradient(135deg, var(--paper-2) 0%, var(--paper-2) 60%, var(--paper-3) 100%);
  border-left: 4px solid var(--aero);
  border-radius: 0 4px 4px 0;
  display: flex;
  flex-direction: column;
  gap: var(--s-2);
  position: relative;
  overflow: hidden;
}

.quesito::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 8em;
  height: 8em;
  background: radial-gradient(circle at top right, rgba(29,53,87,0.06), transparent 70%);
  pointer-events: none;
}

.quesito-num {
  font-family: var(--mono);
  font-size: 0.78rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--aero);
  font-weight: 500;
}

.quesito-text {
  font-family: var(--serif);
  font-size: 1.15rem;
  line-height: 1.4;
  font-style: italic;
  color: var(--ink);
  font-weight: 350;
  font-variation-settings: 'opsz' 36, 'SOFT' 50;
}

/* =====  Callout boxes  ===== */
.callout {
  margin: var(--s-5) 0;
  padding: var(--s-4) var(--s-5);
  border-left: 3px solid var(--aero);
  background: color-mix(in srgb, var(--paper-2) 70%, transparent);
  border-radius: 0 4px 4px 0;
  position: relative;
}

.callout-label {
  display: inline-block;
  font-family: var(--mono);
  font-size: 0.7rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--aero);
  font-weight: 500;
  margin-bottom: var(--s-3);
  padding: 0.15em 0.6em;
  background: color-mix(in srgb, var(--aero) 12%, transparent);
  border-radius: 2px;
}

.callout-body > *:last-child { margin-bottom: 0; }
.callout-body > *:first-child { margin-top: 0; }

.box-teoria { border-left-color: var(--aero); }
.box-teoria .callout-label { color: var(--aero); background: color-mix(in srgb, var(--aero) 12%, transparent); }

.box-ipotesi { border-left-color: var(--gold); }
.box-ipotesi .callout-label { color: var(--gold); background: color-mix(in srgb, var(--gold) 14%, transparent); }

.box-risultati { border-left-color: var(--emerald); background: color-mix(in srgb, var(--emerald) 5%, var(--paper-2)); }
.box-risultati .callout-label { color: var(--emerald); background: color-mix(in srgb, var(--emerald) 14%, transparent); }

.box-avviso { border-left-color: var(--rust); background: color-mix(in srgb, var(--rust) 4%, var(--paper-2)); }
.box-avviso .callout-label { color: var(--rust); background: color-mix(in srgb, var(--rust) 12%, transparent); }
.box-avviso .callout-label::before { content: '⚠ '; }

.box-esempio { border-left-color: var(--amber); }
.box-esempio .callout-label { color: var(--amber); background: color-mix(in srgb, var(--amber) 14%, transparent); }

.box-fase { border-left-color: var(--ink-3); }
.box-fase .callout-label { color: var(--ink-2); background: color-mix(in srgb, var(--ink-3) 12%, transparent); }

/* =====  Figure & tabelle  ===== */
.block-figure,
.figure-placeholder {
  margin: var(--s-5) 0;
  padding: var(--s-5);
  background: var(--paper-2);
  border: 1px dashed var(--rule);
  border-radius: 4px;
  text-align: center;
  color: var(--ink-3);
  font-family: var(--mono);
  font-size: 0.85rem;
}

.block-figure figcaption {
  margin-top: var(--s-3);
  font-size: 0.85rem;
  color: var(--ink-3);
  font-style: italic;
  font-family: var(--serif);
  font-weight: 350;
}

.table-wrap {
  margin: var(--s-5) 0;
  overflow-x: auto;
  border: 1px solid var(--rule);
  border-radius: 4px;
}

.table-wrap table {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.92rem;
  font-family: var(--sans);
}

.table-wrap td {
  padding: 0.55em 0.9em;
  border-bottom: 1px solid var(--rule-soft);
  vertical-align: top;
}

.table-wrap tr:first-child td {
  font-weight: 600;
  color: var(--aero);
  background: color-mix(in srgb, var(--aero) 6%, var(--paper-2));
  border-bottom: 1px solid var(--rule);
}

.table-wrap tr:last-child td {
  border-bottom: none;
}

.table-wrap figcaption {
  padding: var(--s-3);
  font-size: 0.85rem;
  color: var(--ink-3);
  font-style: italic;
  font-family: var(--serif);
  border-top: 1px solid var(--rule-soft);
  background: var(--paper-2);
}

/* =====  Math (KaTeX)  ===== */
.exam-article .katex { font-size: 1.05em; }
.exam-article .katex-display {
  margin: 1.2em 0;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 0.5em 0;
}

/* =====  Footer  ===== */
.site-footer {
  border-top: 1px solid var(--rule);
  margin-top: var(--s-8);
  padding: var(--s-6) 0 var(--s-5);
  font-size: 0.85rem;
  color: var(--ink-3);
}

.site-footer-inner {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 var(--s-5);
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: var(--s-3);
}

.site-footer p { margin: 0; }
.site-footer .credit {
  font-family: var(--mono);
  font-size: 0.78rem;
  letter-spacing: 0.05em;
}

/* =====  Pagination tra esami  ===== */
.exam-pagination {
  margin: var(--s-8) 0 0;
  padding-top: var(--s-6);
  border-top: 1px solid var(--rule);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--s-4);
}

.exam-pagination a {
  display: flex;
  flex-direction: column;
  gap: 0.2em;
  padding: var(--s-4);
  background: var(--paper-2);
  border: 1px solid var(--rule);
  border-radius: 4px;
  text-decoration: none;
  color: var(--ink);
  transition: border-color 0.2s, transform 0.2s;
}

.exam-pagination a:hover {
  border-color: var(--aero);
  transform: translateY(-1px);
}

.exam-pagination .label {
  font-family: var(--mono);
  font-size: 0.75rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--ink-3);
}

.exam-pagination .next { text-align: right; align-items: flex-end; }

.exam-pagination .title {
  font-family: var(--serif);
  font-size: 1.1rem;
  font-weight: 400;
  font-variation-settings: 'opsz' 36;
}

.exam-pagination .placeholder {
  background: transparent;
  border: 1px dashed var(--rule);
  pointer-events: none;
  opacity: 0.4;
}

@media (max-width: 540px) {
  .exam-pagination { grid-template-columns: 1fr; }
}

/* =====  Tipografia di stampa  ===== */
@media print {
  .site-header, .site-footer, .exam-pagination, .exam-aside, .exam-back { display: none; }
  body { background: white; color: black; }
  .exam-article { max-width: 100%; }
  .quesito { break-inside: avoid; }
  .callout { break-inside: avoid; border-left-width: 2px; }
}

/* =====  Selection  ===== */
::selection {
  background: var(--aero);
  color: var(--paper);
}
"""

(OUT / 'assets' / 'style.css').write_text(CSS, encoding='utf-8')

# ----------------------------------------------------------------------
# 2. JS — costruzione dinamica della TOC + scroll spy
# ----------------------------------------------------------------------
JS = r"""
// Scroll spy per la sidebar TOC
(() => {
  const headings = document.querySelectorAll('.exam-article h2, .exam-article h3');
  const tocLinks = document.querySelectorAll('.toc-list a');
  if (!tocLinks.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        tocLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === '#' + id);
        });
      }
    });
  }, { rootMargin: '-80px 0px -70% 0px' });

  headings.forEach(h => observer.observe(h));
})();

// Smooth-scroll con offset header
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top, behavior: 'smooth' });
      history.replaceState(null, '', link.getAttribute('href'));
    }
  });
});
"""

(OUT / 'assets' / 'script.js').write_text(JS, encoding='utf-8')

# ----------------------------------------------------------------------
# 3. Conversione capitoli + raccolta TOC per ognuno
# ----------------------------------------------------------------------
import re

def add_section_ids(html):
    """Assegna id univoci a h2/h3 e ritorna lista TOC."""
    toc = []
    sec_counter = [0]
    sub_counter = [0]
    def slug(s):
        s = re.sub(r'<[^>]+>', '', s)
        s = re.sub(r'\$[^$]*\$', '', s)
        s = re.sub(r'[^\w\s-]', '', s, flags=re.UNICODE).strip().lower()
        s = re.sub(r'[\s-]+', '-', s)
        return s[:50]

    def repl_h2(m):
        sec_counter[0] += 1
        sub_counter[0] = 0
        title = m.group(1).strip()
        s = slug(title) or f'sez-{sec_counter[0]}'
        toc.append({'level': 2, 'id': s, 'title': title, 'num': str(sec_counter[0])})
        return f'<h2 id="{s}">{title}</h2>'

    def repl_h3(m):
        sub_counter[0] += 1
        title = m.group(1).strip()
        s = slug(title) or f'sub-{sec_counter[0]}-{sub_counter[0]}'
        toc.append({'level': 3, 'id': s, 'title': title,
                    'num': f'{sec_counter[0]}.{sub_counter[0]}'})
        return f'<h3 id="{s}">{title}</h3>'

    html = re.sub(r'<h2>([^<]+)</h2>', repl_h2, html)
    html = re.sub(r'<h3>([^<]+)</h3>', repl_h3, html)
    return html, toc



# ----------------------------------------------------------------------
# Figure tecniche aggiuntive e pulizia residui LaTeX nelle pagine HTML
# ----------------------------------------------------------------------
MISSING_FIGURE_MAP = {
    "2018-suppletiva": ["2018-suppletiva-fig-01.png", "2018-suppletiva-fig-02.png"],
    "2019": ["2019-fig-01.png"],
    "2023-straordinaria": ["2023-straordinaria-fig-01.png", "2023-straordinaria-fig-02.png"],
    "2024": ["2024-fig-01.png"],
}

def postprocess_html(slug, html):
    marker = '<div class="figure-placeholder">[Figura tecnica disponibile nella versione PDF]</div>'
    for idx, filename in enumerate(MISSING_FIGURE_MAP.get(slug, []), start=1):
        img = (f'<img class="technical-figure" src="../assets/figures/{filename}" '
               f'alt="Figura tecnica {idx} — {slug}" loading="lazy">')
        html = html.replace(marker, img, 1)

    html = html.replace('$\\SIrange{55}{80}{°}\\mathrm{C}$', '<span class="unit">55–80&nbsp;°C</span>')
    html = html.replace('\\textcolor{bluaero}{blu}', '<span class="color-word blue">blu</span>')
    html = html.replace('\\textcolor{rossoavv}{rosso}', '<span class="color-word red">rosso</span>')
    html = html.replace('\\textcolor{verdeok}{<strong>verde</strong>}', '<span class="color-word green"><strong>verde</strong></span>')
    html = html.replace('\\textcolor{gialloipot}{<strong>giallo</strong>}', '<span class="color-word yellow"><strong>giallo</strong></span>')
    html = html.replace('\\textcolor{rossoavv}{<strong>rossa</strong>}', '<span class="color-word red"><strong>rossa</strong></span>')
    html = html.replace('bar{x}_G', r'\\bar{x}_G').replace('bar{x}_N', r'\\bar{x}_N')
    return html

# Parsing di tutti i capitoli
for ex in EXAMS:
    text = (Path('/home/claude') / ex['file']).read_text(encoding='utf-8')
    title, html = parse_chapter(text)
    html, toc = add_section_ids(html)
    ex['title'] = title
    ex['html'] = postprocess_html(ex['slug'], html)
    ex['toc'] = toc

# ----------------------------------------------------------------------
# 4. Header e footer comuni
# ----------------------------------------------------------------------
def head(title, description, depth=0):
    rel = '../' * depth
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#1d3557">
<meta name="description" content="{description}">
<title>{title}</title>
<link rel="stylesheet" href="{rel}assets/style.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" integrity="sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" integrity="sha384-7zkQWkzuo3B5mTepMUcHkMB5jZaolc2xDwL6VFqjFALcbeS9Ggm/Yr2r3Dy4lfFg" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" integrity="sha384-43gviWU0YVjaDtb/GhzOouOXtZMP/7XUzwPTstBeZFe/+rCMvRwr4yROQP43s0Xk" crossorigin="anonymous" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}], throwOnError: false, macros: {{ '\\\\AR': '\\\\mathrm{{AR}}' }} }});"></script>
</head>
<body>
"""

def site_header(active='', depth=0):
    rel = '../' * depth
    nav_home = 'aria-current="page"' if active == 'home' else ''
    return f"""<header class="site-header">
<div class="site-header-inner">
<a href="{rel}index.html" class="brand">
<span class="brand-mark">Esami</span>
<span class="brand-sub">Costruzioni Aeronautiche · A038</span>
</a>
<nav class="site-nav">
<a href="{rel}index.html" {nav_home}>Indice</a>
<a href="https://github.com" rel="noopener">GitHub</a>
<a href="https://www.raucci.net" rel="noopener">Blog personale</a>
</nav>
</div>
</header>
"""

def site_footer(depth=0):
    return f"""<footer class="site-footer">
<div class="site-footer-inner">
<p>Prof. Ing. Raucci Biagio · ITIS E. Majorana, Cassino · A.S. 2025/26</p>
<p class="credit">Costruzioni Aeronautiche · Classe A038</p>
</div>
</footer>
<script src="{('../' * depth)}assets/script.js"></script>
</body>
</html>
"""

# ----------------------------------------------------------------------
# 5. INDEX.HTML — homepage
# ----------------------------------------------------------------------
def card_class(ex):
    t = ex['type'].lower()
    if 'suppletiva' in t: return 'is-suppl'
    if 'straordinaria' in t: return 'is-straord'
    if 'mim' in t.lower() or 'esempio' in t.lower(): return 'is-mim'
    return ''

# Raggruppa per anno per il display
years_sorted = sorted(set(ex['year'] for ex in EXAMS), reverse=True)

cards_html = []
# 1) ordinarie + suppletive + straordinarie cronologiche dall'ultima
sorted_exams = sorted(EXAMS, key=lambda e: (
    -e['year'],
    {'Ordinaria': 0, 'Suppletiva': 1, 'Straordinaria': 2, 'Esempio MIM': 3}.get(e['type'], 4)
))

for ex in sorted_exams:
    cls = card_class(ex)
    href = f"esami/{ex['slug']}.html"
    cards_html.append(f"""<a href="{href}" class="exam-card {cls}">
<span class="exam-type">{ex['type']}</span>
<span class="exam-year">{ex['year']}</span>
<p class="exam-subtitle">{ex['subtitle']}</p>
<span class="exam-arrow">Apri</span>
</a>""")

index_html = head(
    "Esami di Stato · Costruzioni Aeronautiche",
    "Raccolta delle prove d'esame di Stato per la disciplina A038 (Costruzioni Aeronautiche), con risposte argomentate ai quesiti della seconda parte."
) + site_header(active='home') + f"""
<section class="hero">
<div class="hero-inner">
<div class="hero-eyebrow">Disciplina A038 · Seconda Prova Scritta</div>
<h1 class="hero-title">Esami di Stato.<br><em>Costruzioni Aeronautiche.</em></h1>
<p class="hero-lede">Raccolta ragionata delle prove d'esame ministeriali per l'opzione Costruzioni Aeronautiche dell'indirizzo ITCT — Trasporti e Logistica. Per ciascuna sessione vengono forniti i quesiti della seconda parte e le relative risposte argomentate, complete di dimostrazioni, riferimenti normativi (CS-23/CS-25, FAR, EASA) ed esempi numerici.</p>
<div class="hero-meta">
<div><strong>{len(EXAMS)}</strong> Sessioni d'esame</div>
<div><strong>{sum(len(ex['toc']) for ex in EXAMS)}</strong> Sezioni tematiche</div>
<div><strong>10+</strong> Anni di tracce</div>
</div>
</div>
</section>

<section class="purpose-section container" id="premessa">
<div class="section-head">
<h2 class="section-title">Perché queste note</h2>
<span class="section-title-sub">Premessa didattica</span>
</div>
<div class="purpose-card">
<p>Questo lavoro raccoglie le risposte ai <em>quesiti teorici</em> proposti nelle seconde prove dell'Esame di Stato per l'indirizzo <em>Costruzioni Aeronautiche</em>. L'obiettivo è duplice: da un lato fornire allo studente uno strumento di rapida consultazione su argomenti che, pur essendo parte integrante del programma, sono spesso trattati in maniera sintetica nel corso ordinario delle lezioni; dall'altro abituarlo a un'esposizione tecnica rigorosa, conforme al lessico disciplinare richiesto in sede d'esame.</p>
<p>Ogni quesito è organizzato secondo un'architettura modulare: un <strong>inquadramento teorico</strong> che richiama definizioni e principi fisici fondamentali; uno <strong>svolgimento argomentato</strong>, con riferimenti alle esperienze pratiche quando pertinenti; una <strong>sintesi conclusiva</strong> con i concetti-chiave da non dimenticare.</p>
<p>I quesiti sono raggruppati per anno d'esame, in ordine cronologico. Nell'esposizione si è scelto di privilegiare la chiarezza concettuale rispetto all'esaustività enciclopedica: ogni risposta è stata pensata per essere svolta nei tempi e nei limiti spaziali della prova scritta.</p>
<p>Buon lavoro!</p>
<p class="purpose-signature"><em>Prof. Ing. Raucci Biagio</em></p>
</div>
</section>

<section class="exams-section container">
<div class="section-head">
<h2 class="section-title">Indice delle prove</h2>
<span class="section-title-sub">In ordine cronologico inverso</span>
</div>
<div class="exams-grid">
{chr(10).join(cards_html)}
</div>
</section>
""" + site_footer()

(OUT / 'index.html').write_text(index_html, encoding='utf-8')

# ----------------------------------------------------------------------
# 6. PAGINE SINGOLE PER OGNI ESAME
# ----------------------------------------------------------------------
ordered_for_nav = sorted(EXAMS, key=lambda e: (
    e['year'],
    {'Ordinaria': 0, 'Suppletiva': 1, 'Straordinaria': 2, 'Esempio MIM': 3}.get(e['type'], 4)
))

for i, ex in enumerate(ordered_for_nav):
    prev_ex = ordered_for_nav[i-1] if i > 0 else None
    next_ex = ordered_for_nav[i+1] if i < len(ordered_for_nav)-1 else None

    # TOC sidebar
    toc_items = []
    for entry in ex['toc']:
        if entry['level'] == 2:
            toc_items.append(
                f'<li><a href="#{entry["id"]}"><span class="toc-num">{entry["num"]}</span>{entry["title"]}</a></li>'
            )
    toc_html = f"""<aside class="exam-aside">
<div class="exam-aside-inner">
<div class="toc-label">In questa pagina</div>
<ul class="toc-list">{chr(10).join(toc_items)}</ul>
</div>
</aside>""" if toc_items else ''

    # Pagination
    def link_card(other, label):
        if not other:
            return f'<div class="placeholder"></div>'
        cls = 'next' if label == 'Successivo' else ''
        return f"""<a href="{other['slug']}.html" class="{cls}">
<span class="label">{label}</span>
<span class="title">{other['year']} {'· ' + other['type'] if other['type'] != 'Ordinaria' else ''}</span>
</a>"""

    pagination = f"""<nav class="exam-pagination">
{link_card(prev_ex, 'Precedente')}
{link_card(next_ex, 'Successivo')}
</nav>"""

    # Hash per CSS class
    type_class = card_class(ex)

    body = head(
        f"{ex['title']} · Esami Costruzioni Aeronautiche",
        ex['subtitle'],
        depth=1
    ) + site_header(depth=1) + f"""
<main class="container">
<div class="exam-page">
<article class="exam-article-wrap">
<header class="exam-header">
<a href="../index.html" class="exam-back">Tutte le prove</a>
<div class="exam-eyebrow"><span>{ex['year']}</span><span class="dot">·</span><span>{ex['type']}</span></div>
<h1 class="exam-title">{ex['title']}</h1>
<p class="exam-deck">{ex['subtitle']}</p>
</header>
<div class="exam-article">
{ex['html']}
</div>
{pagination}
</article>
{toc_html}
</div>
</main>
""" + site_footer(depth=1)

    (OUT / 'esami' / f"{ex['slug']}.html").write_text(body, encoding='utf-8')

# ----------------------------------------------------------------------
# 7. README.md
# ----------------------------------------------------------------------
readme = """# Esami di Stato · Costruzioni Aeronautiche

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
1. Scrivi il sorgente LaTeX `cap_esameYYYY.tex` mantenendo la struttura `\\quesito{...}{...}` e gli ambienti `teoriabox`, `risultatibox`, ecc.
2. Aggiungi una entry alla lista `EXAMS` in `convert.py`.
3. Esegui `python3 generate.py` per rigenerare il sito completo.

## Licenza

© Prof. Ing. Raucci Biagio — ITIS E. Majorana, Cassino. Materiale didattico distribuibile con attribuzione.
"""
(OUT / 'README.md').write_text(readme, encoding='utf-8')

# ----------------------------------------------------------------------
# 8. Stampa risultato
# ----------------------------------------------------------------------
print("\n=== Sito generato ===")
for p in sorted(OUT.rglob('*')):
    if p.is_file():
        rel = p.relative_to(OUT)
        size = p.stat().st_size
        print(f"  {str(rel):40s} {size:>8d} bytes")
