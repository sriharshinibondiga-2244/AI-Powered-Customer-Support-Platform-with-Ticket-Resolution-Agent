# ==========================================
# KNOWLEDGE BASE
# ==========================================

knowledge_base = [

    {
        "id": "KB001",
        "title": "VPN Connection Troubleshooting",
        "category": "VPN",
        "content": """
        If the VPN is not connecting:

        1. Verify that the internet connection is working.
        2. Check the VPN username and password.
        3. Restart the VPN client.
        4. Verify that the VPN server is available.
        5. Clear cached VPN credentials.
        6. Reinstall the VPN client if the problem continues.
        """
    },

    {
        "id": "KB002",
        "title": "Payment Deducted but Order Failed",
        "category": "Payment",
        "content": """
        If money has been deducted but the order was not confirmed:

        1. Verify the transaction status.
        2. Check the transaction reference number.
        3. Check whether the order was created.
        4. If payment was successful but the order failed,
           process the refund according to the refund policy.
        """
    },

    {
        "id": "KB003",
        "title": "Password Reset",
        "category": "Account",
        "content": """
        If a customer cannot remember their password:

        1. Select the Forgot Password option.
        2. Enter the registered email address.
        3. Verify the recovery email.
        4. Create a new secure password.
        5. Login again using the new password.
        """
    },

    {
        "id": "KB004",
        "title": "Network Connection Problem",
        "category": "Network",
        "content": """
        If the customer has network connectivity problems:

        1. Check whether the device is connected to the network.
        2. Restart the router.
        3. Check DNS configuration.
        4. Test the connection using another network.
        5. Contact the network administrator if the problem continues.
        """
    },

    {
        "id": "KB005",
        "title": "Account Locked",
        "category": "Account",
        "content": """
        If a customer account is locked:

        1. Verify the customer identity.
        2. Check the number of failed login attempts.
        3. Wait for the account lock period if applicable.
        4. Reset the password if necessary.
        5. Escalate to a human support agent if the account remains locked.
        """
    },

    {
        "id": "KB006",
        "title": "Refund Request",
        "category": "Payment",
        "content": """
        For refund requests:

        1. Verify the transaction.
        2. Check the refund eligibility.
        3. Verify the original payment method.
        4. Initiate the refund according to company policy.
        5. Inform the customer about the expected refund time.
        """
    }

]


def get_all_articles():
    """
    Return all knowledge-base articles.
    """
    return knowledge_base


def search_knowledge(query):
    """
    Simple keyword-based knowledge retrieval.
    """

    query = query.lower()

    results = []

    for article in knowledge_base:

        searchable_text = (
            article["title"] + " " +
            article["category"] + " " +
            article["content"]
        ).lower()

        if any(word in searchable_text for word in query.split()):

            results.append(article)

    return results