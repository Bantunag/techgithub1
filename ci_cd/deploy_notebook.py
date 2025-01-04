import subprocess
import os

def deploy_notebook(workspace_path, local_path, profile):
    # Ensure the environment variables are set properly for the Databricks CLI to use
    os.environ['DATABRICKS_HOST'] = os.getenv('DATABRICKS_HOST')
    os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')

    command = [
        "databricks", "--profile", profile, "workspace", "import",
        "--overwrite", "--language", "PYTHON", local_path, workspace_path
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    # Replace '<profile-name>' with the actual profile name (e.g., 'databricks_profile')
    deploy_notebook("/Workspace/Users/raju.dileep23@gmail.com/my_notebook", "notebooks/my_notebook.py", "databricks_profile")
