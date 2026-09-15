from retriever import retrieve_knowledge
from context_builder import build_context
from resolution_generator import generate_resolution


def run_rag(query):

    # STEP 1: Retrieve relevant knowledge
    retrieved_documents = retrieve_knowledge(query)

    # STEP 2: Build context
    context = build_context(retrieved_documents)

    # STEP 3: Generate resolution
    resolution = generate_resolution(
        query,
        context
    )

    return {
        "query": query,
        "retrieved_documents": retrieved_documents,
        "context": context,
        "resolution": resolution
    }