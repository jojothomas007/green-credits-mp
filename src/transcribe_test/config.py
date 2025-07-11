import json
import os
import logging
import sys
from src.transcribe_test.utils.encryption import Crypt
from transcribe_test.dto.config_dto import AppConfig

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

# Define the path for the INI file
CONFIG_DIR = os.path.join(os.getenv('APPDATA'), 'tandt')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

class Config:
    jira_api_url:str = None
    jira_api_username:str = None
    jira_api_token:str = None
    confluence_api_url:str = None

    """
    Load configuration settings from a JSON file into the application's Config class.

    Description:
        Ensures the configuration directory exists. If the configuration file is found at the
        specified location, it loads the JSON data from the file and updates the `Config` class
        attributes: `jira_api_url`, `jira_api_username`, and `jira_api_token`. Logs success upon
        successful loading. If the file doesn't exist or loading fails due to missing keys, it
        initializes the configuration using `Config.__init_config()`.

    Parameters:
        None

    Returns:
        None

    Raises:
        Exception: If there are issues accessing the JSON keys (e.g., missing `api_url`,
                `api_username`, or `api_token` in the `jira` section of the JSON config file).

    Example:
        Configuration file (`config.json`):
        {
            "jira": {
                "api_url": "https://jira.example.com",
                "api_username": "example_user",
                "api_token": "example_token"
            }
        }

        Usage:
        >>> load_config()
        Configuration loaded successfully.
    """
    def load_config():
        os.makedirs(CONFIG_DIR, exist_ok=True)
        if os.path.exists(CONFIG_FILE):
            json_config = {}            
            try:
                with open(CONFIG_FILE, 'r') as file:
                    json_config:json = json.load(file)
                app_config = AppConfig(**json_config)
                Config.confluence_api_url = app_config.confluence.api_url
                Config.jira_api_url = app_config.jira.api_url
                Config.jira_api_username = app_config.jira.api_username
                Config.jira_api_token = Crypt().decrypt(app_config.jira.api_token.encode())                
                logger.info("Configuration loaded successfully.")
                return
            except Exception as e:
                logger.warning("Exception while loading the config. Reseting configuration.")
        Config.__init_config()

    """
    Update the configuration file with new JSON data.

    Description:
        This function overwrites the existing configuration file (`CONFIG_FILE`) with the provided JSON data.
        The JSON content is formatted using indentation for readability. Logs the success of the operation.

    Args:
        json_config (dict): The JSON data to be written to the configuration file. 
                            This must be a Python dictionary that is serializable to JSON format.

    Returns:
        None

    Raises:
        TypeError: If the provided `json_config` is not serializable to JSON format.
        IOError: If there is an issue writing to the file, such as insufficient permissions.

    Example:
        >>> json_config = {
        ...     "jira": {
        ...         "api_url": "https://jira.example.com",
        ...         "api_username": "example_user",
        ...         "api_token": "example_token"
        ...     }
        ... }
        >>> update_config(json_config)
        Configuration file updated.
    """
    def update_config(app_config:AppConfig):
        json_config =  json.loads(app_config.model_dump_json())
        json_config['jira']['api_token'] = Crypt().encrypt(json_config['jira']['api_token']).decode()
        with open(CONFIG_FILE, 'w') as file:
            json.dump(json_config, file, indent=4)
        logger.info("Configuration file updated.")
    
    def __init_config():
        json_config =  AppConfig().model_dump_json() 
        with open(CONFIG_FILE, 'w') as file:
            json.dump(json_config, file, indent=4)
        logger.info("New Configuration file created.")
        Config.confluence_api_url = ""
        Config.jira_api_url = ""
        Config.jira_api_username = ""
        Config.jira_api_token = ""