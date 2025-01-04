# ci_cd/deploy_notebook.py

import subprocess
import sys

def deploy_notebook(workspace_path, local_path, profile):
    """Deploy a notebook to Databricks using the CLI"""
    
    # Command to deploy the notebook to Databricks
    command = [
        "databricks", "workspace", "import",
        "--overwrite", "--language", "PYTHON", local_path, workspace_path
    ]
    
    # Execute the command and check for success
    try:
        subprocess.run(command, check=True)
        print(f"Successfully deployed notebook {local_path} to {workspace_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error deploying notebook: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Paths and profile
    workspace_path = "/Workspace/Users/raju.dileep23@gmail.com/my_notebook"  # Update your Databricks workspace path
    local_path = "notebooks/my_notebook.py"  # Local path to the notebook file
    profile = "databricks_profile"  # Databricks CLI profile (can be empty for default)

    # Call the deploy function
    deploy_notebook(workspace_path, local_path, profile)
