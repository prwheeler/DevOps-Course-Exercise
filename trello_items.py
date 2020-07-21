import requests
import os
from datetime import datetime
import logging as log

BASE_URL = 'https://api.trello.com/1'

# the trello board ID to use for all the lists and cards
BOARD_ID = os.environ.get('TRELLO_BOARD_ID')

# the ID of the 'Done' and 'To Do' standard lists in the above board
TODO_LIST_ID = os.environ.get('TRELLO_TODO_LIST_ID')
DONE_LIST_ID = os.environ.get('TRELLO_DONE_LIST_ID')

SECURITY_PARMS = {
    'key':   os.environ.get('TRELLO_KEY'),
    'token': os.environ.get('TRELLO_TOKEN')
}


def get_items():
    """
    Fetches all items as cards from the trello API.

    Returns:
        list: The list of items.
    """

    url =  f'{BASE_URL}/boards/{BOARD_ID}/cards'

    log.info(f'GET: url={url}')
    response = requests.get(url, SECURITY_PARMS)
    log.info(f'GET: status={response.status_code}')

    items = [Item.from_card(card) for card in response.json()]
    return sorted(items, key=lambda s: s.status, reverse=True)

def add_item(title, desc, due):
    """
    Adds a new item with the specified title to the trello To Do list.

    Args:
        title: The title of the item.
        desc:  An optional item description.
        due:   An optional due date in european DD/MM/YYYY format 
    """

    url = f'{BASE_URL}/cards' 

    params = {**SECURITY_PARMS, **{
        'idList': TODO_LIST_ID,
        'name':   title,
        'desc':   desc,
        'due':    _iso_date_from_eu_date(due)
    }}

    log.info(f'POST: url={url}')
    response = requests.post(url, params)
    log.info(f'POST: status={response.status_code}')

def complete_item(id):
    """
    Move the item (card) with the specified ID to from the trello To Do list to the Done list.

    Args:
        id: The id of item.
    """

    url = f'{BASE_URL}/cards/{id}' 

    params = {**SECURITY_PARMS, **{
        'idList': DONE_LIST_ID
    }}

    log.info(f'PUT: url={url}')
    response = requests.put(url, params)
    log.info(f'PUT: status={response.status_code}')

def _iso_date_from_eu_date(eudate):
    """
    If eudate is a valid euro date return it as an ISO format for trello.

    Args:
        eudate: a date that should be in european format (dd/mm/yyyy) or e
    Returns:
        ISO date: ISO format date or '' if eudate can't be converted
    """
    try:
        return datetime.strptime(eudate, '%d/%m/%Y').isoformat()
    except ValueError:
        return ''    


class Item:
    def __init__(self, id, title, list_id, desc, due):
        self.id = id
        self.title = title
        self.status = Item._status_from_list_id(list_id)
        self.desc = desc
        self.due = Item._format_due_date(due, self.status)

    @classmethod
    def from_card(cls, card):
        """
        Initialize an Item from an instance of a trello card
        """
        return cls(card['id'], card['name'], card['idList'], card['desc'], card['due'])

    @classmethod
    def _status_from_list_id(cls, list_id):
        """
        Return a status of 'Completed' if the trello list is the 'Done' list for 
        this board, otherwise returns 'Not Started'
        """
        return 'Completed' if list_id == DONE_LIST_ID else 'Not Started'

    @classmethod
    def _format_due_date(cls, due, status):
        """
        Return a due date in ISO timestamp format as a simple date or as an
        empty string if the item is already completed 
        """
        if due is None or status == 'Completed':
            return ''
        
        return datetime.fromisoformat(due.replace('Z', '')).strftime('%d/%m/%Y')

