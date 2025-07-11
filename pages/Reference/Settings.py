import streamlit as st

from src.transcribe_test.config import Config
from src.transcribe_test.dto.config_dto import AppConfig, ConfluenceConfig, JiraConfig

def fetch_issue():
    app_config = AppConfig(
        jira=JiraConfig(
            api_url=st.session_state.jira_api_url, 
            api_username=st.session_state.jira_api_username, 
            api_token=st.session_state.jira_api_token), 
        confluence=ConfluenceConfig (
            api_url=st.session_state.confluence_api_url))
    Config.update_config(app_config)
    
st.set_page_config(
    page_title="Settings",
    page_icon="🙌"
)

st.header('🙌 Settings')

Config.load_config()

st.session_state.confluence_api_url = st.text_input("Confluence base url:", Config.confluence_api_url)
st.session_state.jira_api_url = st.text_input("Jira base url:", Config.jira_api_url)
st.session_state.jira_api_username = st.text_input("Jira username:", Config.jira_api_username)
st.session_state.jira_api_token = st.text_input("Jira API token:", Config.jira_api_token)

st.button("Save", on_click=fetch_issue)
