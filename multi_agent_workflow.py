from rag_pipeline import run_rag


# =====================================================
# 01 - DIAGNOSIS AGENT
# =====================================================

def diagnosis_agent(query):

    text = query.lower()

    # PAYMENT
    if any(word in text for word in [
        "payment",
        "paid",
        "transaction",
        "deducted",
        "charged",
        "upi",
        "credit card",
        "debit card"
    ]):
        category = "Payment"
        intent = "Payment issue"

    # REFUND
    elif any(word in text for word in [
        "refund",
        "money back",
        "reimbursement"
    ]):
        category = "Refund"
        intent = "Refund request"

    # DELIVERY
    elif any(word in text for word in [
        "delivery",
        "delivered",
        "package",
        "shipping",
        "shipment",
        "delayed delivery"
    ]):
        category = "Delivery"
        intent = "Delivery issue"

    # ORDER
    elif any(word in text for word in [
        "order",
        "purchase",
        "cancel order",
        "cancel my order"
    ]):
        category = "Order"
        intent = "Order issue"

    # ACCOUNT
    elif any(word in text for word in [
        "password",
        "login",
        "log in",
        "account",
        "sign in",
        "forgot password",
        "account locked"
    ]):
        category = "Account"
        intent = "Account access issue"

    # TV / ELECTRONICS
    elif any(word in text for word in [
        "tv",
        "television",
        "tv not working",
        "tv won't turn on",
        "tv not turning on",
        "tv sound",
        "tv audio",
        "tv screen",
        "tv display",
        "tv remote",
        "remote control"
    ]):
        category = "Technical"
        intent = "TV technical issue"

    # GENERAL TECHNICAL
    elif any(word in text for word in [
        "vpn",
        "server",
        "application",
        "app",
        "website",
        "error",
        "crash",
        "network",
        "internet",
        "wifi",
        "wi-fi",
        "technical"
    ]):
        category = "Technical"
        intent = "Technical issue"

    # SECURITY
    elif any(word in text for word in [
        "fraud",
        "hacked",
        "unauthorized",
        "stolen",
        "security",
        "scam"
    ]):
        category = "Security"
        intent = "Security issue"

    # PRODUCT
    elif any(word in text for word in [
        "product",
        "item",
        "device",
        "damaged",
        "broken",
        "not working"
    ]):
        category = "Product"
        intent = "Product issue"

    # GENERAL
    else:
        category = "General"
        intent = "General support request"

    # =================================================
    # DIAGNOSIS CONFIDENCE
    # =================================================

    confidence_map = {
        "Payment": 94,
        "Refund": 92,
        "Delivery": 90,
        "Order": 90,
        "Account": 91,
        "Technical": 88,
        "Security": 96,
        "Product": 86,
        "General": 75
    }

    confidence = confidence_map.get(category, 75)

    return {
        "agent": "Diagnosis Agent",
        "category": category,
        "intent": intent,
        "confidence": confidence,
        "status": "Completed"
    }


# =====================================================
# 02 - RETRIEVAL AGENT
# =====================================================

def calculate_similarity(query, article):

    query_text = query.lower()

    keywords = [
        keyword.lower()
        for keyword in article.get("keywords", [])
    ]

    # Count actual keyword/phrase matches
    keyword_matches = 0

    for keyword in keywords:
        if keyword in query_text:
            keyword_matches += 1

    title = article.get("title", "").lower()

    title_words = [
        word for word in title.split()
        if len(word) > 2
    ]

    title_matches = 0

    for word in title_words:
        if word in query_text:
            title_matches += 1

    # -----------------------------------------------
    # RELEVANCE SCORE
    # -----------------------------------------------

    # Strong match
    if keyword_matches >= 2:
        return 90

    # Partial/weak but relevant match
    elif keyword_matches == 1:
        return 60

    # Some title relevance
    elif title_matches >= 2:
        return 60

    elif title_matches == 1:
        return 50

    # No meaningful relevance
    return 0


def retrieval_agent(query):

    rag_result = run_rag(query)

    documents = rag_result.get(
        "retrieved_documents",
        []
    )

    context = rag_result.get(
        "context",
        ""
    )

    if documents:

        top_document = documents[0]

        article_title = top_document.get(
            "title",
            "Knowledge Article"
        )

        # IMPORTANT:
        # Calculate similarity from the actual article
        similarity = calculate_similarity(
            query,
            top_document
        )

        if similarity > 0:
            status = "Knowledge retrieved"
        else:
            status = "Weak knowledge match"

    else:

        article_title = "No relevant knowledge article"

        similarity = 0

        status = "No relevant knowledge found"

    return {

        "agent": "Retrieval Agent",

        "documents": documents,

        "article_title": article_title,

        "similarity": similarity,

        "context": context,

        "rag_result": rag_result,

        "status": status
    }


# =====================================================
# 03 - RESOLUTION AGENT
# =====================================================

def resolution_agent(
    query,
    retrieval_result
):

    rag_result = retrieval_result.get(
        "rag_result",
        {}
    )

    resolution_data = rag_result.get(
        "resolution",
        {}
    )

    resolution = resolution_data.get(
        "response",
        ""
    )

    original_confidence = resolution_data.get(
        "confidence",
        0
    )

    # Get actual retrieval confidence
    retrieval_similarity = retrieval_result.get(
        "similarity",
        0
    )

    # -------------------------------------------------
    # IMPORTANT:
    # Resolution cannot be more confident than
    # the knowledge retrieval itself.
    # -------------------------------------------------

    if retrieval_similarity == 0:

        confidence = 0

    else:

        confidence = min(
            original_confidence,
            retrieval_similarity
        )

    if not resolution:

        resolution = (
            "No automated resolution could be generated. "
            "Additional investigation is required."
        )

    if confidence > 0:

        status = "Resolution generated"

    else:

        status = "Investigation required"

    return {

        "agent": "Resolution Agent",

        "resolution": resolution,

        "confidence": confidence,

        "status": status
    }


# =====================================================
# 04 - VALIDATION AGENT
# =====================================================

def validation_agent(
    diagnosis_result,
    retrieval_result,
    resolution_result
):

    diagnosis_confidence = diagnosis_result.get(
        "confidence",
        0
    )

    retrieval_similarity = retrieval_result.get(
        "similarity",
        0
    )

    resolution_confidence = resolution_result.get(
        "confidence",
        0
    )

    validation_confidence = int(
        (
            diagnosis_confidence
            + retrieval_similarity
            + resolution_confidence
        ) / 3
    )

    # =================================================
    # 70% THRESHOLD
    # =================================================

    if validation_confidence >= 70:

        decision = "AUTO_RESOLVE"

        reason = (
            "Diagnosis, knowledge retrieval and "
            "resolution passed the 70% confidence threshold."
        )

    else:

        decision = "ESCALATE"

        reason = (
            "Validation confidence is below the 70% "
            "threshold. Human support is required."
        )

    return {

        "agent": "Validation Agent",

        "confidence": validation_confidence,

        "decision": decision,

        "reason": reason,

        "status": "Validated"
    }


# =====================================================
# 05 - ESCALATION AGENT
# =====================================================

def escalation_agent(validation_result):

    decision = validation_result.get(
        "decision"
    )

    if decision == "ESCALATE":

        final_decision = (
            "ESCALATE TO HUMAN SUPPORT"
        )

        escalation = (
            "Escalated to Human Agent"
        )

        status = (
            "Human support required"
        )

    else:

        final_decision = (
            "AUTOMATICALLY RESOLVED"
        )

        escalation = (
            "Handled by AI"
        )

        status = (
            "Resolved by AI"
        )

    return {

        "agent": "Escalation Agent",

        "decision": final_decision,

        "escalation": escalation,

        "status": status
    }


# =====================================================
# COMPLETE MULTI-AGENT WORKFLOW
# =====================================================

def run_multi_agent_workflow(query):

    # 1. Diagnosis
    diagnosis = diagnosis_agent(
        query
    )

    # 2. Knowledge Retrieval
    retrieval = retrieval_agent(
        query
    )

    # 3. Resolution
    resolution = resolution_agent(
        query,
        retrieval
    )

    # 4. Validation
    validation = validation_agent(
        diagnosis,
        retrieval,
        resolution
    )

    # 5. Escalation
    escalation = escalation_agent(
        validation
    )

    return {

        "workflow": {

            "diagnosis": diagnosis,

            "retrieval": retrieval,

            "resolution": resolution,

            "validation": validation,

            "escalation": escalation
        },

        "final_decision":
            escalation["decision"],

        "escalation":
            escalation["escalation"],

        "resolution":
            resolution["resolution"],

        "confidence":
            validation["confidence"]
    }