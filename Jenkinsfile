pipeline{
    agent any

    stages {
        stage('Deploy New Version on Remote Instance') {
            steps {
                sshagent(credentials: ['52.15.78.148']) {
                    script {
                        def remoteInstance = 'ubuntu@172.31.20.192'
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
