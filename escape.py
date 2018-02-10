""" Function to escape JSON and SQL. """

def jsonescape(text):
    """Escape characters in text for JSON. See http://json.org/"""
    escaped_string = text.replace('\\', '\\\\')
    escaped_string = escaped_string.replace('"', '\\"')
    escaped_string = escaped_string.replace('/', '\\/')
    escaped_string = escaped_string.replace('\b', '\\b')
    escaped_string = escaped_string.replace('\f', '\\f')
    escaped_string = escaped_string.replace('\n', '\\n')
    escaped_string = escaped_string.replace('\r', '\\r')
    escaped_string = escaped_string.replace('\t', '\\t')
    
    return escaped_string
    
def sqlescape(text):
    """Escape characters in text for SQL."""
    escaped_string = text.replace("'", "''")
    return escaped_string
