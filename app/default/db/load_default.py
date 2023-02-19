import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def load_default_manage_credential_type(db):

    credential_types_json = []

    with open(f"{BASE_DIR}/db/manage-credentials-type.json", "r") as file:
          file_contents = file.read()
          credential_types_json = json.loads(file_contents)

    for value in credential_types_json:
        type_ = db.manage_credential_types.find({"_id":value['_id']})

        if not type_:
            db.manage_credential_types.insert_one(value)
