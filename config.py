from typing import Dict, Optional, Any
from pydantic import Field, RedisDsn, ValidationError
from pydantic_settings import BaseSettings
from azure.identity import DefaultAzureCredential
from redis import Redis

class NoCredentialsError(Exception):
    pass

class ServerConfig(BaseSettings):
    base_url: Optional[str] = Field(validation_alias='ponte_base_url', default="localhost")
    server_port: str = Field(validation_alias='ponte_port', default="8080")
    redis_dsn: Optional[RedisDsn] = Field(validation_alias='redis_connection_string', default=None)
    gh_app_id: str = Field(validation_alias='gh_app_id')
    gh_webhook_secret: str =  Field(validation_alias='gh_webhook_secret')
    gh_client_secret: str = Field(validation_alias="github_client_secret")

def generate_Credentials() -> Dict[str, Any]:
    try:
        credential = DefaultAzureCredential()
        config = ServerConfig().model_dump()
        redisClient = Redis.from_url(config['redis_dsn'])
        return {
            'azure': credential,
            'redis': redisClient
        }
 
    except Exception as e:
        print("Missing required environment variables")
        print(e)
        raise NoCredentialsError()
    
