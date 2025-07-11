import streamlit as st

from src.transcribe_test.service.translator import Translator
from src.transcribe_test.config import Config
from src.transcribe_test.service.confluence_service import ConfluenceService
import logging, sys
import html2text


# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

def fetch_translate_confluence_page():
    confluenceService = ConfluenceService()
    pageId = confluenceService.get_pageId_from_url(st.session_state.confluence_url)
    confluence_page = confluenceService.get_page_content(pageId) 
    st.session_state.translated_page = Translator.translate(confluence_page.body.view.value)
    st.session_state.step = 1

def reset_state():
    st.session_state.step = 0  # Move to the "Reset" step

st.set_page_config(
    page_title="Confluence Page Translator",
    page_icon="📚"
)

st.header('📚 Confluence Page Translator')
st.subheader('Translates text from Confluence Page.')
st.button("Reset", on_click=reset_state)

if "step" not in st.session_state:
    st.session_state.step = 0 # Tracks the current step (0: initial, 1: fetched, 2: translated)
st.session_state.confluence_url = st.text_input("Confluence Page url for Translation:", disabled=(st.session_state.step >= 1))
Config.load_config()
# Fetch Jira issue details
st.button("Translate", disabled=(st.session_state.step >= 1), on_click=fetch_translate_confluence_page)
    
# Display text area and Translate button if Fetch is clicked
if st.session_state.step >= 1:
    translated_text = html2text.html2text(st.session_state.translated_page)
    st.text_area("Confluence Page Body : ", translated_text, 250, disabled=True)
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(translated_text)
    with open("output.md", "rb") as f:
        if st.download_button("Download", f, disabled=(st.session_state.step >= 2), on_click="rerun",
                    file_name="test.md", mime='text/markdown'):
            st.success(f"Jira Issue updated!")
            st.session_state.step = 2