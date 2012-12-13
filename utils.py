import re

def normalise_newlines(input):
    re.sub(r'\r\n', '\n')