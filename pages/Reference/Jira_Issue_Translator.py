import streamlit as st

from src.transcribe_test.dto.jira_issue_dto import Issue
from src.transcribe_test.service.jira_service import JiraService
from src.transcribe_test.service.translator import Translator
from src.transcribe_test.config import Config

def fetch_issue():
    issue:Issue = None
    st.session_state.issue = JiraService().get_issue(issue_key)
    st.session_state.description = st.session_state.issue.fields.description
    st.session_state.step = 1  # Move to the "fetch" step

def translate():
    st.session_state.trans_text = Translator.translate(st.session_state.description)
    st.session_state.step = 2  # Move to the "translate" step

def update_jira_issue():
    st.session_state.issue.fields.description = f'''{st.session_state.issue.fields.description} 
    --------------------------------------------------------------------------------------------
    {st.session_state.trans_text}'''
    JiraService().update_issue_description(st.session_state.issue.key, st.session_state.issue.fields.description)
    st.session_state.step = 3  # Move to the "update" step

def reset_state():
    st.session_state.step = 0  # Move to the "Reset" step

st.set_page_config(
    page_title="Jira Issue Translator",
    page_icon="📚"
)

st.header('📚 Jira Issue Translator')
st.subheader('Translates text from Jira Issue description.')
st.button("Reset", on_click=reset_state)

if "description" not in st.session_state:
    st.session_state.description = ""
if "trans_text" not in st.session_state:
    st.session_state.trans_text = ""
if "step" not in st.session_state:
    st.session_state.step = 0 # Tracks the current step (0: initial, 1: fetched, 2: translated)

issue_key = st.text_input("Jira Issue key for Translation:", disabled=(st.session_state.step >= 1))
Config.load_config()
# Fetch Jira issue details
st.button("Fetch", disabled=(st.session_state.step >= 1), on_click=fetch_issue)
    

# Display text area and Translate button if Fetch is clicked
if st.session_state.step >= 1:
    st.text_area("Jira Issue Description : ", st.session_state.description, 250, disabled=True)
    st.button("Translate", disabled=(st.session_state.step >= 2), on_click=translate)


# Display translated text area and Update button if Translate is clicked
if st.session_state.step >= 2:
    st.session_state.trans_text = st.text_area("Translated Jira Issue Description : ", st.session_state.trans_text, 250, disabled=(st.session_state.step >= 3))
    if st.button("Update", disabled=(st.session_state.step >= 3), on_click=update_jira_issue):
        st.success(f"Jira Issue updated!")



