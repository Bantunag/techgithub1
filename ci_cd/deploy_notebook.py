import os
import hvac
import requests

def get_vault_secret():
    """Retrieve Databricks credentials from Vault."""
    vault_url = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
    vault_token = os.getenv("VAULT_TOKEN")

    client = hvac.Client(url=vault_url, token=vault_token)

    if not client.is_authenticated():
        raise Exception("Vault authentication failed")

    secret_path = "secret/databricks-config"
    secret = client.secrets.kv.v2.read_secret_version(path=secret_path)
    return secret["data"]["data"]

def deploy_notebook(notebook_path):
    """Deploy a notebook to Azure Databricks."""
    credentials = get_vault_secret()
    databricks_host = credentials["host"]
    databricks_token = credentials["token"]

    # Define Databricks API URL
    url = f"{databricks_host}/api/2.0/workspace/import"

    with open(notebook_path, "r") as notebook_file:
        content = notebook_file.read()

    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {databricks_token}"},
        json={
            "path": f"/Shared/{os.path.basename(notebook_path)}",
            "overwrite": True,
            "format": "SOURCE",
            "content": content,
        },
    )

    if response.status_code == 200:
        print(f"Successfully deployed {notebook_path} to Databricks.")
    else:
        print(f"Failed to deploy {notebook_path}. Response: {response.text}")

if __name__ == "__main__":
    notebook_dir = "notebooks/"
    for notebook in os.listdir(notebook_dir):
        if notebook.endswith(".py"):
            deploy_notebook(os.path.join(notebook_dir, notebook))
