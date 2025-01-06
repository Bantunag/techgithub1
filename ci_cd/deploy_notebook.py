import subprocess
import sys
import hvac
import os

def get_vault_secrets():
    """Fetch Databricks credentials from HashiCorp Vault."""
    vault_url = "http://127.0.0.1:8200"  # Replace with your Vault server URL
    vault_token = os.environ.get("VAULT_TOKEN")  # Fetch token from environment variable
    if not vault_token:
        raise ValueError("Vault token is missing. Ensure VAULT_TOKEN is set in environment variables.")
    
    try:
        client = hvac.Client(url=vault_url, token=vault_token)
        # Retrieve secrets from Vault
        secret_path = "secret/databricks-config"  # Update with your Vault path
        secrets = client.secrets.kv.v2.read_secret_version(path=secret_path)["data"]["data"]
        return secrets["host"], secrets["token"]
    except Exception as e:
        print(f"Error fetching secrets from Vault: {e}")
        sys.exit(1)

def deploy_notebook(workspace_path, local_path):
    """Deploy a notebook to Databricks using the CLI."""
    # Get secrets from Vault
    databricks_host, databricks_token = get_vault_secrets()

    # Write Databricks config to file
    config_path = os.path.expanduser("~/.databrickscfg")
    try:
        with open(config_path, "w") as f:
            f.write("[DEFAULT]\n")
            f.write(f"host = {databricks_host}\n")
            f.write(f"token = {databricks_token}\n")
    except Exception as e:
        print(f"Error writing Databricks config: {e}")
        sys.exit(1)

    # Command to deploy the notebook
    command = [
        "databricks", "workspace", "import",
        "--overwrite", "--language", "PYTHON", local_path, workspace_path
    ]

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f"Successfully deployed notebook {local_path} to {workspace_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error deploying notebook: {e}")
        sys.exit(1)

if __name__ == "__main__":
    workspace_path = "/Workspace/bantu/my_notebook"
    local_path = "notebooks/my_notebook.py"
    deploy_notebook(workspace_path, local_path)
