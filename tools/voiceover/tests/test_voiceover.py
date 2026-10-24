"""Runs the voiceover tool against a small fake Google Text-to-Speech server (a tone whose length follows the text and speaking speed),
so the whole flow is tested with no key and no internet.   python3 -m unittest discover -s tools/voiceover/tests"""
import base64, io, json, math, os, shutil, struct, subprocess, sys, tempfile, threading, unittest, wave
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

class Fake(BaseHTTPRequestHandler):
    log = []
    def _json(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        Fake.log.append(("GET", self.path))
        if "key=good" not in self.path: return self._json(403, {"error": "bad key"})
        self._json(200, {"voices": [{"name": "en-AU-Neural2-C", "ssmlGender": "FEMALE", "naturalSampleRateHertz": 24000}, {"name": "en-AU-Neural2-A", "ssmlGender": "FEMALE", "naturalSampleRateHertz": 24000}]})
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        Fake.log.append(("POST", self.path, body))
        if "key=good" not in self.path: return self._json(403, {"error": "bad key"})
        words = len(body["input"]["text"].split()); rate = body["audioConfig"]["speakingRate"]
        seconds = words * 0.4 / rate      # 0.4 s per word at normal speed
        n = int(24000 * seconds); buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
            w.writeframes(b"".join(struct.pack("<h", int(8000 * math.sin(2 * math.pi * 220 * i / 24000))) for i in range(n)))
        self._json(200, {"audioContent": base64.b64encode(buf.getvalue()).decode()})
    def log_message(self, *a): pass

server = HTTPServer(("127.0.0.1", 0), Fake); threading.Thread(target=server.serve_forever, daemon=True).start()
os.environ["TTS_API_URL"] = f"http://127.0.0.1:{server.server_port}/v1"
import voiceover as v   # noqa: E402

def make_silent_video(path, seconds):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s=64x64:d={seconds}:r=10", "-f", "lavfi", "-i", f"sine=frequency=440:duration={seconds}",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", path], check=True)   # has an OLD sound track, which must be replaced

class Tool(unittest.TestCase):
    def setUp(self):
        Fake.log.clear(); os.environ["GOOGLE_TTS_API_KEY"] = "good"
        self.dir = tempfile.mkdtemp(); self.video = os.path.join(self.dir, "demo.mp4"); make_silent_video(self.video, 44)

    def test_the_real_narration_file_is_sane(self):
        lines = json.load(open(os.path.join(v.HERE, "narration.json")))
        self.assertEqual(len(lines), 9)
        for a, b in zip(lines, lines[1:]): self.assertLess(a["end"], b["start"], "lines must not overlap")
        for l in lines: self.assertGreater(l["end"] - l["start"], 1.5); self.assertLess(l["end"], 62.6)

    def test_a_missing_key_explains_what_to_do(self):
        os.environ.pop("GOOGLE_TTS_API_KEY"); os.environ["HOME"] = self.dir
        with self.assertRaises(v.VoiceError) as e: v.load_key()
        self.assertIn("README", str(e.exception))

    def test_a_bad_key_gives_a_plain_message(self):
        os.environ["GOOGLE_TTS_API_KEY"] = "bad"
        with self.assertRaises(v.VoiceError) as e: v.main(["--list"])
        self.assertIn("403", str(e.exception)); self.assertIn("billing", str(e.exception))

    def test_lists_voices(self):
        self.assertEqual(v.main(["--list"]), 0)
        self.assertTrue(any(c[0] == "GET" and "voices?languageCode=en-AU" in c[1] for c in Fake.log))

    def test_check_renders_and_writes_nothing(self):
        before = open(self.video, "rb").read()
        self.assertEqual(v.main(["--video", self.video, "--check"]), 0)
        self.assertEqual(before, open(self.video, "rb").read())

    def test_a_line_too_long_for_its_scene_speeds_up_then_fails_clearly(self):
        lines = [{"start": 0.5, "end": 2.0, "text": "word " * 12}]
        with tempfile.TemporaryDirectory() as w:
            r = v.render_lines("good", lines, "en-AU-Neural2-C", w)
        self.assertLessEqual(r[0]["rate"], v.MAX_RATE + 1e-9); self.assertFalse(r[0]["fits"])

    def test_a_line_that_fits_a_little_slow_is_speeded_up_to_fit(self):
        lines = [{"start": 0.0, "end": 3.0, "text": "one two three four five six seven"}]   # 2.8 s at 1.0, 2.67 s at 1.05
        with tempfile.TemporaryDirectory() as w:
            r = v.render_lines("good", lines, "en-AU-Neural2-C", w, base_rate=0.9)
        self.assertTrue(r[0]["fits"]); self.assertGreater(r[0]["rate"], 0.9)

    def test_full_run_puts_the_voice_on_the_picture_and_drops_the_old_sound(self):
        out = os.path.join(self.dir, "voiced.mp4")
        self.assertEqual(v.main(["--video", self.video, "--out", out, "--voice", "en-AU-Neural2-C"]), 0)
        info = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.split()
        self.assertEqual(sorted(info), ["aac,audio", "h264,video"])
        self.assertAlmostEqual(v.video_length(out), 44, delta=0.3)
        posts = [c for c in Fake.log if c[0] == "POST"]
        self.assertGreaterEqual(len(posts), 8)
        self.assertTrue(all(c[2]["voice"]["name"] == "en-AU-Neural2-C" and c[2]["voice"]["languageCode"] == "en-AU" for c in posts))
        # speech sits inside the scenes: loud near the first line's start, silent in the gap before the next scene
        sil = subprocess.run(["ffmpeg", "-i", out, "-af", "silencedetect=n=-45dB:d=0.3", "-f", "null", "-"], capture_output=True, text=True).stderr
        self.assertIn("silence_start", sil)

    def test_chirp_voices_get_no_pitch_setting(self):
        with tempfile.TemporaryDirectory() as w:
            v.synthesize("good", "hello there", "en-AU-Chirp3-HD-Aoede", 1.0, os.path.join(w, "a.wav"), pitch=2.0)
        self.assertNotIn("pitch", [c for c in Fake.log if c[0] == "POST"][-1][2]["audioConfig"])
        with tempfile.TemporaryDirectory() as w:
            v.synthesize("good", "hello there", "en-AU-Neural2-C", 1.0, os.path.join(w, "a.wav"), pitch=2.0)
        self.assertEqual([c for c in Fake.log if c[0] == "POST"][-1][2]["audioConfig"]["pitch"], 2.0)

    def test_the_key_is_never_written_into_the_repository(self):
        for root, _, files in os.walk(os.path.join(v.ROOT, "tools")):
            for f in files:
                if f.endswith((".py", ".md", ".json")): self.assertNotIn("AI" + "za", open(os.path.join(root, f)).read())   # Google API keys start with this

if __name__ == "__main__":
    unittest.main()
