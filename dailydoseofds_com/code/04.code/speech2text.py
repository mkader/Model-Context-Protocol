#specch to text
from __future__ import annotations

import argparse
import json
import mimetypes
from pathlib import Path

import requests

def transcribe_audio(file_path: Path) -> dict:
	
	content_type, _ = mimetypes.guess_type(file_path)
	if not content_type:
		content_type = "application/octet-stream"

	url = "https://eus2.openai.azure.com/openai/deployments/gpt-4o-transcribe/audio/transcriptions?api-version=2025-03-01-preview"

	headers = {
		"api-key": "Aasdasddadadasdsdsdasddadsdassdd",
	}

	with file_path.open("rb") as audio_file:
		files = {
			"file": (file_path.name, audio_file, content_type), 
		}
		data = {
			"model": "gpt-4o-transcribe",
		}
		response = requests.post(url, headers=headers, data=data, files=files, timeout=120)

	response.raise_for_status()
	return response.json()


def main() -> None:
    result = transcribe_audio(file_path= Path("C:/solera/ai/mcp/usecase_04/hello_input.wav"))
    print(json.dumps(result, indent=2, ensure_ascii=True))

    result = transcribe_audio(file_path= Path("C:/solera/ai/mcp/usecase_04/openai_input.wav"))
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()

python stt.py
{
  "text": "Hello.",
  "usage": {
    "type": "tokens",
    "total_tokens": 27,
    "input_tokens": 23,
    "input_token_details": {
      "text_tokens": 0,
      "audio_tokens": 23
    },
    "output_tokens": 4
  }
}
{
  "text": "Hello, I know Azure Open AI.",
  "usage": {
    "type": "tokens",
    "total_tokens": 62,
    "input_tokens": 52,
    "input_token_details": {
      "text_tokens": 0,
      "audio_tokens": 52
    },
    "output_tokens": 10
  }
}
