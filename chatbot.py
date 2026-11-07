"""
chatbot.py
----------
Step 2 of the RAG pipeline: RETRIEVAL + RESPONSE GENERATION.

Given a user question, this module:
1. Embeds the question the same way the notes were embedded
2. Searches FAISS for the top-k most similar chunks (semantic retrieval)
3. Stuffs those chunks into a prompt as "context"
4. Sends the prompt to an OpenAI chat model so the answer is GROUNDED
   in your actual notes, not just the model's general knowledge
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

INDEX_DIR = "faiss_index"

# The prompt is the key to "grounding" — we explicitly tell the model
# to answer ONLY from the provided context, and to admit when it doesn't know.
PROMPT_TEMPLATE = """You are Ari, a sharp, friendly DSA tutor for students on @decodewher's page.
Explain things directly and confidently, like you already know this topic well —
never say phrases like "based on the notes," "according to the context," or
"based on the provided information." Just teach it naturally, the way a tutor
would explain it out loud to a student.

If the context below genuinely doesn't cover what's being asked, say something like
"That's not something I've covered yet — try asking about [a related topic you do
know from the context]" — without mentioning "notes" or "context" as words.

Context:
{context}

Question: {question}

Answer:"""


def load_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return FAISS.load_local(
        INDEX_DIR, embeddings, allow_dangerous_deserialization=True
    )


def retrieve_context(vector_store, question, k=3):
    """Return the top-k most relevant chunks for the question, with their sources."""
    results = vector_store.similarity_search(question, k=k)
    return results


def generate_answer(question, retrieved_chunks, model="gemini-3.5-flash"):
    context_text = "\n\n---\n\n".join(chunk.page_content for chunk in retrieved_chunks)

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    formatted_prompt = prompt.format(context=context_text, question=question)

    llm = ChatGoogleGenerativeAI(model=model, temperature=0)
    response = llm.invoke(formatted_prompt)

    # Gemini 3.x models can return content as a list of parts (text + internal
    # metadata like thought signatures) instead of a plain string. Extract only
    # the actual text so we don't print raw internal structures.
    content = response.content
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, str):
                text_parts.append(part)
            elif isinstance(part, dict) and "text" in part:
                text_parts.append(part["text"])
        return "".join(text_parts).strip()

    return content


def answer_question(question, k=3):
    """Full pipeline: retrieve relevant chunks, then generate a grounded answer."""
    vector_store = load_vector_store()
    chunks = retrieve_context(vector_store, question, k=k)
    answer = generate_answer(question, chunks)

    sources = sorted({os.path.basename(c.metadata.get("source", "")) for c in chunks})
    return answer, sources


if __name__ == "__main__":
    q = "How does merge sort split and merge the array?"
    ans, srcs = answer_question(q)
    print("Q:", q)
    print("\nA:", ans)
    print("\nSources:", srcs)