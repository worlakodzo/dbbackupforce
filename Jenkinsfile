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
        AWS_REGISTRY='644435390668.dkr.ecr.us-west-2.amazonaws.com'
    }


    stages {

        stage ("Checkout"){
            steps {
                script {

                    env.IMAGE_TAG = "1.0"
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
                    checkout scm


                    env.LAST_TAG = getLastVersionTag()
                    if (env.LAST_TAG == ""){
                        println("Tag is empty")
                    }else{
                        println("Tag is not empty")
                    }

                    // // Get new 3 number version
                    // env.NEW_TAG = getNextgetNext3NumberVersion("${env.LAST_TAG}")


                }
            }
        }


        stage ("Build") {

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
                        sh"""
                            pip3 install requests

                            cd ${WORKSPACE}
                            docker-compose -f docker-compose-e2etest.yaml up -d

                            # python3 e2e.py env.TEST_INSTANCE_PUBLIC_IP
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
        reposSource: [$class: "ManuallyEnteredRepositorySource", url: "$DEVELEAP_PORTFOLIO_PROJECT_URL"],
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
        script: "git ls-remote --tags origin  | awk '{print \$2}' | sed 's@refs/tags/@@'"
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


def getLastTag(){

    def tags = sh(script: 'git tag --sort=committerdate -l | tail -1', returnStdout: true).trim()

    // def git = "git"

    // def tags = sh(returnStdout: true, script: "git ls-remote --tags origin").readLines().collect {

    //     def tag = it.split()[1].replaceAll("refs/tags/", "")

    //     [tagName: tag, timestamp: sh(returnStdout: true, script: "git log -1 --format=%ct ${tag}").trim().toLong()]
    
    // }.sort { it.timestamp }

    // tags.each {
    //     echo "${it.tagName} - ${it.timestamp}"
    // }

    println(tags)

}