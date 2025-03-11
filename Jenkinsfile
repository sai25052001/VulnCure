pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-repository/java-project.git'
            }
        }
        stage('Build Java Project') {
            steps {
                sh 'mvn clean package'
            }
        }
        stage('Run Trivy Scan') {
            steps {
                sh 'trivy fs --format json --output trivy-report.json .'
            }
        }
        stage('Parse Trivy Report') {
            steps {
                sh 'python3 parse_trivy.py'
            }
        }
        stage('Update Dependencies') {
            steps {
                sh 'python3 update_dependencies.py'
                sh 'git config --global user.email "jenkins@example.com"'
                sh 'git config --global user.name "Jenkins"'
                sh 'git add pom.xml'
                sh 'git commit -m "Auto-updated dependencies based on Trivy scan"'
                sh 'git push origin main'
            }
        }
        stage('Deploy & Test') {
            steps {
                sh 'mvn test'
                sh 'mvn verify'
            }
        }
    }
}

