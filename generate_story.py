import subprocess
import random

STORY_TYPES = [
    "creepy alley encounter",
    "late night horror walk",
    "abandoned street mystery",
    "urban night paranoia story",
    "disturbing shadow encounter",
    "silent city horror experience",
    "eerie footsteps story",
    "haunted neighborhood tale",
    "strange voice in the city narrative",
    "schizophrenic urban horror story",
    "mental breakdown in the city story"
]


def generate_story():

    story_type = random.choice(STORY_TYPES)

    prompt = f"""
You are writing a horror story for AI voice narration.

CRITICAL OUTPUT RULES:
- Return ONLY final story text
- No thinking, no drafting, no repetition
- No broken words or partial syllables
- No duplicated fragments like "co co", "Sud Sud", "re re"
- No line breaks
- Fully formed English sentences only
- No repeating words or phrases
- No chinese letters or other non-english characters

STYLE:
- Horror / suspense tone
- First-person perspective
- 250-350 words
- Clean, natural grammar
- Short sentences for narration
- Vivid descriptions of the environment and emotions
- Have a cohesive storyline with a clear beginning, middle, and end
- Mix short and medium sentences. Avoid uniform sentence length


IMPORTANT:
This will be spoken by a TTS system. The text must be perfectly clean and readable aloud.

Topic: {story_type}

OUTPUT ONLY THE STORY.
"""

    result = subprocess.run(
        ["ollama", "run", "qwen2.5"],
        input=prompt,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    story = result.stdout.strip()

    return {
        "title": story_type,
        "script": story
    }