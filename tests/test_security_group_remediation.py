
import importlib

sg_module = importlib.import_module(
    "lambda.security_group_remediation"
)


def test_security_group_remediation(monkeypatch, tmp_path):
    from simulation.aws_environment import SimulatedAWSEnvironment

    env = SimulatedAWSEnvironment(
        state_file=tmp_path / "environment_state.json"
    )

    monkeypatch.setattr(
        sg_module,
        "SimulatedAWSEnvironment",
        lambda: env
    )

    result = sg_module.remediate_security_group("sg-001")

    security_group = env.get_security_group("sg-001")
    rules = security_group["inbound_rules"]

    assert result["status"] == "SUCCESS"
    assert not any(
        rule["port"] == 22 and rule["source"] == "0.0.0.0/0"
        for rule in rules
    )
    assert any(rule["port"] == 443 for rule in rules)
