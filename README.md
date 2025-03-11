<<<<<<< HEAD
# semi-colon
=======
# Java Security Remediation Project

## Overview
This project automates security fixes for Java applications using Trivy, Jenkins, and GitHub.

## Features
- Detects vulnerable dependencies using Trivy
- Parses vulnerability reports
- Auto-upgrades `pom.xml`
- Runs tests to verify security fixes

## How to Run
1. Clone the repository  
2. Install dependencies (`pip install lxml`)  
3. Run Trivy scan:  
   ```bash
   trivy fs --format json --output trivy-report.json .

>>>>>>> de70e4c (Initial commit)
