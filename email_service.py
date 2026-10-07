import os
import smtplib

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def generate_resolution_email(
    customer_name,
    ticket_id,
    query,
    category,
    resolution
):

    email_body = f"""
Hello {customer_name},

We received your support request.

Ticket ID: {ticket_id}
Category: {category}

Your Issue:
{query}

Our AI support system could not automatically resolve
this issue with sufficient confidence.

Recommended steps to resolve the issue:

{resolution}

Please follow the above steps carefully.

If the issue still persists, our human support team
will review your ticket and assist you further.

Ticket ID: {ticket_id}

Thank you,
SUPPORTAI Customer Support Team
"""

    return email_body


def send_resolution_email(
    customer_email,
    customer_name,
    ticket_id,
    query,
    category,
    resolution
):

    sender_email = os.getenv("SUPPORT_EMAIL")
    sender_password = os.getenv("SUPPORT_EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        raise Exception(
            "Email configuration is missing."
        )

    body = generate_resolution_email(
        customer_name,
        ticket_id,
        query,
        category,
        resolution
    )

    message = MIMEMultipart()

    message["From"] = sender_email
    message["To"] = customer_email

    message["Subject"] = (
        f"SUPPORTAI - Ticket {ticket_id} "
        "Resolution Steps"
    )

    message.attach(
        MIMEText(body, "plain")
    )

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.send_message(message)

    return True
