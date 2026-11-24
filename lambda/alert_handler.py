
import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIRECTORY = PROJECT_ROOT / "logs"
ALERT_FILE = LOG_DIRECTORY / "security_alerts.json"


def generate_alert(event):
    """Generate a security alert from a suspicious event."""

    alert = {
        "alert_id": f"SEC-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "severity": "HIGH",
        "incident_type": event.get("eventName", "Unknown"),
        "resource": event.get("resourceName", "Unknown"),
        "resource_type": event.get("resourceType", "Unknown"),
        "message": "Suspicious cloud security activity detected.",
        "status": "OPEN"
    }

    return alert


def send_notification(alert):
    """Simulate an Amazon SNS notification."""

    LOG_DIRECTORY.mkdir(exist_ok=True)

    try:
        with open(ALERT_FILE, "r") as file:
            alerts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        alerts = []

    alerts.append(alert)

    with open(ALERT_FILE, "w") as file:
        json.dump(alerts, file, indent=4)

    print("\n========== SECURITY NOTIFICATION ==========")
    print(f"Alert ID: {alert['alert_id']}")
    print(f"Severity: {alert['severity']}")
    print(f"Incident: {alert['incident_type']}")
    print(f"Resource: {alert['resource']}")
    print(f"Message: {alert['message']}")
    print("Notification status: GENERATED")
    print("============================================\n")


def lambda_handler(event, context=None):
    """AWS Lambda-compatible alert handler."""

    alert = generate_alert(event)
    send_notification(alert)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Security alert generated successfully",
            "alert_id": alert["alert_id"]
        })
    }


if __name__ == "__main__":

    sample_event = {
        "eventName": "PutBucketPolicy",
        "resourceName": "college-project-data",
        "resourceType": "S3"
    }

    result = lambda_handler(sample_event)
    print(result)
