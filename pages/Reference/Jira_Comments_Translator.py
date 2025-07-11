import streamlit as st

from src.transcribe_test.dto.jira_issue_dto import Issue
from src.transcribe_test.service.jira_service import JiraService
from src.transcribe_test.service.translator import Translator
from src.transcribe_test.config import Config

def fetch_issue():
    st.session_state.comments = JiraService().get_comments(issue_key)

def reset_state():
    st.session_state.comments = ""

st.set_page_config(
    page_title="Jira Comments Translator",
    page_icon="📚"
)

st.header('📚 Jira Comments Translator')
st.subheader('Translates text from Jira Issue comments.')
st.button("Reset", on_click=reset_state)
issue_key = st.text_input("Jira Issue key for Translation:")
Config.load_config()
# Fetch Jira issue details
st.button("Fetch", on_click=fetch_issue)
if(st.session_state.comments != ''):
    for comment in st.session_state.comments.comments:
        st.info(f"""<{comment.author.displayName}  -  {comment.created}> : 
                {Translator.translate(comment.body)}""")