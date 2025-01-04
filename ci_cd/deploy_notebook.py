import subprocess

def deploy_notebook(workspace_path, local_path, profile):
    command = [
        "databricks", "--profile", profile, "workspace", "import",
        "--overwrite", "--language", "PYTHON", local_path, workspace_path
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    # Modify these paths as needed
    workspace_path = "/Workspace/Users/raju.dileep23@gmail.com/my_notebook"  # Correct path in Databricks workspace
    local_path = "notebooks/my_notebook.py"  # Local path to your notebook file
    profile = "<profile-name>"  # Your Databricks profile name

    deploy_notebook(workspace_path, local_path, profile)
