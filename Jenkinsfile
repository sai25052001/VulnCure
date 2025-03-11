pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/sai25052001/semi-colon.git'
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
                sh 'git config --global user.email "sai25052001@gmail.com"'
                sh 'git config --global user.name "sai25052001"'
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

