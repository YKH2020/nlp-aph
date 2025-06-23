from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="sk-no-key-required"
)

def ask_zephyr(prompt: str, model: str = "APH") -> str:
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are APH, an AI assistant. Your top priority is helping "
                    "parents of children with autism with advice, resources, and emotional "
                    "support for helping their child. Always respond with empathy and understanding."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content