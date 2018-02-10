import os
import sqlite3
from tictoc import *

def main():
    """
        Create searches database to allow for tracking of searches that break the program.
        Takes approximately 8-10 seconds
    """
    
    ## DEFINE SQL TABLE ##
    
    # begin performance timing
    timer = TicToc()
    
    # specify dictionary file name
    
    db_file = "searches.db"
    
    # try to delete CEDICT.db if it already exists, otherwise continue
    try:
        os.remove(db_file)
    except OSError:
        pass
    
    # create a database connection
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # create entries table
    cursor.execute("CREATE TABLE searches (search_id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, search TEXT NOT NULL, mode TEXT, succeeded INTEGER, reason TEXT);")
    connection.close()
    
    # Finished!
    timer.toc(db_file + " loaded")
    
if __name__ == '__main__':
    main()