pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/sai25052001/VulnCure.git'
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
        stage('Parse Trivy Report in txt file before scan') {
            steps {
                sh 'python3 parse_trivy.py > parse_trivy_output.txt'
            }
        }
        stage('Sending Reports through mail'){
            steps {
                withCredentials([
                   string(credentialsId: 'aws_access_key', variable: 'AWS_ACCESS_KEY_ID'), 
                   string(credentialsId: 'aws_secret_key', variable: 'AWS_SECRET_ACCESS_KEY')
                  ]) {
                sh '''
                export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                export AWS_DEFAULT_REGION=eu-north-1
                python3 message.py
                '''
                }
            }
        }
        stage('Approval') {
            steps {
                script {
                def userInput = input message: 'Please check mail. There you can see the list of reported CVEs. If you want to process, press Yes?', 
                            ok: 'Yes, Proceed'
                echo "Approval received. Proceeding with the pipeline."
                        }
                }
        }
        
        stage('auto fixing the CVEs') {
            steps {
                sh './update.sh'
            }
        }
        stage('Run Trivy Scan again to check the CVEs') {
            steps {
                sh 'trivy fs --format json --output trivy-report.json .'
            }
        }
        stage('Parse Trivy Report again to check CVEs') {
            steps {
                sh 'python3 parse_trivy.py'
            }
        }
        stage('Parse Trivy Report in txt file after scan') {
            steps {
                sh '''
                    python3 parse_trivy.py > parse_trivy_output.txt
                   '''
                  }
        }
        stage('Sending Reports through mail after fix'){
             steps {
                withCredentials([
                   string(credentialsId: 'aws_access_key', variable: 'AWS_ACCESS_KEY_ID'), 
                   string(credentialsId: 'aws_secret_key', variable: 'AWS_SECRET_ACCESS_KEY')
                  ]) {
                sh '''
                export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                export AWS_DEFAULT_REGION=eu-north-1
                python3 message.py
                '''
                }
            }
        }
        stage('Update new Dependencies in git') {
            steps {
                sh 'git config --global user.email "sai25052001@gmail.com"'
                sh 'git config --global user.name "sai25052001"'
    
                sh 'git status'
            
                // Add file only if it has changed
                sh 'git add pom.xml || true'

                // Commit only if there are staged changes
                sh 'git diff --staged --quiet || git commit -m "Auto-updated dependencies based on Trivy scan"'

                withCredentials([string(credentialsId: 'github-credentials', variable: 'GIT_TOKEN')]) {
                sh 'git push https://sai25052001:$GIT_TOKEN@github.com/sai25052001/semi-colon.git main'
                   }
                }
            }
    }
}

