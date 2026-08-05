#text to speech
from __future__ import annotations

import os
from pathlib import Path

import requests


def synthesize_speech(text: str, output_file: Path, voice: str = "alloy") -> Path:
    url = "https://eus2.openai.azure.com/openai/deployments/gpt-4o-mini-tts/audio/speech?api-version=2025-03-01-preview"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer asdasdadasdasdasdasdas",
    }

    payload = {
        "model": "gpt-4o-mini-tts",
        "input": text,
        "voice": voice,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(response.content)
    return output_file


def main() -> None:
    out1 = synthesize_speech(
        text="The quick brown fox jumped over the lazy dog",
        output_file=Path("C:/usecase_04/tts_output_1.mp3"),
        voice="alloy",
    )
    print(f"Saved: {out1}")

    out2 = synthesize_speech(
        text="Hello from Azure OpenAI text to speech.",
        output_file=Path("C:/usecase_04/tts_output_2.mp3"),
        voice="alloy",
    )
    print(f"Saved: {out2}")


if __name__ == "__main__":
    main()
