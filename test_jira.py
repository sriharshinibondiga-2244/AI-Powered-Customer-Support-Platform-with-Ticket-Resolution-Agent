from jira_service import create_jira_issue


result = create_jira_issue(
    ticket_id="TEST-001",
    customer_name="Sri Harshini",
    customer_email="sriharshinibondiga@gmail.com",
    query="My TV sound is low",
    category="Technical",
    priority="High",
    confidence=69,
    resolution=(
        "Please check the TV volume level, "
        "mute settings, audio output settings, "
        "and reconnect the audio device if applicable."
    )
)


print("======================================")
print("JIRA TEST SUCCESS")
print("Issue Key:", result["issue_key"])
print("Issue URL:", result["issue_url"])
print("======================================")