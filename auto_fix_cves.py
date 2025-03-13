import xml.etree.ElementTree as ET

POM_FILE = "pom.xml"

# Extract the highest fixed version from your Trivy scan results
FIXED_VERSIONS = ["2.15.0", "2.16.0", "2.17.0", "2.17.1"]  # Extracted from your scan
HIGHEST_FIXED_VERSION = max(FIXED_VERSIONS, key=lambda v: list(map(int, v.split('.'))))

def remove_xml_namespace(xml_string):
    """Removes unwanted XML namespaces from the given XML string."""
    return xml_string.replace('xmlns:ns0="http://maven.apache.org/POM/4.0.0"', '')

def update_pom():
    """Updates the log4j-core dependency version in pom.xml."""
    with open(POM_FILE, "r", encoding="utf-8") as f:
        xml_content = f.read()

    # Remove unwanted XML namespace
    cleaned_xml = remove_xml_namespace(xml_content)
    
    # Parse XML without namespace
    root = ET.fromstring(cleaned_xml)

    updated = False

    for dependency in root.findall(".//dependency"):
        group_id = dependency.find("groupId").text
        artifact_id = dependency.find("artifactId").text
        version = dependency.find("version")

        if group_id == "org.apache.logging.log4j" and artifact_id == "log4j-core":
            print(f"📌 Found log4j-core version: {version.text}")
            if version.text != HIGHEST_FIXED_VERSION:
                print(f"🚀 Updating log4j-core from {version.text} → {HIGHEST_FIXED_VERSION}")
                version.text = HIGHEST_FIXED_VERSION
                updated = True
            else:
                print("✅ log4j-core is already at the highest version.")

    if updated:
        # Convert XML back to string
        new_xml = ET.tostring(root, encoding="unicode")

        # Save changes to pom.xml
        with open(POM_FILE, "w", encoding="utf-8") as f:
            f.write(new_xml)

        print("✅ pom.xml updated successfully.")
    else:
        print("⚠️ No changes made to pom.xml.")

if __name__ == "__main__":
    update_pom()
