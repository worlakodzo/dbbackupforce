let manageCredentialTypes = [];
let manageCredentials = [];
let databaseEngine = {};
let backUpStorageProvider = {};
let credentialCount = 0;


document.addEventListener("DOMContentLoaded", function(event){

    loadManageCredentialRecord();


    document.querySelector("#btn-add-new-credential").addEventListener("click", function(event){

        const divEl = document.createElement("div");
        divEl.setAttribute("class", "col-lg-12")
        divEl.innerHTML = `

                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title"></h5>

                        <form id="credential-form-${credentialCount}" style="display: block;" data-form-id="${credentialCount}" class="form" action="#" data-method-type="POST" data-credential-id="">

                            <div class="col-12 other-info">
                                <label for="type-${credentialCount}" class="form-label"><strong>Type</strong> <span style="color: red;">*</span></label>
                                <select required id="type-${credentialCount}" data-form-id="${credentialCount}" class="form-select credential-type">
                                    <option value="0" selected disabled>--please choose--</option>
                                    ${loadCredentialTypeIntoSelectedOption()}
                                </select>
                                <p id="type-${credentialCount}-error" style="color: red; display: none;">Type required</p>
                            </div>


                            <div class="col-12 other-info">
                                <label for="engine-or-storage-provider-${credentialCount}" id="engine-or-storage-provider-lb-${credentialCount}" class="form-label"><strong>Engine</strong> <span style="color: red;">*</span></label>
                                <select required id="engine-or-storage-provider-${credentialCount}" data-form-id="${credentialCount}" class="form-select">
                                    

                                </select>
                                <p id="engine-${credentialCount}-error" style="color: red; display: none;">Engine required</p>
                            </div>


                            <div id="form-${credentialCount}-content-detail">  




                            
                            </div>



                            <div>
                                <button style="float: right;" id="btn-save-credential-${credentialCount}" disabled type="button" class="btn btn-primary">Save</button>
                                <button style="float: right; margin-right: 5px;" type="button" id="btn-delete-credential-${credentialCount}" class="btn btn-danger">Delete</button>
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
            <label for="database-name" class="form-label"><strong>Database name</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="database-name">
            <p id="database-name-error" style="color: red; display: none;">Database name required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="host" class="form-label"><strong>Host</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="host">
            <p id="host-error" style="color: red; display: none;">Host required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="port" class="form-label"><strong>Port</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="port">
            <p id="port-error" style="color: red; display: none;">Port required</p>
        </div>



        <div  class="col-12 other-info">
            <label for="username" class="form-label"><strong>Username</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="username">
            <p id="username-error" style="color: red; display: none;">Username required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="password" class="form-label"><strong>Password</strong><span style="color: red;">*</span></label>
            <input type="password" class="form-control" id="password">
            <p id="password-error" style="color: red; display: none;">Password name required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="identifier" class="form-label"><strong>Credential identifier ID</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="credential-identifier">
            <p id="identifier-error" style="color: red; display: none;">Credential identifier required</p>
        </div>
    
    `
}


const loadAWSStorageCredentialTemplate = (formId) => {

    return `

        <div  class="col-12 other-info">
            <label for="access-key-id" class="form-label"><strong>Access key ID</strong><span style="color: red;">*</span></label>
            <input type="password" class="form-control" id="access-key-id">
            <p id="access-key-id-error" style="color: red; display: none;">Access key ID required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="secret-access-key" class="form-label"><strong>Secret access key</strong><span style="color: red;">*</span></label>
            <input type="password" class="form-control" id="secret-access-key">
            <p id="secret-access-key-error" style="color: red; display: none;">Secret access key required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="region" class="form-label"><strong>Region</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="region">
            <p id="region-error" style="color: red; display: none;">Region required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="bucket-name" class="form-label"><strong>S3 Bucket name</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="bucket-name">
            <p id="bucket-name-error" style="color: red; display: none;">Bucket name required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="key-or-destination" class="form-label"><strong>Key/Destination</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="key-or-destination">
            <p id="key-or-destination-error" style="color: red; display: none;">Key required</p>
        </div>


        <div  class="col-12 other-info">
            <label for="identifier" class="form-label"><strong>Credential identifier ID</strong><span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="credential-identifier">
            <p id="identifier-error" style="color: red; display: none;">Credential identifier required</p>
        </div>
    
    `
}