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
    
    if vulnerabilities:
        print(f"Found {len(vulnerabilities)} Vulnerabilities:")
        for vuln in vulnerabilities:
            print(f"CVE: {vuln['CVE']}, Package: {vuln['Package']}, Installed: {vuln['Installed']}, Fixed: {vuln['Fixed']}, Severity: {vuln['Severity']}")
    else:
        print("No vulnerabilities found. The system is secure.")

