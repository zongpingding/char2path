from glyph_unicode import *


# 1. alpha letters
ALPHA_CAPS  = {c: c for c in map(chr, range(ord('A'), ord('Z') + 1))}
ALPHA_SMALL = {c: c for c in map(chr, range(ord('a'), ord('z') + 1))}


# 2. numbers 
# TODO: handle 'eight.taboldstyle' in the future
NUM_LIST = {
    "0": "zero",  
    "1": "one",   
    "2": "two",   
    "3": "three", 
    "4": "four",  
    "5": "five",  
    "6": "six",   
    "7": "seven", 
    "8": "eight", 
    "9": "nine",  
    }

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


# reverse char mapping
ALPHA_CAPS_REVERSE = ALPHA_CAPS
ALPHA_SMALL_REVERSE = ALPHA_SMALL
NUM_LIST_REVERSE = {value: key for key, value in NUM_LIST.items()}
OTHER_SYMBOLS_REVERSE = {value: key for key, value in OTHER_SYMBOLS.items()}