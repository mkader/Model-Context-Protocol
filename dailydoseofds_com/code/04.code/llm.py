from __future__ import annotations

import json

import requests


def ask_llm(user_prompt: str) -> dict:
    url = "https://eus2.openai.azure.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "api-key": "qwewqewqewqeqweqwewqeqewqe",
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 1000,
        "model": "EGPT-4.1",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def main() -> None:
    result = ask_llm("Say hello in one short sentence.")
    print(json.dumps(result, indent=2, ensure_ascii=True))

    result = ask_llm("Summarize what speech-to-text means in one sentence.")
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()



'''
from openai import OpenAI

endpoint = "https://eus2.openai.azure.com/openai/v1"
deployment_name = "EGPT-4.1"
api_key = "sdffsfsdfsdfdfdfsdfsdfsdsdfsdfsdf"

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
)

print(completion.choices[0].message)
'''

>>>>
ChatCompletionMessage(content='The capital of France is Paris.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None)
