#!/usr/bin/env python3
"""Adds a spoken voiceover to the website demo video using Google Cloud Text-to-Speech.

  python3 tools/voiceover/voiceover.py --list                 which Australian English voices your key can use
  python3 tools/voiceover/voiceover.py --samples              short samples of several voices in tools/voiceover/samples/ to choose by ear
  python3 tools/voiceover/voiceover.py --voice en-AU-Neural2-C --check      renders the lines and checks each fits its scene, writes nothing to the video
  python3 tools/voiceover/voiceover.py --voice en-AU-Neural2-C              writes spotter-demo.mp4 with the voiceover (the picture is never changed)

The lines and when each starts/ends (seconds into the video) are in tools/voiceover/narration.json. Needs ffmpeg and an API key for the
"Cloud Text-to-Speech API": put it in the file ~/.spotter-tts-key (one line) or in GOOGLE_TTS_API_KEY. The key is never stored in this repository.
"""
import argparse, base64, json, os, subprocess, sys, tempfile, urllib.error, urllib.parse, urllib.request, wave

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
API = os.environ.get("TTS_API_URL", "https://texttospeech.googleapis.com/v1")
VIDEO = os.path.join(ROOT, "spotter-demo.mp4")
SAMPLE_VOICES = ["en-AU-Neural2-A", "en-AU-Neural2-C", "en-AU-Neural2-B", "en-AU-Neural2-D"]
MAX_RATE = 1.25   # faster than this sounds rushed: shorten the line instead
SAMPLE_RATE = 24000


class VoiceError(Exception):
    pass


def load_key():
    key = os.environ.get("GOOGLE_TTS_API_KEY")
    if not key:
        path = os.path.expanduser("~/.spotter-tts-key")
        if os.path.exists(path):
            key = open(path).read().strip()
    if not key:
        raise VoiceError("No Google Text-to-Speech key. Create one (see tools/voiceover/README.md), save it as ~/.spotter-tts-key and try again.")
    return key


def post(path, key, body=None):
    url = f"{API}/{path}" + ("&" if "?" in path else "?") + urllib.parse.urlencode({"key": key})
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method="POST" if body is not None else "GET",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:400]
        hint = " Is the Cloud Text-to-Speech API enabled, and billing switched on, for the project this key belongs to?" if e.code in (400, 403) else ""
        raise VoiceError(f"Google answered {e.code}: {detail}{hint}")


def list_voices(key):
    data = post("voices?languageCode=en-AU", key)
    return sorted(data.get("voices", []), key=lambda v: v["name"])


def synthesize(key, text, voice, rate, out_wav, pitch=0.0):
    """Renders one line to a mono WAV and returns its length in seconds."""
    audio_config = {"audioEncoding": "LINEAR16", "sampleRateHertz": SAMPLE_RATE, "speakingRate": round(rate, 3)}
    if "Chirp" not in voice:      # Chirp voices do not take a pitch setting
        audio_config["pitch"] = pitch
    data = post("text:synthesize", key, {"input": {"text": text}, "voice": {"languageCode": "en-AU", "name": voice}, "audioConfig": audio_config})
    with open(out_wav, "wb") as f:
        f.write(base64.b64decode(data["audioContent"]))
    with wave.open(out_wav) as w:
        return w.getnframes() / float(w.getframerate())


def render_lines(key, lines, voice, workdir, base_rate=1.05, pitch=1.0):
    """Renders every line, speeding a line up (never beyond MAX_RATE) until it fits its scene. Returns per-line results."""
    results = []
    for i, line in enumerate(lines):
        window = line["end"] - line["start"]
        rate = base_rate
        path = os.path.join(workdir, f"line{i}.wav")
        while True:
            dur = synthesize(key, line["text"], voice, rate, path, pitch)
            if dur <= window - 0.15 or rate >= MAX_RATE:
                break
            rate = min(MAX_RATE, rate * (dur / (window - 0.15)) * 1.02)
        results.append({"i": i, "path": path, "dur": dur, "window": window, "rate": rate, "fits": dur <= window, "text": line["text"]})
    return results


def mix(results, lines, total, out_wav):
    inputs, filters = [], []
    for r, l in zip(results, lines):
        inputs += ["-i", r["path"]]
        ms = int(l["start"] * 1000)
        filters.append(f"[{r['i']}:a]aresample=44100,adelay={ms}|{ms},apad=whole_dur={total}[a{r['i']}]")
    graph = ";".join(filters) + ";" + "".join(f"[a{r['i']}]" for r in results) + \
        f"amix=inputs={len(results)}:normalize=0,atrim=0:{total},loudnorm=I=-16:TP=-1.5:LRA=7[out]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[out]", "-ar", "44100", "-ac", "1", out_wav], check=True)


def video_length(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--voice", default="en-AU-Neural2-C")
    p.add_argument("--list", action="store_true")
    p.add_argument("--samples", action="store_true")
    p.add_argument("--check", action="store_true", help="render and check the timing, write nothing to the video")
    p.add_argument("--rate", type=float, default=1.05, help="speaking speed, 1.0 = normal; a little over 1 sounds more energetic")
    p.add_argument("--pitch", type=float, default=1.0, help="semitones; a little above 0 sounds brighter and friendlier")
    p.add_argument("--video", default=VIDEO)
    p.add_argument("--out", default=None, help="where to write the video (default: replaces --video)")
    args = p.parse_args(argv)
    key = load_key()
    lines = json.load(open(os.path.join(HERE, "narration.json")))

    if args.list:
        for v in list_voices(key):
            print(f"{v['name']:28} {v['ssmlGender']:8} {v.get('naturalSampleRateHertz', '')}")
        return 0
    if args.samples:
        out = os.path.join(HERE, "samples"); os.makedirs(out, exist_ok=True)
        for v in SAMPLE_VOICES:
            synthesize(key, lines[0]["text"], v, args.rate, os.path.join(out, v + ".wav"), args.pitch)
            print("wrote", os.path.join(out, v + ".wav"))
        print("Play them (open the folder) and pick one: --voice <name>")
        return 0

    with tempfile.TemporaryDirectory() as work:
        results = render_lines(key, lines, args.voice, work, args.rate, args.pitch)
        for r in results:
            print(f"line {r['i']}: {r['dur']:.2f}s in a {r['window']:.1f}s scene at speed {r['rate']:.2f}  {'ok' if r['fits'] else 'TOO LONG: shorten this line'}  | {r['text']}")
        if not all(r["fits"] for r in results):
            raise VoiceError("At least one line does not fit its scene. Shorten it in narration.json (faster than %.2fx sounds rushed)." % MAX_RATE)
        if args.check:
            print("All lines fit. Nothing written (--check).")
            return 0
        total = video_length(args.video)
        track = os.path.join(work, "voice.wav")
        mix(results, lines, total, track)
        target = args.out or args.video
        tmp_out = os.path.join(work, "out.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", args.video, "-i", track, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                        "-movflags", "+faststart", "-shortest", tmp_out], check=True)   # only the picture of the input is used: any old sound is dropped
        os.replace(tmp_out, target) if os.path.dirname(tmp_out) == os.path.dirname(target) else open(target, "wb").write(open(tmp_out, "rb").read())
        print(f"Wrote {target} ({total:.1f}s) with voice {args.voice}.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except VoiceError as e:
        print("Stopped: " + str(e), file=sys.stderr)
        sys.exit(1)
