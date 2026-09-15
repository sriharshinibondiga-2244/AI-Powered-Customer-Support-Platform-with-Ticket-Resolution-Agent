def build_context(retrieved_documents):
    """
    Convert retrieved knowledge-base documents
    into context for the Resolution Agent.
    """

    if not retrieved_documents:
        return "No relevant knowledge was found."

    context = ""

    for document in retrieved_documents:
        context += f"""
Title: {document.get('title', '')}
Category: {document.get('category', '')}
Solution:
{document.get('content', '')}

-------------------------
"""

    return context.strip()