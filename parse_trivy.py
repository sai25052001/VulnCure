import json

def parse_trivy_report(report_file):
    with open(report_file, 'r') as file:
        data = json.load(file)
    
    vulnerabilities = []
    for result in data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            vulnerabilities.append({
                "CVE": vuln["VulnerabilityID"],
                "Package": vuln["PkgName"],
                "Installed": vuln["InstalledVersion"],
                "Fixed": vuln.get("FixedVersion", "Not Available"),
                "Severity": vuln["Severity"]
            })

    return vulnerabilities

if __name__ == "__main__":
    report_path = "trivy-report.json"
    vulnerabilities = parse_trivy_report(report_path)
    
    for vuln in vulnerabilities:
        print(f"Package: {vuln['Package']}, Installed: {vuln['Installed']}, Fixed: {vuln['Fixed']}, Severity: {vuln['Severity']}")

