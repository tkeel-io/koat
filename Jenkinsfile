pipeline {
  agent {
    node {
      label 'python'
    }
  }

    environment {
        /*
        tips:app env
        */
        APP_NAME = 'koat'
        DOCKERFILES_PATH = 'Dockerfile'
        
        /*
        CREDENTIAL
        */
        PRIVATE_REPO_CREDENTIAL_ID = 'harbor'

        /*
        config form CREDENTIAL
        */
        PRIVATE_REPO_CONFIG = 'private-repo'
    }

    stages {
        stage ('checkout scm') {
            steps {
                checkout(scm)
            }
        }

        stage('get config'){
            /*
            get form CREDENTIAL
            */
            steps {
                container ('python'){
                    withCredentials([usernamePassword(credentialsId: "$PRIVATE_REPO_CONFIG", usernameVariable: 'registry',passwordVariable: 'repository')]) {
                        script {
                            env.REGISTRY = registry
                            env.REPOSITORY = repository
                            }
                        }

                    withCredentials([usernamePassword(credentialsId: "$PRIVATE_REPO_CREDENTIAL_ID", usernameVariable: 'username',passwordVariable: 'password')]) {
                        script {
                            env.USERNAME = username
                            env.PASSWORD = password
                            }
                        }
                    }
                }
            }

        stage('build & push') {
            steps {
                container ('python') {
                    script{
                        /*
                        build docker image
                        */
                        sh 'docker login -u $USERNAME -p $PASSWORD https://$REGISTRY'
                        sh 'docker build -f $DOCKERFILES_PATH -t $REGISTRY/$REPOSITORY/$APP_NAME:latest .'
                        sh 'docker push $REGISTRY/$REPOSITORY/$APP_NAME:latest'
                    }
                }
            }
        }
    }
}