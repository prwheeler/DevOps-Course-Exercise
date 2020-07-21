"""Flask configuration class."""
import os

def _load_env_value(env_key):
    """
    Load and return an environment variable or fail with a reminder
    """
    value = os.environ.get(env_key)
    if not value:
        raise ValueError(f"No {env_key} set for Flask application. Did you forget to run setup.sh?")
    return value


class Config:
    """Base configuration variables."""
    SECRET_KEY          = _load_env_value('SECRET_KEY')
    TRELLO_KEY          = _load_env_value('TRELLO_KEY')
    TRELLO_TOKEN        = _load_env_value('TRELLO_TOKEN')
    TRELLO_BOARD_ID     = _load_env_value('TRELLO_BOARD_ID')
    TRELLO_TODO_LIST_ID = _load_env_value('TRELLO_TODO_LIST_ID')
    TRELLO_DONE_LIST_ID = _load_env_value('TRELLO_DONE_LIST_ID')
