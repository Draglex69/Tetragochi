# Tetragotchi

Tetris with a virtual pet: adopt a cat, play blocks to the beat of its own songs, feed and pet it, decorate its home, and play Party mode with up to four players.

Written, designed and vibecoded by Alexander Tea.

## Get the Android app

Open **Releases** (right side of this page) and download `Tetragotchi-vNN.apk` on your phone, then open it to install. Android will ask you to allow installing from your browser the first time.

The `.aab` file in the same release is for Google Play.

## How it's built

| Path | What it is |
|---|---|
| `web/tetris.html` | The whole game, one file. Edit this. |
| `web/fonts/` | Pixelify Sans (SIL Open Font License), bundled so the app works offline. |
| `tools/build_web.py` | Copies the game and fonts into the app. |
| `app/` | A small Android app that runs the game full screen and offline. It adds the back button, saving codes to Downloads, clipboard copy and paste, and opening save files. |
| `pwa/` | The web version: manifest, offline service worker, icons and store screenshots. |
| `.github/workflows/android.yml` | On every push to `main`: builds the APK, the AAB and the web version, attaches all three to a release named after the game's version label, and publishes the web version with GitHub Pages when Pages is turned on. |

To ship a new version: replace `web/tetris.html` with the new game (its `vNN` label sets the app version) and push. The release appears under **Releases** a few minutes later.

The app ID is `io.github.draglex69.tetragotchi`. It never changes once the app is on Google Play.

## Signing for Google Play

Without signing secrets, builds use a debug key, which is fine for installing on your own phones. For Google Play, add four repository secrets (Settings → Secrets and variables → Actions → New repository secret):

| Secret | Value |
|---|---|
| `TG_KEYSTORE_BASE64` | the keystore file, base64-encoded |
| `TG_STORE_PASSWORD` | the keystore password |
| `TG_KEY_ALIAS` | `tetragotchi` |
| `TG_KEY_PASSWORD` | the key password |

Keep a backup of the keystore and its password somewhere safe; every future Play update must be signed with it. Never commit it to this repository.

Note: an app signed with the debug key can't be updated in place by one signed with the upload key. Uninstall the debug build first; export your progress with Save / Load and load it back afterwards.

## Web version

Every build also makes `Tetragotchi-vNN-web.zip`: the same game as an installable web app that works offline. Two ways to put it online:

- **GitHub Pages:** Settings → Pages → Source: **GitHub Actions**, then Settings → Secrets and variables → Actions → **Variables** → New variable `PAGES_ENABLED` = `true`. The next push publishes it at your Pages address. For a private repository this needs a paid GitHub plan.
- **Cloudflare Pages:** Workers & Pages → Create → Pages → Upload assets, then drop in the files from the zip.
