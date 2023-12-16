from promptflow import tool
from promptflow.connections import CustomConnection
from azure.identity import ClientSecretCredential
from openai import AzureOpenAI

def get_token(conn:CustomConnection) -> str:
    credential = ClientSecretCredential(tenant_id=conn.tenant_id, 
                                        client_id=conn.client_id, 
                                        client_secret=conn.client_secret
    )
    jwt = credential.get_token("api://{}".format(conn.credential_scope))
    
    token = jwt.token

    return token

@tool
def get_apim_openai_client(openai_conn: CustomConnection) -> AzureOpenAI:

    token = get_token(openai_conn)

    client = AzureOpenAI(
        api_key = token,  
        api_version = openai_conn.openai_api_version,
        azure_endpoint = openai_conn.openai_api_base
        )

    return client