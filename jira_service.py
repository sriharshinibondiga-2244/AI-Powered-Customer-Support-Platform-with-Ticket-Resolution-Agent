import os
import requests
from dotenv import load_dotenv

load_dotenv()


def create_jira_issue(
    ticket_id,
    customer_name,
    customer_email,
    query,
    category,
    priority,
    confidence,
    resolution
):
    jira_url = os.getenv("JIRA_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    project_key = os.getenv("JIRA_PROJECT_KEY")

    if not all([
        jira_url,
        jira_email,
        jira_api_token,
        project_key
    ]):
        raise Exception("Jira configuration is missing in .env")

    url = f"{jira_url}/rest/api/3/issue"

    description = f"""
SUPPORTAI ESCALATED TICKET

Ticket ID: {ticket_id}

Customer Name: {customer_name}
Customer Email: {customer_email}

Category: {category}
Priority: {priority}
AI Validation Confidence: {confidence}%

Customer Issue:
{query}

AI Recommended Resolution:
{resolution}

Reason for Escalation:
AI confidence was below the 70% threshold.
Human support intervention is required.
"""

    payload = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": f"[SUPPORTAI] {ticket_id} - {query}",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            }
        }
    }

    response = requests.post(
        url,
        auth=(jira_email, jira_api_token),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=20
    )

    if response.status_code not in [200, 201]:
        raise Exception(
            f"Jira error {response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    return {
        "success": True,
        "issue_key": data.get("key"),
        "issue_url": f"{jira_url}/browse/{data.get('key')}"
    }