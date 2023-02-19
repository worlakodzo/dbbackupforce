let durationIntervals = [];
let manageCredentials = [];
let databaseEngine = {};
let jobData = {};
const pageLoading =  `
<a class="btn btn" type="button" disabled>
<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Fetching data...
</a>
`
const savingData = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Saving...`;
const deletingData = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Deleting...`;



document.addEventListener("DOMContentLoaded", function(event){

    loadBasicInfo();

    // Add listener to form
    document.getElementById(`job-form`).addEventListener("submit", function(event){
        event.preventDefault();
        const methodType = this.getAttribute("data-method-type");
        const jobId = this.getAttribute("data-job-id");
        saveJob(methodType, jobId);
    });



});




const loadCredentialTypeIntoSelectedOption = () => {
    let content = "";

    for (let type_ of manageCredentialTypes){
        content += `<option value="${type_._id}">${type_.name}</option>`;
    }

    return content;
}

const loadStorageProviderIntoSelectedOption = () => {
    let content = `<option value="0" selected disabled>--please choose--</option>`;

    for (let provider of backUpStorageProvider.providers){
        content += `<option value="${provider._id}">${provider.name}</option>`;
    }

    return content;
}

const loadEngineIntoSelectedOption = () => {
    let content = `<option value="0" selected disabled>--please choose--</option>`;

    for (let engine of databaseEngine.engines){
        content += `<option value="${engine._id}">${engine.name}</option>`;
    }

    return content;
}


const loadBasicInfo = () => {

    // Start spinner
    document.querySelector("#page-spinner").style.display = "block";
    document.querySelector("#job-form").style.display = "none";

    fetch("/jobbasicinfo", {
        method: "GET",
        headers: {"Content-Type": "application/json"}
    }).then(res => {

        if (res.status === 200){
           return res.json();
        }

    }).then(jsonData => {

        console.log(jsonData)
        let optionContent = "";

        // Get data
        durationIntervals = jsonData.duration_interval_types;
        manageCredentials = jsonData.credentials;
        console.log(durationIntervals)

        // load database credential ID
        optionContent = '<option value="" selected disabled>--please choose--</option>';
        for (let interval of durationIntervals){
            optionContent += `<option value="${interval._id}">${interval.name}</option>`;
        }
        document.getElementById("interval-type").innerHTML = optionContent
        


        // load database credential ID
        optionContent = '<option value="" selected disabled>--please choose--</option>';
        for (let credentialData of manageCredentials){
            if (credentialData.type === "database_engines"){
                optionContent += `<option value="${credentialData._id}">${credentialData.engine_or_storage_provider.name} => ${credentialData._id}</option>`;
            }
        }
        document.getElementById("database-credential-id").innerHTML = optionContent




        // load backup storage provider credential ID
        optionContent = '<option value="" selected disabled>--please choose--</option>';
        optionContent += `<option value="default">Default</option>`;
        for (let credentialData of manageCredentials){
            if (credentialData.type === "storage_providers"){
                optionContent += `<option value="${credentialData._id}">${credentialData.engine_or_storage_provider.name} => ${credentialData._id}</option>`;
            }
        }
        document.getElementById("backup-storage-provider-credential-id").innerHTML = optionContent


        // Update  
        document.querySelector("#page-spinner").style.display = "none";
        document.querySelector("#job-form").style.display = "block";



    }).catch(error => {

        console.log(error.message);

    })
}


const validateInput = () => {
    let isValid = true;


    const jobName = document.querySelector(`#job-name`).value;
    const description = document.querySelector(`#description`).value;
    const enableAutomaticBackedUp = document.querySelector(`#enable-automatic-backed-up`).checked;
    const jobStartTime = document.querySelector(`#job-start-time`).value;
    const intervalType = document.querySelector(`#interval-type`).value;
    const intervalValue = document.querySelector(`#interval-value`).value;
    const databaseCredentialId = document.querySelector(`#database-credential-id`).value;
    const backupStorageProviderCredentialId = document.querySelector(`#backup-storage-provider-credential-id`);


    console.log(jobStartTime);


    // form data
    jobData = {
        job_name: jobName,
        description: description,
        enable_automatic_backed_up: enableAutomaticBackedUp,
        job_start_time: jobStartTime,
        interval_type: intervalType,
        interval_value: intervalValue,
        database_credential_id: databaseCredentialId,
        backup_storage_provider_credential_id: backupStorageProviderCredentialId,
    }


    if (jobName === ""){
        document.getElementById(`job-name-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`job-name-error`).style.display = "none";
    }

    if (description === ""){
        document.getElementById(`description`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`description`).style.display = "none";
    }


    if (jobStartTime === ""){
        document.getElementById(`job-start-time-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`job-start-time-error`).style.display = "none";
    }

    if (intervalType === ""){
        document.getElementById(`interval-type-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`interval-type-error`).style.display = "none";
    }

    if (intervalValue === ""){
        document.getElementById(`interval-value-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`interval-value-error`).style.display = "none";
    }

    if (databaseCredentialId === ""){
        document.getElementById(`database-credential-id-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`database-credential-id-error`).style.display = "none";
    }

    if (backupStorageProviderCredentialId === ""){
        document.getElementById(`backup-storage-provider-credential-id-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`backup-storage-provider-credential-id-error`).style.display = "none";
    }

    return isValid;

}


const saveJob = (methodType, jobId) => {
    const btnSaveEl = document.getElementById(`btn-save-job`);


    // Validate form input
    if (validateInput()){

        btnSaveEl.innerHTML = savingData;
        const errorContainerEl = document.querySelector(`#error-container`);
        const errorEl = document.querySelector(`#error-content`);
        errorContainerEl.style.display = "none";

        
        let url = `/jobs/${jobId}`;
        let data = {};

        if (methodType === "POST"){

            url = "/jobs";

            // format data
            data = jobData;


        }else {

            // format data
            data = jobData
        }





        // Save data
        fetch (url, {
            method: methodType,
            body: JSON.stringify(data),
            headers: {"Content-Type": "application/json"}
        }).then(res => {

            return res.json();

        }).then(jsonData => {

            console.log(jsonData)

            if (jsonData.success){


                btnSaveEl.innerHTML = "Save";
                $.notify("Credential Saved.", "success");
                window.location.href = "/job_list";

            }else{

                // error prompt here
                errorEl.innerHTML = jsonData.message
                errorContainerEl.style.display = "block";
                btnSaveEl.innerHTML = "Save";
            }

        }).catch(err => {
            
            btnSaveEl.innerHTML = "Save";
            console.log(err.message);
            errorEl.innerHTML = err.message;
            errorContainerEl.style.display = "block";

        });



    }

}


const displaySavedJob = (formId, credential, performReplace=false) => {


    const divEl = document.createElement("div");
    divEl.setAttribute("class", "col-lg-12");
    divEl.setAttribute("data-form-id", formId);
    divEl.setAttribute("id", `credential-form-container-${formId}`);
    divEl.setAttribute("data-engine-or-storage-provider-name", credential.engine_or_storage_provider.name);

    console.log(credential)
    divEl.innerHTML = `

            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${credential.engine_or_storage_provider.name}</h5>

                    <form id="credential-form-${formId}" style="display: block;" data-form-id="${formId}" class="form" action="#" data-method-type="PUT" data-credential-id="${credential._id}" data-engine-or-storage-provider="${credential.engine_or_storage_provider._id}">

                        <div class="col-12 other-info">
                            <img height="120" src="/static/img/${credential.engine_or_storage_provider.image}" />
                        </div>





                        <div id="form-${formId}-content-detail">  




                        
                        </div>



                        <div>
                            <button style="float: right;" id="btn-save-credential-${formId}" data-form-id="${formId}" data-credential-id="${credential._id}"  type="submit" class="btn btn-primary">Save Changes</button>
                            <button style="float: right; margin-right: 5px;" type="button" id="btn-delete-credential-${formId}" data-form-id="${formId}" data-credential-id="${credential._id}" data-bs-toggle="modal" data-bs-target="#delete-credential-modal" class="btn btn-danger">Delete</button>
                        </div>

                    </form>


                    <div id="error-container-${formId}" style="display: none; margin-top:20px;" class="alert alert-danger alert-dismissible fade show" role="alert">
                        <p id="error-p-${formId}" ></p>
                    </div>

                </div>

            </div>
    `;


    if (performReplace){
        // get handle to element to replace
        const oldChild = document.querySelector(`#credential-form-container-${formId}`);
        
        // get handle to the parent node
        const parentNode = oldChild.parentNode;
        
        parentNode.replaceChild(divEl, oldChild);
    }else{
        document.getElementById("credentials-container").appendChild(divEl);    
    }




    loadFormFields(credential.engine_or_storage_provider._id, formId, credential.credential, true);




    // Add listener to form
    document.getElementById(`credential-form-${formId}`).addEventListener("submit", function(event){
        event.preventDefault();
        const engineOrStorageProvider = this.getAttribute("data-engine-or-storage-provider");
        const methodType = this.getAttribute("data-method-type");
        const credentialId = this.getAttribute("data-credential-id");
        const formId = this.getAttribute("data-form-id");
        
        saveCredential(engineOrStorageProvider, methodType, credentialId, formId);
    });



    // Add listener to delete button
    document.getElementById(`btn-delete-credential-${formId}`).addEventListener("click", function(event){

        const formId = this.getAttribute("data-form-id");
        const credentialId = this.getAttribute("data-credential-id");
    
        const credentialFormContainer = document.getElementById(`credential-form-container-${formId}`)
        const engineOrStorageProviderName = credentialFormContainer.getAttribute("data-engine-or-storage-provider-name");

        
        const content = `<p>Are you sure, you want to delete the selected ${engineOrStorageProviderName} credentials with ID (${credentialId})</p>`;
        document.getElementById("delete-body-modal").innerHTML=`${content}`;

        const deleteBtnEl = document.getElementById("confirm-delete");
        deleteBtnEl.setAttribute("data-credential-id", credentialId);
        deleteBtnEl.setAttribute("data-form-id", formId);

    });



}




