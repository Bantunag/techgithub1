import hvac
import subprocess

def get_vault_secrets():
    """Fetch Databricks credentials from HashiCorp Vault."""
    vault_url = "http://127.0.0.1:8200"  # Replace with your Vault URL
    vault_token = os.environ.get("VAULT_TOKEN")  # Fetch token from environment variable
    if not vault_token:
        raise ValueError("Vault token not found in environment variables. Ensure VAULT_TOKEN is set.")

    client = hvac.Client(url=vault_url, token=vault_token)

    # Retrieve secrets from Vault
    secret_path = "secret/databricks-config"
    secrets = client.secrets.kv.v2.read_secret_version(path=secret_path)["data"]["data"]
    return secrets["host"], secrets["token"]

def deploy_notebook(databricks_workspace_path, notebook_local_path):
    """Deploy a notebook to Databricks."""
    host, token = get_vault_secrets()
    command = [
        "databricks",
        "--host", host,
        "--token", token,
        "workspace",
        "import",
        "--overwrite",
        "--language", "PYTHON",
        notebook_local_path,
        databricks_workspace_path
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    deploy_notebook(
        "/Workspace/bantu/my_notebook",
        "notebooks/my_notebook.py"
    )
