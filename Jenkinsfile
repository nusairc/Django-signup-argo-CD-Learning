pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'git-key', url: 'https://github.com/nusairc/signup-argo.git']])
            }
        }
        
        stage('Docker Login and Build') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-keys', passwordVariable: 'docker_pswd', usernameVariable: 'docker_uname')]) {
                    sh "docker login -u $docker_uname -p $docker_pswd"
                    sh "docker build -t nusair/signup-image:${env.BUILD_NUMBER} . "
                    sh "docker push nusair/signup-image:${env.BUILD_NUMBER}"
                    sh "docker logout"
                }
            }
        }

        stage('helmChart tag') {
            steps {
                sh "sed -i 's|nusair/signup-image:v1|947437598996.dkr.ecr.us-east-1.amazonaws.com/signup-chart:${env.BUILD_NUMBER}|g' signup-chart/values.yaml"
            }
        }

        
        stage('helm package') {
            steps {
                sh "helm package signup-chart"
            }
        }
        
        stage('Logging into AWS ECR & push helm chart to ECR') {
            steps {
                withAWS(credentials: 'aws-key', region: 'us-east-1') {
                    sh '''
                        aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 947437598996.dkr.ecr.us-east-1.amazonaws.com
                        helm registry login -u AWS -p $(aws ecr get-login-password --region us-east-1) 947437598996.dkr.ecr.us-east-1.amazonaws.com
                        helm push signup-chart-0.1.0.tgz oci://947437598996.dkr.ecr.us-east-1.amazonaws.com
                        rm signup-chart-0.1.0.tgz
                    '''
                }
            }
        }
    }
}


