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
| `.github/workflows/android.yml` | Builds the APK and AAB on every push to `main` and attaches them to a release named after the game's version label. |

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
