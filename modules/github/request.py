from datetime import datetime
from typing import Dict, Optional
import re
import jwt
from pydantic import Base64Str, BaseModel, HttpUrl, Json
import requests
from loguru import logger

class GithubContentResponse(BaseModel):
  type: str
  encoding: str
  size: int
  name: str
  path: str
  content: Base64Str 
  sha: str
  url: HttpUrl 
  git_url: HttpUrl 
  html_url: HttpUrl 
  download_url: HttpUrl
  _links: Dict[str, HttpUrl]

def get_installation_access_token(pem_filename: str, app_id: str, installation_id: str) -> str:
    
    now = int(datetime.now().timestamp())
    with open(pem_filename, "rb") as pem_file:
        signing_key = pem_file.read()
    payload = {"iat": now, "exp": now + 600, "iss": app_id}
    encoded_jwt = jwt.encode(payload, signing_key.decode("utf-8"), "RS256")

    response = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers={
            "Authorization": f"Bearer {encoded_jwt}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if not 200 <= response.status_code < 300:
        raise RuntimeError(
            "Unable to get token. Status code was "
            f"{response.status_code}, body was {response.text}."
        )

    return response.json()["token"]

def getPonteConfig(base_url: str, ref: Optional[str] = None) -> Json | None:
    pattern = r"\{\+path\}"

    if ref == None:
        ref = "main"
    
    ref_string = f"ref={ref}"
    file_name = "ponte.yaml"
    config_path = "?".join((file_name, ref_string))
    config_url: str = re.sub(pattern, config_path, base_url)

    headers = {
        'X-GitHub-Api-Version': "2022-11-28",
        'Accepjt': "application/vnd.github+json"
    }

    print(config_url)

    res = requests.get(
        url=config_url, 
        headers=headers
    )
    
    if res.status_code != 200:
        return None

    jsonbody= res.json()
    
    content_response: GithubContentResponse = GithubContentResponse.model_validate(jsonbody)
    print(content_response)

    return jsonbody 

if __name__ == "__main__":
    json = getPonteConfig("https://api.github.com/repos/migueltinembart/ponte-demo-repo/contents/{+path}")
    print(json)
