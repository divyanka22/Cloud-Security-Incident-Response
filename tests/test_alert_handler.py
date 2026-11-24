
import importlib

alert_module = importlib.import_module("lambda.alert_handler")


def test_alert_generation():
    event = {
        "eventName": "PutBucketPolicy",
        "resourceName": "college-project-data",
        "resourceType": "S3"
    }

    alert = alert_module.generate_alert(event)

    assert alert["severity"] == "HIGH"
    assert alert["incident_type"] == "PutBucketPolicy"
    assert alert["resource"] == "college-project-data"
    assert alert["resource_type"] == "S3"
    assert alert["status"] == "OPEN"
    assert "alert_id" in alert
