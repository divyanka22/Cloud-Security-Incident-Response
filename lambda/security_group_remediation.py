
from simulation.aws_environment import SimulatedAWSEnvironment
from pathlib import Path
import json
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIRECTORY = PROJECT_ROOT / "logs"
REPORT_FILE = LOG_DIRECTORY / "remediation_reports.json"


def save_report(report):
    LOG_DIRECTORY.mkdir(exist_ok=True)

    try:
        with open(REPORT_FILE, "r") as file:
            reports = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        reports = []

    reports.append(report)

    with open(REPORT_FILE, "w") as file:
        json.dump(reports, file, indent=4)


def remediate_security_group(group_id):

    environment = SimulatedAWSEnvironment()

    security_group = environment.get_security_group(group_id)

    if security_group is None:
        return {
            "status": "FAILED",
            "message": "Security group not found"
        }

    print("\n====== SECURITY GROUP REMEDIATION ======")
    print(f"Target security group: {group_id}")

    original_rules = security_group["inbound_rules"]

    updated_rules = [
        rule for rule in original_rules
        if not (
            rule["port"] == 22
            and rule["protocol"] == "tcp"
            and rule["source"] == "0.0.0.0/0"
        )
    ]

    if len(updated_rules) == len(original_rules):
        print("No unrestricted SSH rule found.")

        return {
            "status": "NO_ACTION",
            "message": "Security group is already protected"
        }

    environment.update_security_group(
        group_id,
        {"inbound_rules": updated_rules}
    )

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resource": group_id,
        "resource_type": "EC2_SECURITY_GROUP",
        "action": "UNRESTRICTED_SSH_RULE_REMOVED",
        "status": "SUCCESS",
        "details": "Unrestricted SSH inbound rule removed."
    }

    save_report(report)

    print("Unrestricted SSH access: REMOVED")
    print("Other inbound rules: PRESERVED")
    print("Remediation status: SUCCESS")
    print("========================================\n")

    return report


def lambda_handler(event, context=None):

    group_id = event.get("group_id", "sg-001")

    result = remediate_security_group(group_id)

    return {
        "statusCode": 200 if result["status"] != "FAILED" else 404,
        "body": json.dumps(result)
    }


if __name__ == "__main__":

    result = lambda_handler({
        "group_id": "sg-001"
    })

    print(result)
