import os
from flask import Flask # type: ignore
from azure.identity import DefaultAzureCredential # type: ignore
from azure.keyvault.secrets import SecretClient # type: ignore

app = Flask(__name__)

# Replace with your actual Key Vault URL
KEY_VAULT_URL = "https://<your-keyvault-name>.vault.azure.net/"
SECRET_NAME = "DbConnectionString"

# Authenticate using Managed Identity
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

try:
    secret = client.get_secret(SECRET_NAME)
    db_conn_string = secret.value
except Exception as e:
    db_conn_string = f"Error retrieving secret: {str(e)}"

@app.route("/")
def home():
    return f"Database Connection String: {db_conn_string}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
