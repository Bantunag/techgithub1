import subprocess

def deploy_notebook(workspace_path, local_path, profile):
    command = [
        "databricks", "--profile", profile, "workspace", "import",
        "--overwrite", "--language", "PYTHON", local_path, workspace_path
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    deploy_notebook("/Workspace/Notebooks/my_notebook", "notebooks/my_notebook.py", "<profile-name>")
