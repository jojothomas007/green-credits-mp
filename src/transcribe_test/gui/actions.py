import json
from src.transcribe_test.config import Config
from src.transcribe_test.service.jira_service import JiraService
from src.transcribe_test.service.translator import Translator
from transcribe_test.dto.jira_issue_dto import BulkIssueFields, Fields

class Action:
    def update_settings(self, api_url:str, api_username:str, api_token:str):
        json_config = {
                    "jira":{
                        "api_url":api_url,
                        "api_username":api_username,
                        "api_token":api_token,
                    }
                }
        Config.update_config(json_config)
        Config.load_config()

    def translate_jira_issue_description(self, issue_key:str):
        issue = JiraService().get_issue(issue_key)
        description:str = issue.fields.description
        trans_text:str = Translator.translate(description)
        new_description:str = f"{description} \n --------------------------------------------\n{trans_text}"
        payload:json = {
            "fields": {
                "description": new_description
            }
        }
        response = JiraService().update_issue(issue_key, payload)
        return
        