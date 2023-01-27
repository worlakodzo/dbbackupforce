document.addEventListener("DOMContentLoaded", function(event){









});






const loadUsers = () => {

    fetch('/users', {
        method: "GET",
        headers: {"Content-Type": "application/json"}
    }).then(res => {

        if (res.status == 200){
            // Convert data to json
            return res.json();
        }else{

        }


    }).then(res => {
        
    })

}


