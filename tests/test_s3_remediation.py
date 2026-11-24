
import importlib

s3_module = importlib.import_module("lambda.s3_remediation")


def test_s3_bucket_remediation(monkeypatch, tmp_path):
    from simulation.aws_environment import SimulatedAWSEnvironment

    env = SimulatedAWSEnvironment(
        state_file=tmp_path / "environment_state.json"
    )

    monkeypatch.setattr(
        s3_module,
        "SimulatedAWSEnvironment",
        lambda: env
    )

    result = s3_module.remediate_s3_bucket("college-project-data")

    bucket = env.get_s3_bucket("college-project-data")

    assert result["status"] == "SUCCESS"
    assert bucket["public_access"] is False
    assert bucket["block_public_access"] is True
    assert bucket["encryption_enabled"] is True
