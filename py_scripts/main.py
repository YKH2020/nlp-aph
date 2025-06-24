import sys
import os
from knowledge_prompt import retrieve_context
from zephyr import ask_zephyr

SUMMARY_PATH = ".summary.txt"

def clean_response(text: str) -> str:
    text = text.replace("</s>", "").strip()
    return text

def load_summary() -> str:
    if os.path.exists(SUMMARY_PATH):
        with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_summary(summary: str):
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write(summary)

def update_summary(previous_summary: str, last_user_query: str, last_response: str) -> str:
    return previous_summary + f"\nUser: {last_user_query}\nAPH: {last_response}\n"

def format_prompt(summary: str, context: str, query: str) -> str:
    return f"""Chat Summary:
{summary.strip() or '[No prior conversation yet]'}

Retrieved Knowledge:
{context.strip()}

User Query:
{query.strip()}"""

def main():
    # 🧹 Clear memory if requested
    if len(sys.argv) == 2 and sys.argv[1] == "--clear":
        save_summary("")
        print("Chat summary cleared.")
        return

    if len(sys.argv) > 1:
        # 🚀 CLI mode
        query = " ".join(sys.argv[1:]).strip()
        chat_summary = load_summary()

        context = retrieve_context(query)
        full_prompt = format_prompt(chat_summary, context, query)
        response = ask_zephyr(full_prompt)
        cleaned = clean_response(response)

        print(cleaned)

        chat_summary = update_summary(chat_summary, query, cleaned)

        if chat_summary.count("\n") > 3:
            summary_prompt = f"Summarize this conversation in 2-3 sentences:\n\n{chat_summary}"
            condensed = ask_zephyr(summary_prompt)
            chat_summary = condensed.strip()

        save_summary(chat_summary)

    else:
        # 🖥️ Interactive mode
        chat_summary = load_summary()

        while True:
            query = input("Your question (or 'exit'): ").strip()
            if query.lower() in {"exit", "quit"}:
                break

            context = retrieve_context(query)
            full_prompt = format_prompt(chat_summary, context, query)
            response = ask_zephyr(full_prompt)
            print("\nResponse:\n" + response)

            chat_summary = update_summary(chat_summary, query, response)

            if chat_summary.count("\n") > 3:
                summary_prompt = f"Summarize this conversation in 2-3 sentences:\n\n{chat_summary}"
                condensed = ask_zephyr(summary_prompt)
                chat_summary = condensed.strip()

            save_summary(chat_summary)

if __name__ == "__main__":
    main()