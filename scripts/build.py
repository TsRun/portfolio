#!/usr/bin/env python3
"""Generate the deployable pages from the single source of truth.

    project/Portfolio.dc.html  --(verbatim copy)-->  project/index.html   (EN, canonical /)
    project/Portfolio.dc.html  --(FR head/props)-->  project/fr.html      (FR, canonical /fr)

Run after every edit to Portfolio.dc.html:  python3 scripts/build.py

fr.html is the same page with the runtime's defaultLang flipped to "fr" and the
static head (title, description, OG/Twitter, canonical, JSON-LD, noscript)
translated. Each substitution asserts it matched: if an edit to the source
breaks a pattern, the build fails instead of silently shipping English text
on /fr.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "project"
SOURCE = ROOT / "Portfolio.dc.html"

FR_TITLE = "Mathis Serrier — Développeur freelance à Toulouse"
FR_DESCRIPTION = (
    "Portfolio de Mathis Serrier — développeur freelance à Toulouse. "
    "Des échecs à la voix, un entraîneur de cubing à l'aveugle, une task queue "
    "pour agents de code IA. C/C++ à l'École 42, Python et TypeScript partout ailleurs."
)
FR_OG_DESCRIPTION = (
    "Développeur freelance à Toulouse. Je crée les outils qui me manquaient — "
    "des échecs à la voix, un entraîneur de cubing à l'aveugle, une task queue "
    "pour agents de code IA."
)
FR_IMAGE_ALT = "Mathis Serrier — je crée les outils qui me manquaient. Portfolio développeur, Toulouse."

FR_NOSCRIPT = """<noscript>
  <div style="max-width:720px;margin:0 auto;padding:60px 28px;font-family:Georgia,serif;background:#f0eee6;color:#22201b">
    <h1 style="font-weight:400">Mathis Serrier — développeur freelance à Toulouse</h1>
    <p>Je crée les outils qui me manquaient. C/C++ à l'École 42, Python et TypeScript partout ailleurs. Disponible pour des missions freelance — outils desktop, apps web, intégrations IA &amp; agents, en remote depuis Toulouse.</p>
    <ul>
      <li><strong>ChessVoice</strong> — les échecs entièrement à la voix : STT/TTS navigateur, parsing des coups hybride grammaire locale + LLM, sur chess.com et lichess.</li>
      <li><strong>Savana</strong> — un gestionnaire de comptes League of Legends desktop : switch en un clic par injection de session, stats ranked via l'API Riot. <a href="https://github.com/TsRun/Savana">Code</a></li>
      <li><strong>Fil de Fer</strong> — un renderer 3D wireframe en C : projection isométrique, zoom et rotation, tracé ligne à ligne avec MiniLibX. <a href="https://github.com/TsRun/Fil-de-Fers">Code</a></li>
      <li><strong>minishell</strong> — un petit Bash réécrit from scratch en C : parsing, pipes, signaux, builtins, zéro leak. <a href="https://github.com/TsRun/minishell">Code</a></li>
    </ul>
    <p>Ce portfolio est interactif et nécessite JavaScript. En attendant : <a href="https://github.com/TsRun">github.com/TsRun</a></p>
  </div>
</noscript>"""

# (pattern, replacement, expected match count)
FR_SUBSTITUTIONS = [
    (r'<html lang="en">', '<html lang="fr">', 1),
    (r"<title>[^<]*</title>", f"<title>{FR_TITLE}</title>", 1),
    (r'(<meta name="description" content=")[^"]*(">)', rf"\g<1>{FR_DESCRIPTION}\g<2>", 1),
    (r'(<link rel="canonical" href=")https://tsrun\.dev/(">)', r"\g<1>https://tsrun.dev/fr\g<2>", 1),
    (r'(<meta property="og:url" content=")https://tsrun\.dev/(">)', r"\g<1>https://tsrun.dev/fr\g<2>", 1),
    (r'(<meta property="og:title" content=")[^"]*(">)', rf"\g<1>{FR_TITLE}\g<2>", 1),
    (r'(<meta property="og:description" content=")[^"]*(">)', rf"\g<1>{FR_OG_DESCRIPTION}\g<2>", 1),
    (r'(<meta name="twitter:title" content=")[^"]*(">)', rf"\g<1>{FR_TITLE}\g<2>", 1),
    (r'(<meta name="twitter:description" content=")[^"]*(">)', rf"\g<1>{FR_OG_DESCRIPTION}\g<2>", 1),
    (r'(:image:alt" content=")[^"]*(">)', rf"\g<1>{FR_IMAGE_ALT}\g<2>", 2),
    (r'(content="https://tsrun\.dev/assets/og)\.jpg(")', r"\g<1>-fr.jpg\g<2>", 2),
    (r'(<meta property="og:locale" content=")en_US(">)', r"\g<1>fr_FR\g<2>", 1),
    (r'(<meta property="og:locale:alternate" content=")fr_FR(">)', r"\g<1>en_US\g<2>", 1),
    (r'("jobTitle": ")Freelance developer(")', r"\g<1>Développeur freelance\g<2>", 1),
    (r"<noscript>.*?</noscript>", FR_NOSCRIPT.replace("\\", "\\\\"), 1),
    (
        r"(&quot;defaultLang&quot;:\{[^}]*?&quot;default&quot;:&quot;)en(&quot;)",
        r"\g<1>fr\g<2>",
        1,
    ),
]


def main():
    source = SOURCE.read_text(encoding="utf-8")

    (ROOT / "index.html").write_text(source, encoding="utf-8")

    fr, errors = source, []
    for pattern, replacement, expected in FR_SUBSTITUTIONS:
        fr, count = re.subn(pattern, replacement, fr, flags=re.S)
        if count != expected:
            errors.append(f"  {count}/{expected} matches for: {pattern[:70]}")
    if errors:
        sys.exit("build failed — patterns out of sync with Portfolio.dc.html:\n" + "\n".join(errors))

    (ROOT / "fr.html").write_text(fr, encoding="utf-8")
    print("built: project/index.html, project/fr.html")


if __name__ == "__main__":
    main()
