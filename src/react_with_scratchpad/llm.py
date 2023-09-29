
import os

from typing import cast, Any

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def complete(message: str) -> str:
    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": message,
            }],
            temperature=0)
    return cast(Any, completion).choices[0].message.content
