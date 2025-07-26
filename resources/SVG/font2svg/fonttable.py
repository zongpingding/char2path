import string
from glyph_unicode_map import *


# 1. alpha letters
ALPHA_LIST = string.ascii_uppercase + string.ascii_lowercase 

# 2. numbers 
# TODO: handle 'eight.taboldstyle' in the future
NUM_LIST = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    ]

# 3. other symbols (31)
OTHER_SYMBOLS = {
    "!": "exclam",
    '"': "quotedbl",
    "#": "numbersign",
    "$": "dollar",
    "%": "percent",
    # " ": "space", # ignore space symbol
    "&": "ampersand",
    "'": "quotesingle",
    "(": "parenleft",
    ")": "parenright",
    "*": "asterisk",
    "+": "plus",
    ",": "comma",
    "-": "hyphen",
    ".": "period",
    "/": "slash",
    ":": "colon",
    ";": "semicolon",
    "<": "less",
    "=": "equal",
    ">": "greater",
    "?": "question",
    "@": "at",
    "[": "bracketleft",
    "\\": "backslash", # backslash '\'
    "]": "bracketright",
    "^": "asciicircum",
    "_": "underscore",
    "`": "grave",
    "{": "braceleft",
    "|": "bar",
    "}": "braceright",
    "~": "asciitilde",
    }