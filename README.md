# Play Folder in mpv, For Dummies

You right-click a folder. It plays. That's the whole trick.

Got a folder full of FLACs? Right-click, pick **Play Music**, and your album starts rolling. Got a folder of videos? Right-click, pick **Play Videos**, and mpv goes full screen. No dragging files, no playlists, no fuss.

## What You Need

- Ubuntu (this was built on 26.04)
- **mpv**, the media player. Don't have it? Run `sudo apt install mpv`
- One of these file managers:
  - **Files** (the Ubuntu default, also called Nautilus)
  - **Nemo**
  - **Dolphin**

## Install It (2 Minutes, Tops)

1. Open a terminal in this folder.
2. Run:

   ```
   ./install.sh
   ```

3. If it asks for your password, type it. It's installing one small helper package for Files.
4. Close your file manager and open it again.

Done. Seriously.

## Use It

**In Files:** right-click any folder that has music or videos inside. You'll see **Play Music (mpv)** or **Play Videos (mpv)**, depending on what's in there. No media? No menu item. It stays out of your way.

**In Nemo or Dolphin:** right-click any folder and choose **Play folder in mpv**. It figures out music vs. video for you. If the folder has nothing playable, you'll get a polite little pop-up saying so.

**Bonus:** in Files, right-click the empty space *inside* a folder to play that folder.

## The Two Moods (a.k.a. Profiles)

The settings live at the bottom of `~/.config/mpv/mpv.conf`.

| Mood | What it does |
|------|--------------|
| **music** | Shows the album art, plays tracks back to back with no gaps, and leaves your audio untouched. Quit halfway through an album? It picks up right where you left off. Hit the last track? It loops back to the top. |
| **videos** | Goes full screen, uses your graphics card, and remembers where you stopped. |

Want to tweak? Open that file and fiddle with the `[music]` or `[videos]` section. Some fan favorites:

- Like shuffle? Add `shuffle=yes` under `[music]`.
- Hate full screen? Change `fullscreen=yes` to `fullscreen=no` under `[videos]`.
- Want albums to stop at the end? Change `loop-playlist=yes` to `loop-playlist=no` under `[music]`.
- Prefer a fresh start every time? Change `save-position-on-quit=yes` to `save-position-on-quit=no` under `[music]`.

## Uh Oh, Something's Off

**No menu item in Files.** Close Files completely with `nautilus -q`, then open it again.

**The menu item is missing on one giant folder.** It only peeks at a sample of what's inside, so it never freezes your computer. Right-click one level deeper and you'll get it.

**My network drive is slow.** Files won't freeze. The menu may skip the Play item the first time. Right-click again and it'll be there.

**My album started in the middle of a song.** That's the resume feature doing its job. Press `Enter` to skip ahead, or `<` to go back a track.

**A big library takes a moment to start.** That's mpv reading thousands of songs. Grab a coffee. It'll get there.

## Remove It

Changed your mind? Delete these and restart your file manager:

```
rm ~/.local/bin/mpv-play-folder
rm ~/.local/share/nautilus-python/extensions/mpv-play-folder.py
rm ~/.local/share/nemo/actions/mpv-play-folder.nemo_action
rm ~/.local/share/kio/servicemenus/mpv-play-folder.desktop
```

Your mpv settings stay put, and a backup of the original is saved as `~/.config/mpv/mpv.conf.bak-2026-11-12`.
