pipeline{
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/shariqazeem/crypto-signals-project-cicd.git'
            }
        }

        stage('Deploy New Version on Remote Instance') {
            steps {
                sshagent(credentials: ['crypto-app']) {
                    script {
                        def remoteInstance = 'ubuntu@52.15.78.148'
                        def projectDirectory = 'crypto-signals-project-cicd'
                        def dockerComposePath = "${projectDirectory}/docker-compose.yml"

                        sh "ssh -o StrictHostKeyChecking=no ${remoteInstance} 'cd ${projectDirectory} && docker-compose down'"
                        sh "ssh -o StrictHostKeyChecking=no ${remoteInstance} 'cd ${projectDirectory} && docker-compose rm -f'"
                        sh "ssh -o StrictHostKeyChecking=no ${remoteInstance} 'cd ${projectDirectory} && git pull origin main'"
                        sh "ssh -o StrictHostKeyChecking=no ${remoteInstance} 'cd ${projectDirectory} && docker-compose up -d'"
                    }
                }
            }
        }
    }
}
