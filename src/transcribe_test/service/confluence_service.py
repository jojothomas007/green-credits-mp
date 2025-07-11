import json
import logging
import base64
import requests
from requests.auth import HTTPBasicAuth
from src.transcribe_test.dto.confluence_page_content_dto import ConfluencePageContent
from src.transcribe_test.dto.jira_user_dto import User
from src.transcribe_test.dto.jira_issue_dto import BulkIssues, Issue, IssueLink
from src.transcribe_test.config import Config
from src.transcribe_test.utils.request_sender import RequestSender
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

class ConfluenceService:
    def __init__(self):
        self.request_sender:RequestSender = RequestSender()
        self.confluence_api_url = f"{Config.confluence_api_url}/wiki/rest/api"
        self.jira_api_username = Config.jira_api_username
        self.jira_api_token = Config.jira_api_token
        self.auth = HTTPBasicAuth(self.jira_api_username, self.jira_api_token)
        self.headers = {
            "Accept": "application/json"
        }

    def is_valid_link(self, url:str) -> bool:
        return url.startswith(self.confluence_api_url.split("wiki")[0])

    def get_pageId_from_url(self, url:str) -> str:
        return url.split("/pages/")[1].split("/")[0]

    def get_page_content(self, page_id:str) -> requests.Response:
        request_url = f"{self.confluence_api_url}/content/{page_id}?expand=body.view"
        response = self.request_sender.get_request(request_url, self.headers, self.auth)
        return ConfluencePageContent.model_validate_json(response.content)