# Shorts Generator
### An automated AI pipeline that writes, narrates, and renders short-form videos

I wanted to see how far I could push Python automation for content creation — turns out, pretty far. Feed it a prompt, walk away, come back to a stack of ready-to-upload Shorts.

Built with XTTS-v2, Whisper, FFmpeg, and too many hours staring at ffmpeg error logs.

---

## What it does

- **AI-generated scripts** — stories and narration written from scratch, no templates
- **Natural voice narration** — powered by XTTS-v2 for human-sounding speech
- **Auto-subtitles** — Whisper transcribes and burns in captions with frame-accurate timing
- **Cinematic backgrounds** — drops content over gameplay or ambient footage
- **Background music** — layers in copyright-free ambience at a sane volume
- **Vertical 1080×1920 output** — native format for TikTok and YouTube Shorts
- **Batch generation** — set a number, let it run, collect your videos

---

## Tech Stack

| Layer | |
|---|---|
| Language | Python |
| Content generation | Ollama + Qwen2.5 |
| Voice synthesis | Coqui TTS (XTTS-v2) |
| Speech-to-text | OpenAI Whisper |
| Video & audio | FFmpeg, MoviePy |
| Deep learning | PyTorch, Torchaudio |

---

## Getting it running

### Prerequisites

- Python 3.9+
- FFmpeg
- XTTS-v2

### 1. Clone and set up

```bash
git clone git@github.com:CosmoJelly/short-form-video-generator.git
cd short-form-video-generator
```

### 2. Create a virtual environment

**Linux / macOS**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows**
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## FFmpeg Setup

**Arch Linux**
```bash
sudo pacman -S ffmpeg
```

**Ubuntu / Debian**
```bash
sudo apt install ffmpeg
```

**Windows** — download from [ffmpeg.org](https://ffmpeg.org) and add to PATH.

---

## XTTS-v2 Model

The first run automatically downloads the model:

```
tts_models/multilingual/multi-dataset/xtts_v2
```

No manual setup needed — just make sure you have disk space and a stable connection.

---

## Configuration

Everything lives in `config.json`:

```json
{
  "output_dir": "output",
  "temp_dir": "temp",
  "background_video_dir": "assets/gameplay",
  "background_music_dir": "assets/music",
  "font_path": "assets/fonts/Arial.ttf",
  "sub_font_size": 60,
  "video_size": [1080, 1920],
  "fps": 30,
  "music_volume": 0.08,
  "tts_volume": 1.3,
  "batch_size": 3
}
```

To generate more videos per run, bump `batch_size`:

```json
"batch_size": 5
```

---

## Running

```bash
python main.py
```

Finished videos land in the `output/` folder.

---

## Project Structure

```
short-form-video-generator/
├── assets/
│   ├── gameplay/       
│   ├── music/           
│   └── fonts/
├── output/              
├── temp/               
├── config.json
├── main.py
├── render_video.py
├── generate_voice.py
├── generate_story.py
├── generate_subtitles.py
├── requirements.txt
└── README.md
```

---

## Where to get assets

### Background videos

Free, no-attribution sources that work well:

- [Pexels](https://www.pexels.com/videos/)
- [Pixabay](https://pixabay.com/videos/)
- [Mixkit](https://mixkit.co/free-stock-video/)
- [Coverr](https://coverr.co/)

### Background music

Keep it subtle — the default `music_volume` of `0.08` is already pretty low. Good sources:

- [Pixabay Music](https://pixabay.com/music/)
- [FreeSound](https://freesound.org/)
- [Mixkit](https://mixkit.co/free-stock-music/)

---

## 🎧 Built to this soundtrack

> *[apology letter](https://open.spotify.com/playlist/4lApVuz9dhv8byOxvOtPrS?si=942d9eeace7c4ea4)*

> *[concoction](https://open.spotify.com/playlist/4w0wwlKLRZOytO89vUpWJb?si=bced9d7c34834348)*

> *[on the hunt](https://open.spotify.com/playlist/4VFsVk6ScI5x2WeAjJLDoi?si=8e3e9bcb2e2d4cbc)*

> *[brainrot](https://open.spotify.com/playlist/69NJQCobg7NMEz3q05Jmur?si=0ac75f1241c748ed)*

> *[amogus](https://open.spotify.com/playlist/3x31JT5qo6yZSI2BKo0JLh?si=cdf409f83c4b4e61)*

---

## License

Do whatever you want with this. It was a personal experiment and it worked, so here it is.
