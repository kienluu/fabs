import re

def normalise_newlines(input):
    return re.sub(r'\r\n', '\n', input)