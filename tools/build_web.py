"""Copies the game (web/tetris.html) into the Android app's assets, with the fonts bundled so it runs offline.

Usage: python3 tools/build_web.py
The Android build runs this automatically (see .github/workflows/android.yml)."""
import re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = ROOT / 'web' / 'tetris.html'
out = ROOT / 'app' / 'src' / 'main' / 'assets' / 'www'
html = src.read_text(encoding='utf-8')

fonts_css = '<style>\n' + '\n'.join(
    f"@font-face{{font-family:'Pixelify Sans';font-style:normal;font-weight:{w};font-display:swap;"
    f"src:url(fonts/pixelify-sans-latin-{w}-normal.woff2) format('woff2')}}" for w in (400, 600, 700)) + '\n</style>'
html = re.sub(r'<link rel="preconnect" href="https://fonts\.g(oogleapis|static)\.com"[^>]*>\s*', '', html)
html, n = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Pixelify\+Sans[^"]*">', fonts_css, html)
if n != 1:
    raise SystemExit('Google Fonts link not found in web/tetris.html')

out.mkdir(parents=True, exist_ok=True)
(out / 'index.html').write_text(html, encoding='utf-8')
shutil.copytree(ROOT / 'web' / 'fonts', out / 'fonts', dirs_exist_ok=True)
ver = re.search(r'<span id="ver"[^>]*>v(\d+)</span>', html)
print('Web assets ready:', 'v' + ver.group(1) if ver else '(no version label)')
