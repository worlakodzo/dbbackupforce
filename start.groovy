def git = sh(script: 'git tag --sort=committerdate -l | tail -1', returnStdout: true).trim()
// def tags = git.readLines().collect { it.split()[1].split("/").last().strip() }

// if (tags){
//     tags = tags.sort {
//     def date = sh(script: "git log -1 --pretty=format:'%ct' ${it}", returnStdout: true).trim()
//     date.toLong()
//     }

// }

println("working")
println(git)
