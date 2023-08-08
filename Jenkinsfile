pipeline{
    agent any

    environment {
        SSH_KEY = credentials('crypto-app')
        SSH_USER = 'ubuntu'
        TARGET_HOST = '172.31.3.156'
    }

    stages{
        stage('Checkout') {
            steps{
                checkout scm
            }
        }

        stage('Stop and Clean on Remote') {
            steps {
                script {
                    // Execute commands on the remote EC2 instance
                    sshCommand remote: [
                        host: TARGET_HOST,
                        user: SSH_USER,
                        key: SSH_KEY
                    ], command: '''
                        cd crypto-signals-project-cicd
                        docker-compose down
                        docker-compose rm -f
                        git pull origin main
                    '''
                }
            }
        }
        stage('Build and Run on Remote') {
            steps {
                script {
                    // Execute commands on the remote EC2 instance
                    sshCommand remote: [
                        host: TARGET_HOST,
                        user: SSH_USER,
                        key: SSH_KEY
                    ], command: '''
                        cd crypto-signals-project-cicd
                        docker-compose up -d
                    '''
                }
            }
        }
    }
}