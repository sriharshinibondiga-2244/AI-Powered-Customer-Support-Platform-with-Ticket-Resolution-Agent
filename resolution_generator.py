# ==========================================
# AI RESOLUTION GENERATOR
# ==========================================

def generate_resolution(query, context):

    if not context or context == "No relevant knowledge was found.":

        return {
            "response": (
                "We could not find a suitable solution in our "
                "knowledge base. Your issue will be reviewed by "
                "a support agent."
            ),
            "confidence": 0
        }

    # For now, generate a grounded response
    # directly from the retrieved knowledge.

    response = (
        "Based on our support knowledge base, "
        "here is the recommended solution:\n\n"
        + context
        + "\n\n"
        "If the issue continues after following these steps, "
        "the ticket can be escalated to a human support agent."
    )

    return {
        "response": response,
        "confidence": 85
    }