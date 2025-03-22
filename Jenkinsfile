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
        // Confirmation Stage
        stage('Approval Before fixing the CVEs') {
            steps {
                script {
                    def userInput = input message: 'Proceed with auto fixing the CVEs?', 
                                           ok: 'Yes', 
                                           parameters: [
                                               choice(name: 'approval', choices: ['Yes', 'No'], description: 'Select Yes to proceed or No to abort')
                                           ]
                    if (userInput == 'No') {
                        error('Pipeline aborted by user.')
                    }
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
                    cat post_autofix_message.txt >> parse_trivy_output.txt
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

                // Debug: Check if pom.xml actually changed
                sh 'git status'
                sh 'cat pom.xml | grep log4j-core'

                // Debug: Show updated pom.xml
                sh 'git status'
                sh 'cat pom.xml | grep log4j-core'

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

