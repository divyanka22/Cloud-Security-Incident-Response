# Cloud Security Incident Response Runbook with Automated Alerting

## 1. Project Overview

The Cloud Security Incident Response Runbook with Automated Alerting is a Python-based project designed to simulate cloud security monitoring, suspicious activity detection, automated alert generation, and security remediation.

The project demonstrates how suspicious activities in a simulated AWS environment can be identified and handled through an automated incident response workflow.

## 2. Objectives

- Simulate an AWS cloud environment.
- Detect suspicious cloud API activities.
- Generate automated security alerts.
- Identify insecure S3 bucket configurations.
- Simulate security group remediation.
- Maintain incident logs and remediation reports.
- Demonstrate cloud security incident response procedures.

## 3. Technologies Used

- **Programming Language:** Python
- **Cloud Platform:** AWS (CloudFormation template and AWS service concepts)
- **Testing Framework:** Pytest
- **Data Format:** JSON
- **Development Environment:** Visual Studio Code

## 4. Key Features

### 4.1 Suspicious Activity Detection
Monitors simulated cloud API events and identifies suspicious activities such as:
- PutBucketPolicy
- PutBucketAcl
- PutBucketPublicAccessBlock
- AuthorizeSecurityGroupIngress

### 4.2 Automated Security Alerting
Generates HIGH-severity security alerts when suspicious activities are detected and stores alert details in JSON files.

### 4.3 S3 Bucket Remediation
Simulates security improvements by:
- Disabling public access.
- Enabling Block Public Access.
- Enabling server-side encryption.

### 4.4 Security Group Remediation
Identifies and removes unrestricted SSH access while preserving other inbound rules, such as HTTPS.

### 4.5 Incident Logging
Stores security events, generated alerts, and remediation reports for monitoring and review.

## 5. Project Structure

```text
Cloud-Security-Incident-Response/
│
├── cloudformation/
│   └── main-template.yaml
│
├── lambda/
│   ├── alert_handler.py
│   ├── s3_remediation.py
│   └── security_group_remediation.py
│
├── logs/
│   ├── incident_events.json
│   ├── security_alerts.json
│   └── remediation_reports.json
│
├── runbook/
│
├── simulation/
│   ├── aws_environment.py
│   ├── incident_simulator.py
│   └── environment_state.json
│
├── tests/
│   ├── test_alert_handler.py
│   ├── test_environment.py
│   ├── test_incident_pipeline.py
│   ├── test_s3_remediation.py
│   └── test_security_group_remediation.py
│
├── requirements.txt
└── README.md
```

## 6. Installation and Execution

### Prerequisites
- Python 3.10 or later
- Visual Studio Code
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/divyanka22/Cloud-Security-Incident-Response
```

### Step 2: Navigate to the Project

```bash
cd Cloud-Security-Incident-Response
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 6: Run the Incident Simulator

```bash
python -m simulation.incident_simulator
```

The simulator generates sample cloud security events, detects suspicious activities, and automatically generates security alerts.

### Step 7: Run Automated Tests

```bash
python -m pytest -v
```

## 7. Testing Results

The project was tested using Pytest.

| Test Case | Result |
|---|---|
| Simulated AWS environment | PASSED |
| Security alert generation | PASSED |
| Incident detection and alert integration | PASSED |
| S3 bucket remediation | PASSED |
| Security group remediation | PASSED |
| **Total** | **5/5 PASSED** |

## 8. AWS Deployment

The project includes an AWS CloudFormation template illustrating the infrastructure design.

The current implementation uses a local simulated AWS environment. Actual AWS deployment and live AWS API integration have not been performed.

## 9. Limitations

- Security events are simulated rather than collected from a live AWS account.
- Alerts are generated locally rather than delivered through a live SNS notification service.
- Remediation actions modify simulated resources rather than actual AWS resources.
- CloudFormation deployment has not been performed.

## 10. Future Enhancements

- Integrate live AWS CloudTrail events.
- Implement AWS Lambda-based incident response.
- Configure Amazon SNS email notifications.
- Add a security monitoring dashboard.
- Expand automated remediation capabilities.

## 11. Conclusion

This project demonstrates the fundamentals of cloud security monitoring and incident response through a Python-based simulation. It combines suspicious activity detection, automated alert generation, security remediation, incident logging, and automated testing into a single workflow.

The project provides a foundation for understanding how automated cloud security incident response systems can be designed and extended.