SYSTEM_INSTRUCTIONS = (
    "You are a document QA assistant. Answer the user's question using ONLY the provided context snippets. "
    "If the answer is not in the context, say you cannot find it. Cite short quotes from the context when helpful."
)


PROMPT_TEMPLATE = (
    "System: {system}\n\n"
    "Context:\n{context}\n\n"
    "User question: {question}\n\n"
    "Assistant:"
)