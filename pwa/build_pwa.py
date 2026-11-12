"""Builds the installable Tetragotchi app (PWA) from the single-file game.

Usage:  python3 build_pwa.py path/to/tetris.html path/to/output-folder

It copies the game into index.html, swaps the Google Fonts link for the bundled
font files (so the app works offline), links the manifest and icons, and
registers the service worker. Icons, fonts, manifest and sw.js are copied from
the folder this script sits in.
"""
import json, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
src, out = Path(sys.argv[1]), Path(sys.argv[2])
html = src.read_text(encoding="utf-8")

ver = re.search(r'<span id="ver"[^>]*>(v\d+)</span>', html)
version = ver.group(1) if ver else "v0"

# 1. Fonts: bundled files instead of Google Fonts
fonts_css = "<style>\n" + "\n".join(
    f"@font-face{{font-family:'Pixelify Sans';font-style:normal;font-weight:{w};font-display:swap;"
    f"src:url(fonts/pixelify-sans-latin-{w}-normal.woff2) format('woff2')}}"
    for w in (400, 600, 700)) + "\n</style>"
html = re.sub(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*', "", html)
html = re.sub(r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*', "", html)
html, n = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Pixelify\+Sans[^"]*">', fonts_css, html)
assert n == 1 or "fonts/pixelify-sans-latin-400" in html, "Google Fonts link not found"
already_built = 'rel="manifest"' in html

# 2. Manifest, icons and the app-capable flags
head_links = (
    '<link rel="manifest" href="manifest.webmanifest">\n'
    '<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">\n'
    '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
    '<meta name="apple-mobile-web-app-title" content="Tetragotchi">\n')
if not already_built:
    html = html.replace('<meta name="mobile-web-app-capable" content="yes">',
                        '<meta name="mobile-web-app-capable" content="yes">\n' + head_links, 1)

# 3. Service worker: offline play and quick start-up
sw_reg = ("<script>if('serviceWorker' in navigator&&location.protocol!=='file:')"
          "addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}))</script>\n")
if "serviceWorker.register" not in html:
    html = html.replace("</body>", sw_reg + "</body>", 1)

out.mkdir(parents=True, exist_ok=True)
(out / "index.html").write_text(html, encoding="utf-8")
same = out.resolve() == HERE
if not same:
    for d in ("icons", "fonts", "screenshots"):
        if (HERE / d).exists():
            shutil.copytree(HERE / d, out / d, dirs_exist_ok=True)
    shutil.copy(HERE / "manifest.webmanifest", out / "manifest.webmanifest")
# Stamp the version into the service worker; a new name makes installed copies refresh
sw = re.sub(r"tetragotchi-(__VERSION__|v\d+)", "tetragotchi-" + version, (HERE / "sw.js").read_text(encoding="utf-8"))
(out / "sw.js").write_text(sw, encoding="utf-8")
print("Built", version, "into", out)
