#!/bin/sh
# Installs whatever applies: Nautilus extension, Nemo action, Dolphin service menu.
set -e
cd "$(dirname "$0")"
command -v mpv >/dev/null || sudo apt install -y mpv
install -Dm755 mpv-play-folder.py ~/.local/bin/mpv-play-folder

# mpv profiles: own file, pulled in by one include line at the TOP of mpv.conf
# (anything after a [profile] header would land inside that profile).
conf=~/.config/mpv/mpv.conf
install -Dm644 mpv-play-folder.conf ~/.config/mpv/mpv-play-folder.conf
touch "$conf"
grep -q 'mpv-play-folder.conf' "$conf" || sed -i '1i include="~~/mpv-play-folder.conf"' "$conf"
[ -s "$conf" ] || echo 'include="~~/mpv-play-folder.conf"' > "$conf"

if command -v nautilus >/dev/null; then
    dpkg -s python3-nautilus >/dev/null 2>&1 || sudo apt install -y python3-nautilus
    install -Dm644 mpv-play-folder.py ~/.local/share/nautilus-python/extensions/mpv-play-folder.py
    if pgrep -xu "$(id -u)" nautilus >/dev/null; then nautilus -q || true; fi  # restart only if running
fi
command -v nemo >/dev/null && install -Dm644 mpv-play-folder.nemo_action ~/.local/share/nemo/actions/mpv-play-folder.nemo_action
command -v dolphin >/dev/null && install -Dm755 mpv-play-folder-dolphin.desktop ~/.local/share/kio/servicemenus/mpv-play-folder.desktop
echo "Installed. Reopen your file manager and right-click a music/video folder."
