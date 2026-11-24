
from simulation.aws_environment import SimulatedAWSEnvironment
from pathlib import Path
import json
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIRECTORY = PROJECT_ROOT / "logs"
REPORT_FILE = LOG_DIRECTORY / "remediation_reports.json"


def save_remediation_report(report):
    """Save remediation activity."""

    LOG_DIRECTORY.mkdir(exist_ok=True)

    try:
        with open(REPORT_FILE, "r") as file:
            reports = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        reports = []

    reports.append(report)

    with open(REPORT_FILE, "w") as file:
        json.dump(reports, file, indent=4)


def remediate_s3_bucket(bucket_name):
    """Remediate public-access misconfiguration."""

    environment = SimulatedAWSEnvironment()

    bucket = environment.get_s3_bucket(bucket_name)

    if bucket is None:
        return {
            "status": "FAILED",
            "message": "S3 bucket not found"
        }

    if (
        bucket["public_access"] is False
        and bucket["block_public_access"] is True
    ):
        return {
            "status": "NO_ACTION",
            "message": "Bucket is already protected"
        }

    print("\n========== S3 REMEDIATION ==========")
    print(f"Target bucket: {bucket_name}")

    updated_configuration = {
        "public_access": False,
        "block_public_access": True,
        "encryption_enabled": True
    }

    environment.update_s3_bucket(
        bucket_name,
        updated_configuration
    )

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resource": bucket_name,
        "resource_type": "S3",
        "action": "PUBLIC_ACCESS_BLOCKED",
        "status": "SUCCESS",
        "details": "Public access disabled and encryption enabled."
    }

    save_remediation_report(report)

    print("Public access: DISABLED")
    print("Block public access: ENABLED")
    print("Encryption: ENABLED")
    print("Remediation status: SUCCESS")
    print("====================================\n")

    return report


def lambda_handler(event, context=None):

    bucket_name = event.get(
        "bucket_name",
        "college-project-data"
    )

    result = remediate_s3_bucket(bucket_name)

    return {
        "statusCode": 200 if result["status"] != "FAILED" else 404,
        "body": json.dumps(result)
    }


if __name__ == "__main__":

    result = lambda_handler({
        "bucket_name": "college-project-data"
    })

    print(result)
