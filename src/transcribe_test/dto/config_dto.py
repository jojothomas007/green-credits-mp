from pydantic import BaseModel, HttpUrl
from typing import Optional

class JiraConfig(BaseModel):
    api_url: str = ''
    api_username: str = ''
    api_token: str = ''

class ConfluenceConfig(BaseModel):
    api_url: str = ''

class AppConfig(BaseModel):
    jira: JiraConfig = JiraConfig()
    confluence: ConfluenceConfig = ConfluenceConfig()
