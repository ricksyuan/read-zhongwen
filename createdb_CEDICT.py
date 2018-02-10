import os
import re
import sqlite3
from tictoc import TicToc
from pinyin import prettify_pinyin


def main():
    """
        Loads CEDICT txt file into an indexed SQL database.
        
        Converts pinyin to format with diacriticals.
        
        Takes approximately 8-10 seconds
    """
    
    ## DEFINE SQL TABLE ##
    
    # begin performance timing
    timer = TicToc()
    
    # specify dictionary file name
    
    db_file = "CEDICT.db"
    
    # try to delete CEDICT.db if it already exists, otherwise continue
    try:
        os.remove(db_file)
    except OSError:
        pass
    
    # create a database connection
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    # create entries table
    cursor.execute("CREATE TABLE entries (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, traditional TEXT NOT NULL, simplified TEXT NOT NULL, pinyin TEXT NOT NULL, definition TEXT NOT NULL);")
    
    # create unique index
    cursor.execute("CREATE UNIQUE INDEX idx_entries ON entries (traditional, simplified, pinyin)") # Unique only guaranteed by having all three of traditional, simplified, pinyin in index
    
    # create individual indices to speed up search (100x difference!)
    cursor.execute("CREATE INDEX idx_entries_simplified ON entries (simplified)") # Only this index is used in "SELECT * FROM entries WHERE simplified = 'A'"";
    cursor.execute("CREATE INDEX idx_entries_traditional ON entries (traditional)")
    cursor.execute("CREATE INDEX idx_entries_pinyin ON entries (pinyin)")
    
    ## INSERT ENTRIES ##
    
    # CEDICT entries contained on a single line
    # create regex to parse entries
    
    regex = re.compile(r"^([^ ]+) ([^ ]+) \[(.+)\] /(.+)/")
    
    with open("cedict_1_0_ts_utf-8_mdbg.txt") as infile:
    
        for line in infile:
            # comment lines in CEDICT start with #. Ignore these
            if line[0] != '#':
                (traditional, simplified, pinyin, definition) = regex.match(line).groups()
                # Make pinyin pretty (convert numbers to diacritical marks)
                pretty_pinyin = prettify_pinyin(pinyin)
                
                # Make pinyin in definitions pretty
            
                # pinyin is always contained in square brackets [ ] and typically followed by a number, e.g., [qing1 zi4 tou2].
                # Reg ex group defined by () captures pinyin inside of brackets, e.g. qing1 zi4 tou2. Space character is needed to
                # capture multi-word pinyin.
                
                definition_pinyin_regex = re.compile(r"\[([a-zA-Z0-5(u:) ]+)\]+") # handles multiple [] groups 
                definition_pinyin_list = definition_pinyin_regex.findall(definition)

                non_blank_definition_pinyin_list = list(filter(lambda x: x.strip() != "", definition_pinyin_list)) # handles [ ] with no pinyin inside (see following definition: 中括號 中括号 [zhong1 kuo4 hao4] /square brackets [ ] (math.)/)

                if len(non_blank_definition_pinyin_list) == 0:
                    pass
                else:
                    for definition_pinyin in non_blank_definition_pinyin_list:
                        definition_pretty_pinyin = prettify_pinyin(definition_pinyin)
                        definition = definition.replace(definition_pinyin, definition_pretty_pinyin)
                entry = (traditional, simplified, pretty_pinyin, definition)
                cursor.execute("INSERT INTO entries(traditional,simplified, pinyin, definition) VALUES(?,?,?,?)", entry)
    # commit insertions
    connection.commit()
    connection.close()
    
    # Finished!
    timer.toc(db_file + " loaded")
    
if __name__ == '__main__':
    main()