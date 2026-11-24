
from simulation import incident_simulator


def test_suspicious_event_triggers_alert(monkeypatch):
    event = {
        "eventName": "PutBucketPolicy",
        "resourceName": "college-project-data",
        "resourceType": "S3"
    }

    alert_calls = []

    class FakeAlertModule:
        @staticmethod
        def lambda_handler(event):
            alert_calls.append(event)

    monkeypatch.setattr(
        incident_simulator,
        "detect_suspicious_activity",
        lambda event: True
    )

    monkeypatch.setattr(
        incident_simulator.importlib,
        "import_module",
        lambda name: FakeAlertModule
    )

    result = incident_simulator.process_event(event)

    assert result is True
    assert len(alert_calls) == 1
    assert alert_calls[0]["eventName"] == "PutBucketPolicy"
