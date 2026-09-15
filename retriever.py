from knowledge_base import search_knowledge


def retrieve_knowledge(query, top_k=3):
    """
    Retrieve the most relevant knowledge-base articles
    for the customer query.
    """

    results = search_knowledge(query)

    if not results:
        return []

    return results[:top_k]