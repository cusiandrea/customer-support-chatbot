from typing import List, Dict

from app.llm.client import LocalLLM


llm = LocalLLM()


def build_context_from_chunks(retrieved_chunks: List[Dict]) -> str:
    context_parts = []

    for chunk in retrieved_chunks:
        source = chunk.get("source", "unknown")
        text = chunk.get("text", "")
        context_parts.append(f"[Source: {source}]\n{text}")

    return "\n\n".join(context_parts)


def build_system_prompt() -> str:
    return (
        "You are a customer support assistant for an e-commerce company.\n"
        "Write in a polite, professional, and empathetic tone.\n"
        "Use only the information provided in the context.\n"
        "Do not invent policies, timelines, conditions, or exceptions.\n"
        "If the context is not enough to answer safely, say that the case should be reviewed by a human support agent.\n"
        "Keep the answer concise and clear.\n"
        "Do not mention internal systems, retrieval, chunks, or source formatting."
    )


def build_user_prompt(user_query: str, context: str) -> str:
    return (
        f"Context:\n{context}\n\n"
        f"Customer question:\n{user_query}\n\n"
        "Please provide a helpful customer support answer based only on the context above."
    )


def generate_response(user_query: str, retrieved_chunks: List[Dict]) -> str:
    if not retrieved_chunks:
        return (
            "I could not find enough information in the policy documents to answer your request. "
            "Please contact a human support agent for further assistance."
        )

    context = build_context_from_chunks(retrieved_chunks)
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(user_query, context)

    response = llm.generate(system_prompt, user_prompt)

    if not response:
        return (
            "I could not generate a reliable answer from the available policy information. "
            "Please contact a human support agent for further assistance."
        )

    return response