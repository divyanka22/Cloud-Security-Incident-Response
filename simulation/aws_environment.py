

import json
from pathlib import Path


class SimulatedAWSEnvironment:

    def __init__(self, state_file=None):
        self.state_file = (
            Path(state_file) if state_file
            else Path(__file__).parent / "environment_state.json"
        )

        if self.state_file.exists():
            with open(self.state_file, "r") as file:
                self.resources = json.load(file)
        else:
            self.resources = {
                "s3_buckets": {
                    "college-project-data": {
                        "public_access": True,
                        "block_public_access": False,
                        "encryption_enabled": False
                    }
                },
                "security_groups": {
                    "sg-001": {
                        "description": "Test web server security group",
                        "inbound_rules": [
                            {
                                "protocol": "tcp",
                                "port": 22,
                                "source": "0.0.0.0/0"
                            },
                            {
                                "protocol": "tcp",
                                "port": 443,
                                "source": "0.0.0.0/0"
                            }
                        ]
                    }
                }
            }

        self.save_state()

    def save_state(self):
        with open(self.state_file, "w") as file:
            json.dump(self.resources, file, indent=4)

    def get_resources(self):
        return self.resources

    def get_s3_bucket(self, bucket_name):
        return self.resources["s3_buckets"].get(bucket_name)

    def get_security_group(self, group_id):
        return self.resources["security_groups"].get(group_id)

    def update_s3_bucket(self, bucket_name, configuration):
        if bucket_name not in self.resources["s3_buckets"]:
            raise ValueError("S3 bucket not found")

        self.resources["s3_buckets"][bucket_name].update(configuration)
        self.save_state()

    def update_security_group(self, group_id, configuration):
        if group_id not in self.resources["security_groups"]:
            raise ValueError("Security group not found")

        self.resources["security_groups"][group_id].update(configuration)
        self.save_state()

    def display_resources(self):
        print("\n========== SIMULATED AWS ENVIRONMENT ==========")
        print(json.dumps(self.resources, indent=4))
        print("================================================\n")


if __name__ == "__main__":
    environment = SimulatedAWSEnvironment()
    environment.display_resources()
