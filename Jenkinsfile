pipeline {
    agent any

environment {
        AWS_ACCESS_KEY_ID = credentials('aws-key').accessKey
        AWS_SECRET_ACCESS_KEY = credentials('aws-key').secretKey
        ECR_REPOSITORY = '947437598996.dkr.ecr.us-east-1.amazonaws.com/signup-chart'
        DOCKER_TAG = 'latest'
        HELM_CHART_DIR = 'signup-chart'
    }

    // }
    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'git-key', url: 'https://github.com/nusairc/signup-argo.git']])
            }
        }

            
        stage('Docker Login and Build') {
            steps {
               withCredentials([usernamePassword(credentialsId: 'docker-key', passwordVariable: 'docker-pass', usernameVariable: 'docker-user')]) {
                    sh 'docker login -u %docker-user% -p %docker-pass%'
                    sh "docker build -t nusair/signup-image:${env.BUILD_NUMBER} . "
                    sh "docker push nusair/signup-image:${env.BUILD_NUMBER}"
                    sh 'docker logout'
                }
            }
        }


        stage('helmChart tag') {
            steps {
                sh "sed -i 's|nusair/signup-image:v1|${ECR_REPOSITORY}:${DOCKER_TAG}|g' $HELM_CHART_DIR/values.yaml"
            }
        }

        stage('helm package') {
            steps {
                sh "helm package $HELM_CHART_DIR"
            }
        }

        stage('Logging into AWS ECR & push helm chart to ECR') {
            steps {
                withAWS(credentials: 'aws-key', region: 'us-east-1') {
                    sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 947437598996.dkr.ecr.us-east-1.amazonaws.com"
                    sh "helm registry login -u AWS -p $$(aws ecr get-login-password --region us-east-1) 947437598996.dkr.ecr.us-east-1.amazonaws.com"
                    sh "helm push $HELM_CHART_DIR-0.1.0.tgz oci://947437598996.dkr.ecr.us-east-1.amazonaws.com"
                    sh "rm $HELM_CHART_DIR-0.1.0.tgz"
                }
            }
        }



        
        //  stage('pass buildnumber to another pipeline') {
        //     steps {
        //         build job: 'helm2-pipeline', parameters: [string(name: 'build_number', value: "${build_number}")]
        //     }
        // }
    }
}
