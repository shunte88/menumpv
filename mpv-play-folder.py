#!/usr/bin/env python3
"""Right-click a folder -> play it in mpv with the "music" or "videos" profile.

Nautilus: loaded as an extension (dynamic "Play Music"/"Play Videos" item).
Nemo/Dolphin: their menu files run `mpv-play-folder DIR`.
Install: ./install.sh      Self-check: python3 mpv-play-folder.py
"""
import os
import sys
import subprocess
import threading

AUDIO = {".flac", ".mp3", ".ogg", ".oga", ".opus", ".m4a", ".aac", ".wav", ".wv",
         ".ape", ".alac", ".aiff", ".aif", ".dsf", ".dff", ".mka", ".wma", ".mpc"}
VIDEO = {".mkv", ".mp4", ".m4v", ".avi", ".mov", ".webm", ".wmv", ".mpg", ".mpeg",
         ".ts", ".m2ts", ".flv", ".ogv", ".3gp", ".vob"}


def classify(path, max_dirs=10, max_entries=300, enough=20, per_dir=3):
    """Return "videos", "music" or None by sampling media files.
    Runs on Nautilus' UI thread (often over NFS), so the work is capped: at most
    max_dirs directory listings, max_entries entries read per listing, stop at `enough` media files.
    Goes deep (stack, per_dir subfolders each) so Library/Artist/Album/CD1 is reached.
    ponytail: sampling - a huge folder whose first few subfolders hold no media shows no menu."""
    audio = video = 0
    queue = [path]
    for _ in range(max_dirs):
        if not queue or audio + video >= enough:
            break
        try:
            with os.scandir(queue.pop()) as it:
                subdirs = 0
                for n, e in enumerate(it):
                    if n >= max_entries or audio + video >= enough:
                        break
                    if e.is_dir(follow_symlinks=False):
                        if subdirs < per_dir:
                            queue.append(e.path)
                            subdirs += 1
                        continue
                    ext = os.path.splitext(e.name)[1].lower()
                    audio += ext in AUDIO
                    video += ext in VIDEO
        except OSError:
            continue
    if not (audio or video):
        return None
    return "videos" if video >= audio else "music"


_pending = {}  # path -> classify thread still running (e.g. stuck on a dead NFS server)
_done = {}     # path -> result that finished after the menu gave up waiting


def _run(path):
    _done[path] = classify(path)
    _pending.pop(path, None)


def classify_bg(path, timeout=0.25):
    """classify() off the UI thread; give up after `timeout` so Files never freezes.
    A late result is kept and shown on the next right-click. One thread per path, even if it never returns."""
    if path in _done:
        return _done.pop(path)
    t = _pending.get(path)
    if t is None:
        t = _pending[path] = threading.Thread(target=_run, args=(path,), daemon=True)
        t.start()
    t.join(timeout)
    return _done.pop(path, None)


def play(path, profile):
    subprocess.Popen(["mpv", f"--profile={profile}", "--", path],
                     start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__" and len(sys.argv) > 1:  # Nemo/Dolphin entry point
    for path in sys.argv[1:]:
        profile = classify(path)
        if profile:
            play(path, profile)
        else:
            subprocess.run(["notify-send", "-i", "mpv", "Play folder in mpv",
                            f"No audio or video found in {os.path.basename(path)}"])
elif __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        assert classify(d) is None
        os.makedirs(f"{d}/album/CD1")
        open(f"{d}/album/CD1/01.FLAC", "w").close()
        open(f"{d}/album/cover.jpg", "w").close()
        assert classify(f"{d}/album") == "music"
        open(f"{d}/album/movie.mkv", "w").close()
        assert classify(f"{d}/album") == "videos"  # tie -> videos
        assert classify_bg(f"{d}/album") == "videos"
    import time
    real, classify = classify, lambda p: time.sleep(1.0) or "music"  # simulate a slow NAS
    t0 = time.time()
    assert classify_bg("/slow") is None and time.time() - t0 < 0.4  # gave up, UI not blocked
    assert classify_bg("/slow") is None and len(_pending) == 1       # no second thread
    time.sleep(0.8)
    assert classify_bg("/slow") == "music" and not _done             # late result used once
    print("ok")
else:
    from gi.repository import GObject, Nautilus

    LABEL = {"music": "Play Music (mpv)", "videos": "Play Videos (mpv)"}

    class MpvPlayFolder(GObject.GObject, Nautilus.MenuProvider):
        def _item(self, name, path):
            profile = classify_bg(path)
            if not profile:
                return []
            item = Nautilus.MenuItem(name=f"MpvPlayFolder::{name}", label=LABEL[profile])
            item.connect("activate", lambda *_: play(path, profile))
            return [item]

        def get_file_items(self, files):
            if len(files) != 1 or not files[0].is_directory() or not files[0].get_location().get_path():
                return []
            return self._item("file", files[0].get_location().get_path())

        def get_background_items(self, folder):
            path = folder.get_location().get_path()
            return self._item("bg", path) if path else []
