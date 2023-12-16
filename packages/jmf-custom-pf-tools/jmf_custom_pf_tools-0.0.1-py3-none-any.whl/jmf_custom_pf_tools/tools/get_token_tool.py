from promptflow import tool
from azure.identity import ClientSecretCredential
from promptflow.connections import CustomConnection

@tool
def get_token(conn:CustomConnection) -> str:
    credential = ClientSecretCredential(tenant_id=conn.tenant_id, 
                                        client_id=conn.client_id, 
                                        client_secret=conn.client_secret
    )
    jwt = credential.get_token("api://{}".format(conn.credential_scope))
    
    token = jwt.token

    return token
    