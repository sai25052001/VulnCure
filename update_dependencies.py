import xml.etree.ElementTree as ET

def update_pom(pom_file, package, new_version):
    tree = ET.parse(pom_file)
    root = tree.getroot()
    ns = {'mvn': 'http://maven.apache.org/POM/4.0.0'}
    
    for dep in root.findall(".//mvn:dependency", ns):
        artifact = dep.find("mvn:artifactId", ns)
        if artifact is not None and artifact.text == package:
            version = dep.find("mvn:version", ns)
            if version is not None:
                version.text = new_version
                print(f"Updated {package} to {new_version}")
    
    tree.write(pom_file)

if __name__ == "__main__":
    update_pom("pom.xml", "org.apache.logging.log4j", "2.17.1")

