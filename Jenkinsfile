pipeline {

    agent any

    options {
	    timestamps()
        timeout(time:15, unit:'MINUTES')
	}

    environment {
        COMPOSE_PROJECT_NAME="portfolio"
        DB_HOST="db"
        DB_NAME="develeap_portfolio"
        DB_PORT="27017"
        APP_NAME="uasset"
        REPOSITORY="uasset"
        REPOSITORY_HELM="uasset_helm"
        AWS_REGISTRY='644435390668.dkr.ecr.us-west-2.amazonaws.com'
    }


    stages {

        stage ("Checkout"){
            steps {
                script {

                    env.IMAGE_TAG = "1.0" // Initial/Default major and minor version

                    sh """
                        # Create .env file
                        echo COMPOSE_PROJECT_NAME=$COMPOSE_PROJECT_NAME >> .env
                        echo DB_HOST=$DB_HOST >> .env
                        echo DB_PORT=$DB_PORT >> .env
                        echo DB_NAME=$DB_NAME >> .env
                        echo DB_USERNAME=$DB_USERNAME >> .env
                        echo DB_PASSWORD=$DB_PASSWORD >> .env
                        echo DB_ROOT_USERNAME=$DB_ROOT_USERNAME >> .env
                        echo DB_ROOT_PASSWORD=$DB_ROOT_PASSWORD >> .env
                    """


                    // Checkout branch
                    // checkout scm
                    checkout([
                        $class: 'GitSCM',
                        branches: scm.branches,
                        doGenerateSubmoduleConfigurations: scm.doGenerateSubmoduleConfigurations,
                        extensions: scm.extensions + [[$class: 'CloneOption', noTags: false, reference: '', shallow: true]],
                        submoduleCfg: [],
                        userRemoteConfigs: scm.userRemoteConfigs
                    ])


                    // Get Tag git remote
                    env.LAST_TAG = getLastVersionTag()
                    if (env.LAST_TAG == ""){
                        println("Tag is empty")
                        env.LAST_TAG = env.IMAGE_TAG
                    }else{
                        println("Tag is not empty")
                    }

                    // Get new 3 number version
                    env.IMAGE_TAG = getNext3NumberVersion("${env.LAST_TAG}")
                    println("env.IMAGE_TAG: ${env.IMAGE_TAG}")


                }
            }
        }


        stage ("Build & Package") {

            when {
                anyOf {
                    branch "main"
                    branch "feature/*"
                }
            }
            steps {

                script {

                        println("Building  docker image")

                        sh """
                            cd ${WORKSPACE}/app

                            docker build -t $AWS_REGISTRY/$REPOSITORY:$IMAGE_TAG .

                            # add app image to env file
                            echo APP_IMAGE=$AWS_REGISTRY/$REPOSITORY:$IMAGE_TAG >> .env
                        """

                        // Update APP_IMAGE
                        env.APP_IMAGE="$AWS_REGISTRY/$REPOSITORY:$IMAGE_TAG"


                        // Package helm chart
                        sh"""
                            git clone ${PROJECT_GITOPS_REPO_URL}
                            
                            cd portfolio-gitops/manifest/
                            helm package  uasset --app-version ${IMAGE_TAG} --version ${IMAGE_TAG}
                        """


                    
                }
            }
        }

        stage ("UnitTest") {
            when {
                anyOf {
                    branch "main"
                    branch "feature/*"
                }
            }
            steps {

                script {

                        println("Unit testing application")
                        sh """
                            cd ${WORKSPACE}
                            docker-compose -f docker-compose-unittest.yaml  up -d

                            pip3 install requests
                            python3 ${WORKSPACE}/app/test/test_unittest.py



                            docker-compose -f docker-compose-unittest.yaml down -v --remove-orphans

                        """                   
                }
            }
        }

        stage ("Publish") {

            when {branch "main"}
            steps {


                script{

                   println('Pulishing docker image to elastic container registry...')
                   docker.withRegistry("https://$AWS_REGISTRY/$REPOSITORY", 'ecr:us-west-2:worlako-jenkins'){

                        // Tag and push images registry
                        build_app = docker.image("${APP_IMAGE}")
                        build_app.push("${IMAGE_TAG}")
                    
                    }

                   println('Pulishing application helm to elastic container registry...')
                    // Push Application Helm
                    sh"""
                        cd ${WORKSPACE}/portfolio-gitops/manifest/
                        aws ecr get-login-password --region us-west-2 | helm registry login --username AWS --password-stdin 644435390668.dkr.ecr.us-west-2.amazonaws.com
                        helm push uasset*.tgz oci://644435390668.dkr.ecr.us-west-2.amazonaws.com/
                    """


                   // Update application helm chart image tag
                   println('Update application helm chart image tag')
                   sh"""
                        cd ${WORKSPACE}/portfolio-gitops/manifest/uasset
                        sed -i "s/tag:.*/tag: ${IMAGE_TAG}/g" values.yaml

                        git add .
                        git commit -m "updated uasset image with ${IMAGE_TAG}"
                        git push
                    """


                }

            }

            
        }


        stage('E2E Test'){
            when {
                anyOf {
                    branch "main"
                    branch "feature/*"
                }
            }
            steps{
                script{
                        println("Running End to End Test")
                        sh"""
                            cd ${WORKSPACE}
                            docker-compose -f docker-compose-e2etest.yaml up -d

                            python3 ${WORKSPACE}/app/test/test_e2e_test.py


                        """
                }
            }
            
        }

        stage('Push Tag'){
            when {branch "main"}
            steps{
                script{
                        sh"""
                            cd ${WORKSPACE}
                            git clean -f
                            git config --global user.name "worlako-jenkin-pipeline"
                            git config --global user.email "worlako@jenkinpipeline.com"
                            git remote set-url origin ${PROJECT_REPO_URL}
                            git tag ${IMAGE_TAG} || echo "tag already exists."
                            git push origin --tags
                        """
                }
            }
            
        }
    }



    post {

        always {

            // Clean test enviroment
            sh """
                cd ${WORKSPACE}
                docker-compose -f docker-compose-unittest.yaml down -v --remove-orphans

                docker-compose -f docker-compose-e2etest.yaml  down -v --remove-orphans
            """

            

            // Clean workspace
            cleanWs()
        }
        

        success {
            setBuildStatus("Build succeeded", "SUCCESS");
        }
        failure {
            setBuildStatus("Build failed", "FAILURE");
        }

    }




}


void setBuildStatus(String message, String state) {

    step([
        $class: "GitHubCommitStatusSetter",
        reposSource: [$class: "ManuallyEnteredRepositorySource", url: "$PROJECT_GITOPS_REPO_URL"],
        // commitShaSource: [$class: "ManuallyEnteredShaSource", sha: commitSha],
        contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
        errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
        statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
    ]);


    
}

def formatTag(_3_number_version){
    return "v=${_3_number_version}"
}


def getNext3NumberVersion(tag){

    def vlist = tag.tokenize('.')

    if (vlist.size() == 3){

        // Split last version
        def (major, minor, patch) = vlist

        // Caculate new patch
        int new_patch = patch.toInteger() + 1

        // Format new 3 number version
        return "${major}.${minor}.${new_patch}"

    }else{

        // Format initial 3 number version
        return "${tag}.1"
    }

    return tag

}


def getMajorMinorVersion(release_branch) {

    // release/1.2
    def (branch, major_minor_version) = release_branch.tokenize("/")
    return major_minor_version
}


def getLastVersionTag(){

    def tagText = sh (
        returnStdout: true,
        script: "git ls-remote --tags ${PROJECT_REPO_URL}  | awk '{print \$2}' | sed 's@refs/tags/@@'"
        ).trim()

    // split tags
    def tags = tagText.tokenize("\n")
    println(tags)

    if (tags){

        // Return last tag
        def last_tags = tags[-1]
        return last_tags.replace("v=", "")
    }

    return ""
}