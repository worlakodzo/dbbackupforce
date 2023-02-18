let manageCredentialTypes = [];
let manageCredentials = [];
let databaseEngine = {};
let backUpStorageProvider = {};
let credentialCount = 0;
let credentialData = {};
const pageLoading =  `
<a class="btn btn" type="button" disabled>
<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Fetching data...
</a>
`
const savingData = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Saving...`;
const deletingData = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Deletings...`;



document.addEventListener("DOMContentLoaded", function(event){

    loadManageCredentialRecord();


    document.querySelector("#btn-add-new-credential").addEventListener("click", function(event){

        const divEl = document.createElement("div");
        divEl.setAttribute("class", "col-lg-12");
        divEl.setAttribute("data-form-id", credentialCount);
        divEl.setAttribute("id", `credential-form-container-${credentialCount}`);
        divEl.innerHTML = `

                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title"></h5>

                        <form id="credential-form-${credentialCount}" style="display: block;" data-form-id="${credentialCount}" class="form" action="#" data-method-type="POST" data-credential-id="" data-engine-or-storage-provider="">

                            <div class="col-12 other-info">
                                <label for="type-${credentialCount}" class="form-label"><strong>Type</strong> <span style="color: red;">*</span></label>
                                <select required id="type-${credentialCount}" data-form-id="${credentialCount}" class="form-select credential-type">
                                    <option value="" selected disabled>--please choose--</option>
                                    ${loadCredentialTypeIntoSelectedOption()}
                                </select>
                                <p id="type-${credentialCount}-error" style="color: red; display: none;">Type required</p>
                            </div>


                            <div class="col-12 other-info">
                                <label for="engine-or-storage-provider-${credentialCount}" id="engine-or-storage-provider-lb-${credentialCount}" class="form-label"><strong>Engine</strong> <span style="color: red;">*</span></label>
                                <select required id="engine-or-storage-provider-${credentialCount}" data-form-id="${credentialCount}" class="form-select">
                                    

                                </select>
                                <p id="engine-or-storage-provider-${credentialCount}-error" style="color: red; display: none;">Engine or Provider required</p>
                            </div>


                            <div id="form-${credentialCount}-content-detail">  




                            
                            </div>



                            <div>
                                <button style="float: right;" id="btn-save-credential-${credentialCount}" data-form-id="${credentialCount}"  type="submit" class="btn btn-primary">Save Changes</button>
                                <button style="float: right; margin-right: 5px;" type="button" id="btn-delete-credential-${credentialCount}" data-form-id="${credentialCount}" class="btn btn-danger">Delete</button>
                            </div>

                        </form>
                    </div>

                </div>
        `;
        


        document.getElementById("credentials-container").appendChild(divEl);

        // Add listener to credential type selected
        document.getElementById(`type-${credentialCount}`).addEventListener("change", function(event){
            const credentialType = this.value;
            const formId = this.getAttribute("data-form-id");
            const formContentDetailEl = document.getElementById(`form-${formId}-content-detail`).innerHTML = "";

            // Load engine or provider
            if (credentialType === "database_engines"){
                document.getElementById(`engine-or-storage-provider-${formId}`).innerHTML = loadEngineIntoSelectedOption();
                document.getElementById(`engine-or-storage-provider-lb-${formId}`).innerHTML = `<strong>Engine</strong> <span style="color: red;">*</span>`;
            } else if (credentialType === "storage_providers"){
                document.getElementById(`engine-or-storage-provider-${formId}`).innerHTML = loadStorageProviderIntoSelectedOption();
                document.getElementById(`engine-or-storage-provider-lb-${formId}`).innerHTML = `<strong>Provider</strong> <span style="color: red;">*</span>`;
            }

        });



        // Add listener to database engine or storage provider selected
        document.getElementById(`engine-or-storage-provider-${credentialCount}`).addEventListener("change", function(event){
            const engineOrStorageProvider = this.value;
            const formId = this.getAttribute("data-form-id");
            const formContentDetailEl = document.getElementById(`form-${formId}-content-detail`);
            document.getElementById(`credential-form-${formId}`).setAttribute("data-engine-or-storage-provider", engineOrStorageProvider);

            switch(engineOrStorageProvider) {

                case "mysql":
                    formContentDetailEl.innerHTML = loadDatabaseCredentialTemplate(formId);
                  break;
                case "postgresql":
                    formContentDetailEl.innerHTML = loadDatabaseCredentialTemplate(formId);
                  break;
                case "mariadb":
                    formContentDetailEl.innerHTML = loadDatabaseCredentialTemplate(formId);
                  break;
                case "sqlite":
                    formContentDetailEl.innerHTML = loadDatabaseCredentialTemplate(formId);
                  break;
                case "mongodb":
                    formContentDetailEl.innerHTML = loadDatabaseCredentialTemplate(formId);
                  break;
                case "elasticsearch":
                    formContentDetailEl.innerHTML = loadDatabaseCredentialTemplate(formId);
                  break;
                case "redis":
                    formContentDetailEl.innerHTML = loadDatabaseCredentialTemplate(formId);
                  break;
                case "memcached":
                    formContentDetailEl.innerHTML = loadDatabaseCredentialTemplate(formId);
                  break;
                case "aws":
                    formContentDetailEl.innerHTML = loadAWSStorageCredentialTemplate(formId);
                  break;
                case "azure":
                    formContentDetailEl.innerHTML = loadAWSStorageCredentialTemplate(formId);
                  break;
                case "gcp":
                    formContentDetailEl.innerHTML = loadAWSStorageCredentialTemplate(formId);
                  break;
                default:
                    console.log("error")
                  break;

              }



        });

        // Add listener to delete button
        document.getElementById(`btn-delete-credential-${credentialCount}`).addEventListener("click", function(event){
            const credentialType = this.value;
            const formId = this.getAttribute("data-form-id");
            document.getElementById(`credential-form-container-${formId}`).remove();
        });


        // Add listener to form
        document.getElementById(`credential-form-${credentialCount}`).addEventListener("submit", function(event){
            event.preventDefault();
            const engineOrStorageProvider = this.getAttribute("data-engine-or-storage-provider");
            const methodType = this.getAttribute("data-method-type");
            const credentialId = this.getAttribute("data-credential-id");
            const formId = this.getAttribute("data-form-id");
            
            saveCredential(engineOrStorageProvider, methodType, credentialId, formId);
        });


        // Increase count
        credentialCount += 1;
        


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


const loadManageCredentialRecord = () => {

    // Start spinner
    document.querySelector("#page-spinner").style.display = "none";

    fetch("/credentials", {
        method: "GET",
        headers: {"Content-Type": "application/json"}
    }).then(res => {

        if (res.status === 200){
           return res.json();
        }

    }).then(jsonData => {

        console.log(jsonData)
        // Get data
        manageCredentialTypes = jsonData.credential_types;
        manageCredentials = jsonData.credentials;

        for (let type_ of manageCredentialTypes){

            if (type_._id === "database_engines"){
                databaseEngine = type_;
            }else if (type_._id === "storage_providers"){
                backUpStorageProvider = type_;
            }
        }


    }).catch(error => {

        console.log(error.message);

    })
}


const loadDatabaseCredentialTemplate = (formId) => {

    return `

        <div  class="col-12 other-info">
            <label for="database-name-${formId}" class="form-label"><strong>Database name</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="database-name-${formId}">
            <p id="database-name-${formId}-error" style="color: red; display: none;">Database name required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="host-${formId}" class="form-label"><strong>Host</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="host-${formId}">
            <p id="host-${formId}-error" style="color: red; display: none;">Host required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="port-${formId}" class="form-label"><strong>Port</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="port-${formId}">
            <p id="port-${formId}-error" style="color: red; display: none;">Port required</p>
        </div>



        <div  class="col-12 other-info">
            <label for="username-${formId}" class="form-label"><strong>Username</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="username-${formId}">
            <p id="username-${formId}-error" style="color: red; display: none;">Username required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="password-${formId}" class="form-label"><strong>Password</strong><span style="color: red;">*</span></label>
            <input type="password" class="form-control" id="password-${formId}">
            <p id="password-${formId}-error" style="color: red; display: none;">Password name required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="identifier-${formId}" class="form-label"><strong>Credential identifier ID</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="credential-identifier-${formId}">
            <p id="credential-identifier-${formId}-error" style="color: red; display: none;">Credential identifier required</p>
        </div>
    
    `
}


const loadAWSStorageCredentialTemplate = (formId) => {

    return `

        <div  class="col-12 other-info">
            <label for="access-key-id-${formId}" class="form-label"><strong>Access key ID</strong><span style="color: red;">*</span></label>
            <input type="password" class="form-control" id="access-key-id-${formId}">
            <p id="access-key-id-${formId}-error" style="color: red; display: none;">Access key ID required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="secret-access-key-${formId}" class="form-label"><strong>Secret access key</strong><span style="color: red;">*</span></label>
            <input type="password" class="form-control" id="secret-access-key-${formId}">
            <p id="secret-access-key-${formId}-error" style="color: red; display: none;">Secret access key required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="region-${formId}" class="form-label"><strong>Region</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="region-${formId}">
            <p id="region-${formId}-error" style="color: red; display: none;">Region required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="bucket-name-${formId}" class="form-label"><strong>S3 Bucket name</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="bucket-name-${formId}">
            <p id="bucket-name-${formId}-error" style="color: red; display: none;">Bucket name required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="key-or-destination-${formId}" class="form-label"><strong>Key/Destination</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="key-or-destination-${formId}">
            <p id="key-or-destination-${formId}-error" style="color: red; display: none;">Key required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="credential-identifier-${formId}" class="form-label"><strong>Credential identifier ID</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="credential-identifier-${formId}">
            <p id="credential-identifier-${formId}-error" style="color: red; display: none;">Credential identifier required</p>
        </div>
    
    `
}

const validateInput = (engineOrStorageProvider, formId) => {

    let isValid = true;
    switch(engineOrStorageProvider) {
    
        case "mysql":
            isValid = validateDatabaseInput(formId);
          break;
        case "postgresql":
            isValid = validateDatabaseInput(formId);
          break;
        case "mariadb":
            isValid = validateDatabaseInput(formId);
          break;
        case "sqlite":
            isValid = validateDatabaseInput(formId);
          break;
        case "mongodb":
            isValid = validateDatabaseInput(formId);
          break;
        case "elasticsearch":
            isValid = validateDatabaseInput(formId);
          break;
        case "redis":
            isValid = validateDatabaseInput(formId);
          break;
        case "memcached":
            isValid = validateDatabaseInput(formId);
          break;
        case "aws":
            isValid = validateAWSStorageInput(formId);
          break;
        case "azure":
            isValid = validateAzureStorageInput(formId);
          break;
        case "gcp":
            isValid = validateGCPStorageInput(formId);
          break;
        default:
            console.log("error")
            isValid = true;
          break;

      }


      return isValid;

}

const validateDatabaseInput = (formId) => {
    let isValid = true;

    const databaseName = document.querySelector(`#database-name-${formId}`).value;
    const host = document.querySelector(`#host-${formId}`).value;
    const port = document.querySelector(`#port-${formId}`).value;
    const username = document.querySelector(`#username-${formId}`).value;
    const password = document.querySelector(`#password-${formId}`).value;
    const credentialId = document.querySelector(`#credential-identifier-${formId}`).value;
    const credentialType = document.querySelector(`#type-${formId}`).value;
    const engineOrStorageProvider = document.querySelector(`#engine-or-storage-provider-${formId}`).value;

    credentialData = {
        database_name: databaseName,
        database_host: host,
        database_port: port,
        database_user: username,
        database_password: password,
        credential_id: credentialId
    }


    if (credentialType === ""){
        document.getElementById(`type-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`type-${formId}-error`).style.display = "none";
    }

    if (engineOrStorageProvider === ""){
        document.getElementById(`engine-or-storage-provider-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`engine-or-storage-provider-${formId}-error`).style.display = "none";
    }


    if (databaseName === ""){
        document.getElementById(`database-name-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`database-name-${formId}-error`).style.display = "none";
    }

    if (host === ""){
        document.getElementById(`host-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`host-${formId}-error`).style.display = "none";
    }

    if (port === ""){
        document.getElementById(`port-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`port-${formId}-error`).style.display = "none";
    }

    if (username === ""){
        document.getElementById(`username-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`username-${formId}-error`).style.display = "none";
    }

    if (password === ""){
        document.getElementById(`password-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`password-${formId}-error`).style.display = "none";
    }

    if (credentialId === ""){
        document.getElementById(`credential-identifier-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`credential-identifier-${formId}-error`).style.display = "none";
    }

    return isValid;

}



const validateAWSStorageInput = (formId) => {
    let isValid = true;

    const accessKeyId = document.querySelector(`#access-key-id-${formId}`).value;
    const secretAccessKey = document.querySelector(`#secret-access-key-${formId}`).value;
    const region = document.querySelector(`#region-${formId}`).value;
    const bucketName = document.querySelector(`#bucket-name-${formId}`).value;
    const keyOrDestination = document.querySelector(`#key-or-destination-${formId}`).value;
    const credentialId = document.querySelector(`#credential-identifier-${formId}`).value;
    const credentialType = document.querySelector(`#type-${formId}`).value;
    const engineOrStorageProvider = document.querySelector(`#engine-or-storage-provider-${formId}`).value;

    credentialData = {
        access_key_id: accessKeyId,
        secret_access_key: secretAccessKey,
        region: region,
        bucket_name: bucketName,
        key_or_destination: keyOrDestination,
        credential_id: credentialId
    }


    if (accessKeyId === ""){
        document.getElementById(`access-key-id-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`access-key-id-${formId}-error`).style.display = "none";
    }

    if (secretAccessKey === ""){
        document.getElementById(`secret-access-key-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`secret-access-key-${formId}-error`).style.display = "none";
    }

    if (region === ""){
        document.getElementById(`region-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`region-${formId}-error`).style.display = "none";
    }

    if (bucketName === ""){
        document.getElementById(`bucket-name-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`bucket-name-${formId}-error`).style.display = "none";
    }

    if (keyOrDestination === ""){
        document.getElementById(`key-or-destination-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`key-or-destination-${formId}-error`).style.display = "none";
    }

    if (credentialId === ""){
        document.getElementById(`credential-identifier-${formId}-error`).style.display = "block";
        isValid = false;
    }else{
        document.getElementById(`credential-identifier-${formId}-error`).style.display = "none";
    }



    return isValid;

}



const validateAzureStorageInput = () => {



}

const validateGCPStorageInput = () => {



}


const saveCredential = (engineOrStorageProvider, methodType, credentialId, formId) => {
    const btnSaveEl = document.getElementById(`btn-save-credential-${formId}`);


    // Validate form input
    if (validateInput(engineOrStorageProvider, formId)){
        btnSaveEl.innerHTML = savingData;

        const credentialType = document.querySelector(`#type-${formId}`).value;
        const engineOrStorageProvider = document.querySelector(`#engine-or-storage-provider-${formId}`).value;
        const engineOrStorageProviderData = {}


        // Format url
        let url = `/credentials/${credentialId}`;
        if (methodType === "POST"){

            url = "/credentials";
            
            if (credentialType === "database_engines"){

                for (let engine of databaseEngine.engines){
                    engineOrStorageProvider = engine;
                }

            } else if (credentialType === "storage_providers"){

                for (let provider of backUpStorageProvider.providers){
                    engineOrStorageProvider = provider;
                }

            }

        }


        const data = {

            _id: credentialData.credential_id,
            type: credentialType,
            engine_or_storage_provider: engineOrStorageProviderData,
            credential: credentialData
        };


        console.log(data);


        // Save data
        fetch (url, {
            method: methodType,
            body: JSON.stringify(data),
            headers: {"Content-Type": "application/json"}
        }).then(res => {

            return res.json();

        }).then(jsonData => {

            if (jsonData.success){

                btnSaveEl.innerHTML = "Save Changes";
                $.notify("Credential Saved.", "success");
                
            }else{

                // error prompt here
                btnSaveEl.innerHTML = "Save Changes";
            }

        }).catch(err => {
            
            btnSaveEl.innerHTML = "Save Changes";
            console.log(err.message);

        });



    }

}