MAP_ALPHA_SMALL = {f'\\u{ord(c):04x}': c for c in map(chr, range(ord('a'), ord('z') + 1))}

MAP_ALPHA_CAPS  = {f'\\u{ord(c):04x}': c for c in map(chr, range(ord('A'), ord('Z') + 1))}

MAP_NUMS  = {f'\\u{ord(c):04x}': c for c in map(chr, range(ord('0'), ord('9') + 1))}

MAP_OTHER_SYMBOLS = {
    "\u0021": "!",
    "\u0022": '"',
    "\u0023": r"\#",
    "\u0024": "$",
    "\u0025": r"\%",
    "\u0026": "&",
    "\u0027": "'",
    "\u0028": "(",
    "\u0029": ")",
    "\u002a": "*",
    "\u002b": "+",
    "\u002c": ",",
    "\u002d": "-",
    "\u002e": ".",
    "\u002f": "/",
    "\u003a": ":",
    "\u003b": ";",
    "\u003c": "<",
    "\u003d": "=",
    "\u003e": ">",
    "\u003f": "?",
    "\u0040": "@",
    "\u005b": "[",
    "\u005c": r"\ctpbackslash",
    "\u005d": "]",
    "\u005e": "^",
    "\u005f": "_",
    "\u0060": "`",
    "\u007b": r"\{",
    "\u007c": "|",
    "\u007d": r"\}",
    "\u007e": "~",
}