import json
import os
import re

# from generate_script import generate_script
from generate_voice import generate_voice
from generate_subtitles import generate_subtitles
from render_video import render_video
# from fetch_reddit import fetch_post
from generate_story import generate_story

HORROR_WORDS = [
    "suddenly",
    "breathing",
]


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


def clean_tts_text(text):

    # remove ansi / garbage (important)
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)

    # fix split-word artifacts like "co cobblestones"
    text = re.sub(r'\b(\w{1,3})\s+\1(\w+)', r'\1\2', text)

    # fix duplicated prefixes like "Sud Suddenly"
    text = re.sub(r'\b([A-Za-z]{2,})\s+\1[a-z]+\b', r'\1', text)

    # fix repeated words (like "down down")
    text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)

    # remove weird duplicated punctuation spacing
    text = re.sub(r'\.\s*\.\s*\.', '...', text)

    # fix broken line issues
    text = text.replace("\n", " ")

    # collapse whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def add_horror_pauses(text):

    # --------------------------------------------------
    # CLEAN EXISTING BAD PAUSES
    # --------------------------------------------------

    text = text.replace("... ... ...", "...")
    text = text.replace(".. ..", "...")
    text = text.replace(". . .", "...")

    # --------------------------------------------------
    # MICRO PAUSES
    # --------------------------------------------------

    text = text.replace(",", ", ")

    # --------------------------------------------------
    # ADD TENSION BEFORE HORROR WORDS
    # --------------------------------------------------

    for word in HORROR_WORDS:
        text = text.replace(word, "... " + word)

    return text


def run_pipeline(video_count):

    config = load_config()

    os.makedirs(config["output_dir"], exist_ok=True)
    os.makedirs(config["temp_dir"], exist_ok=True)

    # --------------------------------------------------
    # GENERATE MULTIPLE VIDEOS
    # --------------------------------------------------

    for index in range(video_count):

        print(f"\n[INFO] Generating video {index + 1}/{video_count}")

        # --------------------------------------------------
        # 1.1 Fetch Reddit post
        # --------------------------------------------------

        # post = fetch_post()

        # --------------------------------------------------
        # 1.2 Create story
        # --------------------------------------------------

        script_data = generate_story()

        # --------------------------------------------------
        # 2.1 Generate script
        # --------------------------------------------------

        # script_data = generate_script(post)

        script_text = script_data["script"]

        # --------------------------------------------------
        # CLEAN SCRIPT
        # --------------------------------------------------

        script_text = clean_tts_text(script_text)

        # --------------------------------------------------
        # ADD DRAMATIC PACING
        # --------------------------------------------------

        script_text = add_horror_pauses(script_text)

        # --------------------------------------------------
        # SAVE RAW SCRIPT FOR DEBUGGING
        # --------------------------------------------------

        # os.makedirs("temp", exist_ok=True)

        # with open(
        #     f"temp/script_{index + 1}.txt",
        #     "w",
        #     encoding="utf-8"
        # ) as f:
        #     f.write(script_text)

        # --------------------------------------------------
        # GENERATE VOICE
        # --------------------------------------------------

        audio_path = os.path.join(
            config["temp_dir"],
            f"voice_{index + 1}.mp3"
        )

        generate_voice(script_text, audio_path)

        # --------------------------------------------------
        # GENERATE SUBTITLES
        # --------------------------------------------------

        subtitle_path = os.path.join(
            config["temp_dir"],
            f"subs_{index + 1}.srt"
        )

        generate_subtitles(audio_path, subtitle_path)

        # --------------------------------------------------
        # FINAL OUTPUT PATH
        # --------------------------------------------------

        safe_title = (
            script_data["title"][:40]
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        output_path = os.path.join(
            config["output_dir"],
            f"{index + 1}_{safe_title}.mp4"
        )

        # --------------------------------------------------
        # RENDER VIDEO
        #
        # render_video.py handles:
        # - background music
        # - music looping
        # - video looping
        # - audio mixing
        # - subtitles
        # --------------------------------------------------

        render_video(
            config,
            audio_path,
            subtitle_path,
            output_path
        )

        print("DONE:", output_path)


if __name__ == "__main__":

    config = load_config()

    # --------------------------------------------------
    # NUMBER OF VIDEOS TO GENERATE (FROM CONFIG)
    # --------------------------------------------------

    video_count = config.get("video_count", 1)

    run_pipeline(video_count=video_count)