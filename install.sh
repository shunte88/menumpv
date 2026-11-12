#!/bin/sh
# Installs whatever applies: Nautilus extension, Nemo action, Dolphin service menu.
set -e
cd "$(dirname "$0")"
install -Dm755 mpv-play-folder.py ~/.local/bin/mpv-play-folder

if command -v nautilus >/dev/null; then
    dpkg -s python3-nautilus >/dev/null 2>&1 || sudo apt install -y python3-nautilus
    install -Dm644 mpv-play-folder.py ~/.local/share/nautilus-python/extensions/mpv-play-folder.py
    nautilus -q || true
fi
command -v nemo >/dev/null && install -Dm644 mpv-play-folder.nemo_action ~/.local/share/nemo/actions/mpv-play-folder.nemo_action
command -v dolphin >/dev/null && install -Dm755 mpv-play-folder-dolphin.desktop ~/.local/share/kio/servicemenus/mpv-play-folder.desktop
echo "Installed. Reopen your file manager and right-click a music/video folder."
