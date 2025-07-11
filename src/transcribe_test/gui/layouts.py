import tkinter as tk
from tkinter import ttk
from src.transcribe_test.gui.actions import Action
from src.transcribe_test.gui.widget import TntButton, TntTextArea, TntTextBox, TntLabel
from src.transcribe_test.config import Config
class App():
    def create_window():

        # Create the main window
        root = tk.Tk()
        root.title("Transcribe and Test")

        # Create the notebook (tab container)
        notebook = ttk.Notebook(root)

        # Tab 1: Jira Issue
        jira_tab = ttk.Frame(notebook)
        notebook.add(jira_tab, text="JiraIssue")

        # Tab 2: Settings
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text="Settings ⚙️")

        # Pack notebook (tabs)
        notebook.pack(expand=True, fill="both")

        JiraIssueTab(jira_tab)
        SettingsTab(settings_tab)

        return root
    
class JiraIssueTab(tk.Frame):
    def __init__(self, parent):
        # Layout for Jira Issue tab
        self.label_jira_issue = TntLabel(parent, text="Jira Issue Key for Translation:")
        self.label_jira_issue.pack(pady=10, anchor="w")

        self.entry_issue_key = TntTextBox(parent)
        self.entry_issue_key.pack(pady=10, anchor="w")

        self.update_button = TntButton(parent, text="Update", command=self.__update_jira_issue)
        self.update_button.pack(pady=5)
    
    def __update_jira_issue(self):
        Action().translate_jira_issue_description(
            self.entry_issue_key.get()
            )


class SettingsTab(tk.Frame):
    def __init__(self, parent):
        self.label_url = TntLabel(parent, text="Jira Base Url:")
        self.label_url.pack(pady=10, anchor="w")

        self.entry_url = TntTextBox(parent)
        self.entry_url.pack(pady=10, anchor="w")
        self.entry_url.insert(0, Config.jira_api_url)

        self.label_username = TntLabel(parent, text="Jira username:")
        self.label_username.pack(pady=10, anchor="w")

        self.entry_username = TntTextBox(parent)
        self.entry_username.pack(pady=10, anchor="w")
        self.entry_username.insert(0, Config.jira_api_username)

        self.label_token = TntLabel(parent, text="Jira API Token:")
        self.label_token.pack(pady=10, anchor="w")

        self.entry_token = TntTextArea(parent)
        self.entry_token.pack(pady=10, anchor="w")
        self.entry_token.insert(0, Config.jira_api_token)

        self.update_button = TntButton(parent, text="Update", command=self.__update_settings)
        self.update_button.pack(pady=5)

    def __update_settings(self):
        Action().update_settings(
            self.entry_url.get(),
            self.entry_username.get(),
            self.entry_token.get()
            )


