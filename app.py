"""
app.py
------
Simple command-line interface for your RAG chatbot.

Run:
    python app.py

Type a DSA question, get a grounded answer from your notes.
Type 'exit' to quit.
"""

from chatbot import answer_question

def main():
    print("=" * 50)
    print(" DecodeWher DSA Q&A Bot (RAG-powered)")
    print(" Ask a question about your notes. Type 'exit' to quit.")
    print("=" * 50)

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ("exit", "quit"):
            print("Bye! Keep decoding those DSA problems 👋")
            break
        if not question:
            continue

        answer, sources = answer_question(question)
        print(f"\nBot: {answer}")
        print(f"\n(Sources: {', '.join(sources)})")


if __name__ == "__main__":
    main()
