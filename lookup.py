import sqlite3
from escape import jsonescape

# Max length of characters in traditional or simplified CEDICT entry. Update whenever loading new CEDICT dictionary.
MAX_LENGTH = 20;

def lookup(text):
    """ Lookup simplified character in CEDICT SQL database.
        jsonescapes returned phrases dictionary
        SQL queries use ? and tuples, following https://docs.python.org/2/library/sqlite3.html to prevent SQL injection.
    """

    # specify dictionary file name 
    db_file = "CEDICT.db"
    
    # create a database connection
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    # analyze text to determine whether to lookup characters as traditional or simplified
    (traditional_count, simplified_count, other_count) = analyze_text(text)
    # traditional or simplified mode. Start with queries for the type of character most frequently found
    mode = None
    if simplified_count >= traditional_count:
        mode = "simplified"
    else:
        mode = "traditional"
    
    # create phrases list with definitions
    phrases = []

    while len(text) > 0:
       
        # Start with longest phrase possible and shrink character by character until a phrase is found or none
        for i in range(min(MAX_LENGTH, len(text)), 0, -1):
            current_text = text[0:i]
            rows = []
            if mode == "simplified":
                # try simplified first
                cursor.execute("SELECT traditional, simplified, pinyin, definition FROM entries WHERE simplified = ?", (current_text,))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    phrase_type = "simplified"
                else:
                    # then try traditional if no simplified
                    cursor.execute("SELECT traditional, simplified, pinyin, definition FROM entries WHERE traditional = ?", (current_text,))
                    rows = cursor.fetchall()
                    # change label
                    if len(rows) > 0:
                        phrase_type = "traditional"
            elif mode == "traditional":
                # try traditional first
                cursor.execute("SELECT traditional, simplified, pinyin, definition FROM entries WHERE traditional = ?", (current_text,))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    phrase_type = "traditional"
                else:
                    # then try simplified if no traditional
                    cursor.execute("SELECT traditional, simplified, pinyin, definition FROM entries WHERE simplified = ?", (current_text,))
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        phrase_type = "simplified"

            # if word is found, then add results to phrases list
            if len(rows) > 0:
                definitions = []
                for row in rows:
                    # jsonescape information to be loaded into phrases
                    traditional = jsonescape(row[0])
                    simplified = jsonescape(row[1])
                    pinyin = jsonescape(row[2])
                    definition = jsonescape(row[3])
                    definitions.append({"traditional": traditional, "simplified": simplified, "pinyin": pinyin, "definition": definition})
                phrases.append({"lookup": jsonescape(current_text), "definitions": definitions, "type": phrase_type})
                text = text[i:]
                break
            elif i == 1:
                # If reached this point, character is not in dictionary, so add first character  as an "other" phrase_type and start parsing
                # from next character onwards.
                phrases.append({"lookup": jsonescape(text[0]), "definitions": None, "type": "other"})
                text = text[1:]

    connection.close()
    return (phrases, mode)
    
    
    
def analyze_text(text):
    """ Returns count of traditional, simplified, and other text in a tuple """

    # specify dictionary file name 
    db_file = "CEDICT.db"
    
    # create a database connection
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    characters = []
    simplified_count = 0
    traditional_count = 0
    other_count = 0
    for character in text:
        
        # select from simplified
        cursor.execute("SELECT traditional, simplified, pinyin, definition FROM entries WHERE simplified = ?", (character,))
        simplified_rows = cursor.fetchall()
        if len(simplified_rows) > 0:
            simplified_count += 1
        # select from traditional
        cursor.execute("SELECT traditional, simplified, pinyin, definition FROM entries WHERE traditional = ?", (character,))
        traditional_rows = cursor.fetchall()
        if len(traditional_rows) > 0:
            traditional_count += 1
        
        # not found in either simplified or traditional
        if len(simplified_rows) == 0 and len(traditional_rows) == 0:
            other_count += 1
            
    connection.close()
    return traditional_count, simplified_count, other_count