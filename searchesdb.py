import sqlite3
from escape import sqlescape

""" Search Database functions to help detect bugs"""

def searchFailed(search_id, reason):
    """Update searches database that the search_id search failed for the supplied reason."""
    # create a database connection
    connection = sqlite3.connect("searches.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE searches SET succeeded = 0, reason = ? WHERE search_id = ?;", (reason, search_id,))
    # commit insertions
    connection.commit()
    connection.close()
    
def insertSearch(search):
    """inserts the search characters into the searches database and returns the search_id for the newly added search."""
    # create a database connection
    connection = sqlite3.connect("searches.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO searches(search) VALUES(?);", (sqlescape(search),))
    # commit insertions
    connection.commit()
    cursor.execute("SELECT MAX(search_id) FROM searches;")
    search_id = int(cursor.fetchone()[0])
    connection.close()
    # return search_id
    return search_id
    
def searchSucceeded(search_id, mode):
    """For search_id, update the searches database that the search was successful."""
    # create a database connection
    connection = sqlite3.connect("searches.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE searches SET succeeded = 1, mode = ? WHERE search_id = ?;", (mode, search_id,))
    # commit insertions
    connection.commit()
    connection.close()