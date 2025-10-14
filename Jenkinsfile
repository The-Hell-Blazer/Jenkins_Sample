pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building the project...'
                writeFile file: 'build.txt', text: 'This is a demo build artifact.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'echo "All tests passed!"'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh 'mkdir -p deploy'
                sh 'cp build.txt deploy/'
                echo 'Deployment complete!'
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}
