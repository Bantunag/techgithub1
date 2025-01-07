import os
import base64
import requests

# Databricks configuration (hardcoded)
DATABRICKS_HOST = "https://adb-3988105243971966.6.azuredatabricks.net/"
DATABRICKS_TOKEN = "dapi8ff0ce1dbd98e5e131ee9b90f6851152-3"

def create_folder(folder_path):
    """
    Create a folder in the Databricks workspace if it doesn't exist.
    Args:
        folder_path (str): Path of the folder to create.
    """
    url = f"{DATABRICKS_HOST}/api/2.0/workspace/mkdirs"
    headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}
    data = {"path": folder_path}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Folder created or already exists: {folder_path}")
    else:
        print(f"Failed to create folder: {folder_path}. Error: {response.text}")

def upload_notebook(local_path, databricks_path):
    """
    Upload a notebook to Azure Databricks workspace.
    Args:
        local_path (str): Path to the local notebook file.
        databricks_path (str): Target Databricks workspace path.
    """
    # Ensure parent folders exist
    parent_folder = os.path.dirname(databricks_path)
    create_folder(parent_folder)

    # Read the file and encode its content in base64
    with open(local_path, 'rb') as file:
        content = base64.b64encode(file.read()).decode('utf-8')

    url = f"{DATABRICKS_HOST}/api/2.0/workspace/import"
    headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}
    data = {
        "path": databricks_path,
        "format": "SOURCE",  # Use SOURCE for Python files
        "language": "PYTHON",
        "content": content,
        "overwrite": True
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Notebook uploaded successfully: {local_path} -> {databricks_path}")
    else:
        print(f"Failed to upload notebook: {local_path}. Error: {response.text}")

def main():
    """
    Deploy notebooks from the local 'notebooks/' directory to Databricks.
    """
    local_notebooks_dir = "notebooks"
    databricks_base_path = "/Workspace/nagaraj"  # Adjust your base path here

    if not os.path.exists(local_notebooks_dir):
        print(f"Directory not found: {local_notebooks_dir}")
        return

    for root, _, files in os.walk(local_notebooks_dir):
        for file in files:
            if file.endswith(".py"):  # Only deploy Python files
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_notebooks_dir)
                databricks_path = f"{databricks_base_path}/{relative_path}"
                databricks_path = databricks_path.replace("\\", "/")  # Ensure UNIX-style paths
                upload_notebook(local_path, databricks_path)

if __name__ == "__main__":
    main()
