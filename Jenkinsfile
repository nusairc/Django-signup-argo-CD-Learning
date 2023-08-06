pipeline {
    agent any
    // environment {
    //     build_number = "${env.BUILD_ID}"
    //     AWS_ACCOUNT_ID="947437598996"
    //     AWS_DEFAULT_REGION="us-east-1"
    //     IMAGE_REPO_NAME="signup-chart"
    //     IMAGE_TAG="latest"
    //     REPOSITORY_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}"
    // }
    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'git-key', url: 'https://github.com/nusairc/signup-helm.git']])
            }
        }
        stage('Python Build') {
            steps {
                dir('./registration'){    
                 bat 'python settings.py build'
                }
            }}

       stage('Unit Test') {
            steps {
                dir('./registration/app1') {
                    bat 'python ../../manage.py test'
                }
            }
        }

            
        stage('Docker Login and Build') {
            steps {
                withCredentials([string(credentialsId: 'nusair', variable: 'docker-var')]) {
                    bat 'docker login -u nusair -p %docker-var%'
                    bat "docker build -t nusair/signup-image:${env.BUILD_NUMBER} . "
                    bat "docker push nusair/signup-image:${env.BUILD_NUMBER}"
                    bat 'docker logout'
                }
            }
        }


        stage('helmChart tag') {
            steps {
                // bat "sed -i 's|nusair/signup-image:v1|nusair/signup-image:${env.BUILD_NUMBER}|g' ./signup-chart/values.yaml"
                bat """
                powershell.exe -Command "((Get-Content -Path './signup-chart/values.yaml') -replace 'nusair/signup-image:v1', 'nusair/signup-image:${env.BUILD_NUMBER}') | Set-Content -Path './signup-chart/values.yaml'"
                """
            }
        }
        
        stage('helm package ') {
            steps {
                bat "\"C:\\Program Files\\windows-amd64\\helm\" package E:\\Signup-pro\\registration\\signup-chart"
                // bat 'wsl /usr/local/bin/helm package signup-chart
                // bat 'wsl helm package signup-chart'
                // bat 'wsl sudo helm package signup-chart'
                
            }
        }

        stage('Logging into AWS ECR & push helm chart to ECR') {
            steps {
                withCredentials([aws(credentialsId: 'aws-key', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        bat '"C:\\Program Files\\Amazon\\AWSCLIV2\\aws" ecr get-login-password --region us-east-1 | "C:\\Program Files\\windows-amd64\\helm" registry login --username AWS --password-stdin 947437598996.dkr.ecr.us-east-1.amazonaws.com'
                        bat "\"C:\\Program Files\\windows-amd64\\helm\" push signup-chart-0.1.0.tgz oci://947437598996.dkr.ecr.us-east-1.amazonaws.com"
                        bat "del signup-chart-0.1.0.tgz"
                    }
                }
            }
        }

        
         stage('pass buildnumber to another pipeline') {
            steps {
                build job: 'helm2-pipeline', parameters: [string(name: 'build_number', value: "${build_number}")]
            }
        }
    }
}
