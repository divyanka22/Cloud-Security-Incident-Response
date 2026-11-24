import json
import importlib
from datetime import datetime, timezone


SUSPICIOUS_EVENTS = {
    "PutBucketPolicy",
    "PutBucketAcl",
    "PutBucketPublicAccessBlock",
    "AuthorizeSecurityGroupIngress"
}


def create_security_event(event_name, resource_name, resource_type):
    """Create a simulated AWS CloudTrail event."""

    event = {
        "eventTime": datetime.now(timezone.utc).isoformat(),
        "eventSource": "s3.amazonaws.com"
        if resource_type == "S3"
        else "ec2.amazonaws.com",
        "eventName": event_name,
        "resourceName": resource_name,
        "resourceType": resource_type,
        "userIdentity": {
            "type": "IAMUser",
            "userName": "test-user"
        }
    }

    return event


def detect_suspicious_activity(event):
    """Check whether an API event is suspicious."""

    event_name = event.get("eventName")

    if event_name in SUSPICIOUS_EVENTS:
        print("\n[ALERT] Suspicious API activity detected!")
        print(f"Event: {event_name}")
        print(f"Resource: {event.get('resourceName')}")
        print(f"Type: {event.get('resourceType')}")

        return True

    print(f"[INFO] Normal activity: {event_name}")
    return False

def process_event(event):
    """Detect suspicious activity and generate an alert automatically."""

    is_suspicious = detect_suspicious_activity(event)

    if is_suspicious:
        alert_module = importlib.import_module(
            "lambda.alert_handler"
        )

        alert_module.lambda_handler(event)

    return is_suspicious

def save_event(event):
    """Save event details to a JSON file."""

    log_file = "logs/incident_events.json"

    try:
        with open(log_file, "r") as file:
            events = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        events = []

    events.append(event)

    with open(log_file, "w") as file:
        json.dump(events, file, indent=4)


if __name__ == "__main__":

    print("========== INCIDENT DETECTION SYSTEM ==========")

    test_events = [
        create_security_event(
            "PutBucketPolicy",
            "college-project-data",
            "S3"
        ),
        create_security_event(
            "AuthorizeSecurityGroupIngress",
            "sg-001",
            "EC2"
        ),
        create_security_event(
            "ConsoleLogin",
            "AWS Console",
            "IAM"
        )
    ]

    for event in test_events:
        save_event(event)
        process_event(event)

    print("\nDetection process completed.")
