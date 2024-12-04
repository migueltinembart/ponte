from typing import Optional
from pydantic import Field, RedisDsn, ValidationError
from pydantic_settings import BaseSettings

class ServerConfig(BaseSettings):
    base_url: Optional[str] = Field(validation_alias='ponte_base_url', default="localhost")
    server_port: str = Field(validation_alias='ponte_port', default="8080")
    redis_dsn: Optional[RedisDsn] = Field(validation_alias='redis_connection_string', default=None)
    gh_app_id: str = Field(validation_alias='github_app_id')
    gh_webhook_secret: str =  Field(validation_alias='github_webhook_secret')
    gh_private_key: str = Field(validation_alias="github_private_key")

    azure_subscription_id: Optional[str] = Field(validation_alias="azure_subscription_id")
    azure_tenant_id: Optional[str] = Field(validation_alias="azure_tenant_id")
    azure_client_id: Optional[str] = Field(validation_alias="azure_client_id")
    azure_client_secret: Optional[str] = Field(validation_alias="azure_client_secret")

def loadEnv():
    try:
        ServerConfig().model_dump()
    except ValidationError as e:
        print("Missing required environment variables")
        print(e)
        exit(1)

if __name__ == "__main__":
    loadEnv()
