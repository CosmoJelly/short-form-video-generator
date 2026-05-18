import os
import random
import subprocess


def get_random_background(bg_dir):

    if not os.path.exists(bg_dir):
        return None

    files = [
        f for f in os.listdir(bg_dir)
        if f.lower().endswith((".mp4", ".mov", ".mkv", ".webm"))
    ]

    if not files:
        return None

    return os.path.join(bg_dir, random.choice(files))


def get_random_music(music_dir):

    if not os.path.exists(music_dir):
        return None

    files = [
        f for f in os.listdir(music_dir)
        if f.lower().endswith((".mp3", ".wav", ".ogg"))
    ]

    if not files:
        return None

    return os.path.join(music_dir, random.choice(files))


def render_video(config, audio_path, subtitle_path, output_path):

    bg_video = get_random_background(config["background_video_dir"])

    bg_music = get_random_music(config["background_music_dir"])

    temp_video = "temp/video_no_subs.mp4"
    mixed_audio = "temp/final_audio.mp3"

    # --------------------------------------------------
    # MIX NARRATION + BACKGROUND MUSIC
    # --------------------------------------------------

    if bg_music:

        print(f"[INFO] Using background music: {bg_music}")

        subprocess.call([
            "ffmpeg", "-y",

            # narration audio
            "-i", audio_path,

            # loop music infinitely
            "-stream_loop", "-1",
            "-i", bg_music,

            # --------------------------------------------------
            # AUDIO MIXING
            #
            # [0:a] = narration
            # [1:a] = background music
            # --------------------------------------------------

            "-filter_complex",
            (
                #f"[0:a]volume={config['tts_volume']}[a0];"
                f"[1:a]volume={config['music_volume']}[a1];"
                "[a0][a1]amix=inputs=2:duration=first:dropout_transition=2"
            ),

            "-shortest",

            "-c:a", "libmp3lame",

            mixed_audio
        ])

    else:

        mixed_audio = audio_path

    # --------------------------------------------------
    # CASE 1: Background gameplay exists
    # --------------------------------------------------

    if bg_video:

        print(f"[INFO] Using background video: {bg_video}")

        subprocess.call([
            "ffmpeg", "-y",

            "-stream_loop", "-1",
            "-i", bg_video,
            "-i", mixed_audio,

            # --------------------------------------------------
            # FIX: force audio-driven timeline
            # --------------------------------------------------

            "-map", "0:v:0",
            "-map", "1:a:0",

            "-shortest",

            # --------------------------------------------------
            # VIDEO FILTERS
            # --------------------------------------------------

            "-vf",
            (
                "scale=1080:1920:"
                "force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "eq=brightness=-0.06:contrast=1.15,"
                "gblur=sigma=3"
            ),

            "-c:v", "libx264",
            "-preset", "veryfast",
            "-c:a", "aac",

            temp_video
        ])

    # --------------------------------------------------
    # CASE 2: No gameplay exists
    # Create black vertical background
    # --------------------------------------------------

    else:

        print("[INFO] No background video found. Using black screen.")

        subprocess.call([
            "ffmpeg", "-y",

            "-f", "lavfi",
            "-i", "color=c=black:s=1080x1920:r=30",

            "-i", mixed_audio,

            "-map", "0:v:0",
            "-map", "1:a:0",

            "-shortest",

            "-c:v", "libx264",
            "-preset", "veryfast",
            "-c:a", "aac",

            temp_video
        ])

    # --------------------------------------------------
    # BURN SUBTITLES
    # --------------------------------------------------

    font_path = config.get("font_path")

    # --------------------------------------------------
    # CUSTOM FONT
    # --------------------------------------------------

    if font_path and os.path.exists(font_path):

        subtitle_filter = (
            f"subtitles={subtitle_path}:"
            f"force_style="
            f"'FontName={font_path},"
            f"FontSize=19,"
            f"Alignment=5,"
            f"MarginV=80,"
            f"Bold=1,"
            f"Outline=3,"
            f"Shadow=2,"
            f"PrimaryColour=&HFFFFFF&'"
        )

    # --------------------------------------------------
    # DEFAULT FONT
    # --------------------------------------------------

    else:

        subtitle_filter = (
            f"subtitles={subtitle_path}:"
            f"force_style="
            f"'FontSize=19,"
            f"Alignment=5,"
            f"MarginV=80,"
            f"Bold=1,"
            f"Outline=3,"
            f"Shadow=2,"
            f"PrimaryColour=&HFFFFFF&'"
        )

    # --------------------------------------------------
    # FINAL RENDER WITH SUBTITLES
    # --------------------------------------------------

    subprocess.call([
        "ffmpeg", "-y",

        "-i", temp_video,
        "-i", mixed_audio,

        "-map", "0:v:0",
        "-map", "1:a:0",

        "-vf", subtitle_filter,

        "-shortest",

        "-c:v", "libx264",
        "-preset", "veryfast",
        "-c:a", "aac",

        output_path
    ])

    print(f"[INFO] Final video saved to: {output_path}")

    return output_path