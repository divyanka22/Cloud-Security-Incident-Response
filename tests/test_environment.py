
from simulation.aws_environment import SimulatedAWSEnvironment


def test_environment_creates_default_resources(tmp_path):
    state_file = tmp_path / "environment_state.json"

    env = SimulatedAWSEnvironment(state_file=state_file)

    resources = env.get_resources()

    assert "college-project-data" in resources["s3_buckets"]
    assert "sg-001" in resources["security_groups"]
    assert state_file.exists()
