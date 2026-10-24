# Voiceover for the demo video

Adds a friendly Australian-English voice to `spotter-demo.mp4` using Google Cloud Text-to-Speech.
The words and timings are in `narration.json` (one line per scene of the 43.7 s video). The tool only touches the sound: the picture is copied.

## One-time setup (about 5 minutes)
1. Open <https://console.cloud.google.com/> and pick (or create) a project. Billing must be switched on for the project (the free monthly allowance covers this video many times over, so it costs nothing in practice).
2. **APIs & Services → Library →** search **Cloud Text-to-Speech API → Enable**.
3. **APIs & Services → Credentials → Create credentials → API key.** Click the key, under *API restrictions* choose **Restrict key → Cloud Text-to-Speech API**, Save.
4. Save it on your Mac, outside this repository:
   ```bash
   printf '%s' 'PASTE_THE_KEY_HERE' > ~/.spotter-tts-key && chmod 600 ~/.spotter-tts-key
   ```
   (or `export GOOGLE_TTS_API_KEY=...` for one session). Never commit the key.

## Choosing a voice
```bash
python3 tools/voiceover/voiceover.py --list       # voices Google offers for en-AU
python3 tools/voiceover/voiceover.py --samples    # writes a short sample of four voices to listen to
```
Try `--voice en-AU-Neural2-C` (default), `-A`, `-B`, `-D`, or an `en-AU-Chirp3-HD-*` voice if `--list` shows them (the most natural and lively).
`--rate 1.05` is the speaking speed (a little brisk and upbeat); `--pitch` nudges the tone (not used by Chirp voices).

## Making the video
```bash
python3 tools/voiceover/voiceover.py --check                       # renders each line and says whether it fits its scene; writes nothing
python3 tools/voiceover/voiceover.py --voice en-AU-Neural2-C       # writes the voiced spotter-demo.mp4
```
A line that is too long for its scene is sped up (never past 1.25×) and reported if it still does not fit; shorten the text in `narration.json` then.
The old sound track is replaced, not mixed. Loudness is levelled to -16 LUFS.

## Tests
```bash
python3 -m unittest discover -s tools/voiceover/tests
```
They run the whole tool against a fake Google server, so they need no key and no internet (but do need `ffmpeg`).
