pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = "USERNAME ??"
        APP_NAME = "weather-app"
        WEATHER_API_KEY = credentials('a12d3e27079a99e8c4a20f4259279ced')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            agent {
                docker {
                    image 'python:3.9-slim'
                    reuseNode true
                }
            }
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            agent {
                docker {
                    image 'python:3.9-slim'
                    reuseNode true
                }
            }
            steps {
                sh 'python -m pytest tests/'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}")
                }
            }
        }
        
        stage('Push to Registry') {
            steps {
                withCredentials([string(credentialsId: 'docker-hub-password', variable: 'DOCKER_PASSWORD')]) {
                    sh "docker login -u ${DOCKER_REGISTRY} -p ${DOCKER_PASSWORD}"
                    sh "docker push ${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}"
                    sh "docker tag ${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER} ${DOCKER_REGISTRY}/${APP_NAME}:latest"
                    sh "docker push ${DOCKER_REGISTRY}/${APP_NAME}:latest"
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                sh """
                WEATHER_API_KEY=${WEATHER_API_KEY} \
                BUILD_NUMBER=${BUILD_NUMBER} \
                DOCKER_REGISTRY=${DOCKER_REGISTRY} \
                docker-compose -f docker-compose.staging.yml up -d
                """
            }
        }
    }
    
    post {
        always {
            sh "docker system prune -f"
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}