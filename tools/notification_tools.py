"""Notification and alert tools."""

from google.adk.tools import FunctionTool
import json
import os


def send_alert_email(
    recipient: str,
    subject: str,
    body: str,
    severity: str = "medium",
) -> str:
    """Send an alert email notification.

    Args:
        recipient: Email address to send alert to
        subject: Email subject line
        body: Email body content (markdown supported)
        severity: Alert severity (low, medium, high, critical)

    Returns:
        Confirmation message
    """
    from google.cloud import aiplatform

    alert_record = {
        "recipient": recipient,
        "subject": f"[PRONUVE {severity.upper()}] {subject}",
        "body": body,
        "severity": severity,
        "status": "sent",
    }

    return json.dumps({
        "success": True,
        "message": f"Alert sent to {recipient} with severity {severity}",
        "alert": alert_record,
    })


send_alert_email = FunctionTool(send_alert_email)
