import logging 
import sqlite3
from sqlite3 import Error

logger = logging.getLogger(__name__)

def database_connect(path: str):
    """Connect to the Bot Database"""
    
    connection = None
    try: 
        connection = sqlite3.connect(path)
        logger.info('Successfully connected to database: %s', path)
        
    except Error as exception:
        logger.error('Issue connecting to database "%s"', path, exc_info=True)
        raise RuntimeError('Issue connecting to database') from exception
    
    return connection

def execute_query(connection, query):
    
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logger.debug('Executed: %s', query)
    except Error as exception:
        logger.error('Issue running query"%s"', query, exc_info=True)
        


""" Details about Table format
Table: delayed_messages

id: INTEGER - autoincrement
channel: INTEGER - NOT NULL
message: INTEGER - NOT NULL
call_date: INTEGER - NOT NLL
"""
        