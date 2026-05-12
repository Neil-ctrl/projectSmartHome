from llama_cpp import Llama
import re

llm = Llama(
    model_path="models/qwen2.5-1.5b-instruct-q4_k_m.gguf",
    n_ctx=256,
    n_threads=4,
    verbose=False
)

PROMPT = """
You are a smart home assistant.

Allowed commands:
- lights on
- lights off
- NOP

You MUST answer in EXACTLY this format:

speech:(...)
command:(...)

You may output MULTIPLE command lines.

Examples:

User: how are you doing
speech:(im doing well.)
command:(NOP)

User: turn off the lights then turn them on again
speech:(okay, turning the lights off and back on.)
command:(lights off)
command:(lights on)

User: lights on
speech:(turning on the lights.)
command:(lights on)

User: lights off
speech:(turning off the lights.)
command:(lights off)

DO NOT explain.
DO NOT add extra text.
"""


def process(text):

    prompt = f"""
{PROMPT}

User: {text}
"""

    output = llm(
        prompt,
        max_tokens=64,
        temperature=0.0,
        stop=[
            "\n\n",
            "User:",
            "</s>"
        ]
    )

    response = output["choices"][0]["text"]

    print("LLM RAW:", response)

    speech_match = re.search(
        r"speech:\((.*?)\)",
        response,
        re.IGNORECASE | re.DOTALL
    )

    command_matches = re.findall(
        r"command:\((.*?)\)",
        response,
        re.IGNORECASE | re.DOTALL
    )

    speech = speech_match.group(1).strip() if speech_match else ""

    commands = [
        c.strip()
        for c in command_matches
    ]

    return speech, commands