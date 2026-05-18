import os
import torch
from TTS.api import TTS

# -------------------------------------------------
# Setup
# -------------------------------------------------
os.environ["COQUI_TOS_AGREED"] = "1"

device = "cuda" if torch.cuda.is_available() else "cpu"

# -------------------------------------------------
# Load XTTS (stable mode)
# -------------------------------------------------
tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=torch.cuda.is_available()
)

# -------------------------------------------------
# Horror pacing enhancer
# -------------------------------------------------
def improve_pacing(text: str) -> str:
    text = text.replace(".", "... ")
    text = text.replace(",", ", ")
    text = text.replace("!", "...!")
    text = text.replace("?", "...?")
    return text


# -------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------
def generate_voice(script_text, output_path):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    script_text = script_text.replace("\n", " ")

    #script_text = improve_pacing(script_text)

    # FIX: let XTTS choose default speaker internally
    tts.tts_to_file(
        text=script_text,
        file_path=output_path,
        speaker = "Gracie Wise",
        language="en"
    )

    print(f"[XTTS] Saved voice -> {output_path}")