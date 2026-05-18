import whisper
import re

# --------------------------------------------------
# LOAD MODEL ONCE (IMPORTANT FOR BATCH SPEED)
# --------------------------------------------------

_model = whisper.load_model("base")


def format_timestamp(seconds):

    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)

    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"


# --------------------------------------------------
# SENTENCE DETECTION HELPERS
# --------------------------------------------------

SENTENCE_ENDINGS = {".", "?", "!", "…"}


def is_sentence_end(word):
    return any(word.strip().endswith(p) for p in SENTENCE_ENDINGS)


def clean_word(w):
    return w["word"].strip()


# --------------------------------------------------
# GROUP WORDS INTO NATURAL SENTENCES
# --------------------------------------------------

def group_into_sentences(words):

    sentences = []
    current = []

    for w in words:

        current.append(w)

        if is_sentence_end(w["word"]) or len(current) >= 18:
            sentences.append(current)
            current = []

    if current:
        sentences.append(current)

    return sentences


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

def generate_subtitles(audio_path, output_srt):

    result = _model.transcribe(
        audio_path,
        word_timestamps=True,
        fp16=False
    )

    subtitle_entries = []

    for segment in result["segments"]:

        words = segment.get("words", [])

        if not words:
            continue

        sentences = group_into_sentences(words)

        for sentence in sentences:

            start = sentence[0]["start"]
            end = sentence[-1]["end"]

            text = " ".join(clean_word(w) for w in sentence)

            # --------------------------------------------------
            # CLEAN UP SUBTITLE TEXT
            # --------------------------------------------------

            text = re.sub(r"\s+", " ", text).strip()
            text = text.upper()

            subtitle_entries.append({
                "start": start,
                "end": end,
                "text": text
            })

    # --------------------------------------------------
    # WRITE SRT FILE
    # --------------------------------------------------

    with open(output_srt, "w", encoding="utf-8") as f:

        for idx, sub in enumerate(subtitle_entries, start=1):

            f.write(f"{idx}\n")
            f.write(
                f"{format_timestamp(sub['start'])} --> "
                f"{format_timestamp(sub['end'])}\n"
            )
            f.write(sub["text"] + "\n\n")

    return output_srt