import os
import subprocess
from pathlib import Path
from fonttable import *
from glyph_coordinates import *



#####  bool control  #####
EXTRACT_SVG_FROM_FONT = True 
EXTRACT_SVG = True
EXTRACT_COOR = True


#####    assign font     #####
FONT_FOLDER = "../../Fonts/"
FONT_NAME = "texgyreadventor-regular.otf"
FONT_ALIAS = 'texgyre'
FONT = FONT_FOLDER + FONT_NAME

#####  SVG directories  #####
DATA_DIR = "../../data"
PARENT_DIR = Path('SVGs')
SUB_DIR_1 = Path('.')
SUB_DIR_2 = Path('_moreSVGs_')
RAW_SVG_PATH = PARENT_DIR
SVG_DIR = [Path(os.path.join(PARENT_DIR, SUB_DIR_1)), Path(os.path.join(PARENT_DIR, SUB_DIR_2))]

caps_dir = "caps"
small_dir = "small"
nums_dir = "nums"
other_symbols_dir = "other_symbols"
CAPS_DIR = Path(os.path.join(PARENT_DIR, caps_dir))
SMALL_DIR = Path(os.path.join(PARENT_DIR, small_dir))
NUMS_DIR = Path(os.path.join(PARENT_DIR, nums_dir))
OTHER_SYMBOLS_DIR = Path(os.path.join(PARENT_DIR, other_symbols_dir))
FONTABLE_SVG_DIR = [CAPS_DIR, SMALL_DIR, NUMS_DIR, OTHER_SYMBOLS_DIR]
if EXTRACT_SVG:
    os.makedirs(CAPS_DIR, exist_ok=True)
    os.makedirs(SMALL_DIR, exist_ok=True)
    os.makedirs(NUMS_DIR, exist_ok=True)
    os.makedirs(OTHER_SYMBOLS_DIR, exist_ok=True)


#####  generate svg from font  #####
# fonts2svg lmmonolt10-regular.otf -av
if EXTRACT_SVG_FROM_FONT:
    os.makedirs(RAW_SVG_PATH, exist_ok=True)
    subprocess.run([
        "fonts2svg",
        FONT,
        "-av", # cancel view adjust to get the baseline --> still fails
        "-o",
        RAW_SVG_PATH
        ], check=True)


#####    extract letters and numbers from SVG_DIR      #####
if EXTRACT_SVG:
    for svg_dir in SVG_DIR:
        for f in svg_dir.iterdir():
            # f_no_ext = f.name.split('.')[0] # this will extracts 'eight.taboldstyle', etc,
            f_no_ext = f.name[:-4]  # remove .svg extension
            if f.suffix == '.svg':
                char = f_no_ext
                match True:
                    case _ if char in OTHER_SYMBOLS.values(): # type of 'dict_values'
                        target_dir = OTHER_SYMBOLS_DIR
                    case _ if char in NUM_LIST.values():
                        target_dir = NUMS_DIR
                    case _ if char in ALPHA_CAPS.values():
                        target_dir = CAPS_DIR
                    case _ if char in ALPHA_SMALL.values():
                        target_dir = SMALL_DIR
                    case _:
                        continue
                subprocess.run(["cp", f, target_dir], check=True)
                print(f.name, "->", target_dir)


#####   generate pgf from svg   #####
# maps dir to unicode map
def dir_to_unicode_map(dir:str) -> (str):
    match True:
        case _ if dir == str(CAPS_DIR):
            name_in_coor = MAP_ALPHA_CAPS[ f'u{ord(ALPHA_CAPS_REVERSE[f_no_ext]):04x}']
            file_name = f'ctp-{FONT_ALIAS}-alpha-caps.data.tex'
        case _ if dir == str(SMALL_DIR):
            name_in_coor = MAP_ALPHA_SMALL[ f'u{ord(ALPHA_SMALL_REVERSE[f_no_ext]):04x}']
            file_name = f'ctp-{FONT_ALIAS}-alpha-small.data.tex'
        case _ if dir == str(NUMS_DIR):
            name_in_coor = MAP_NUMS[ f'u{ord(NUM_LIST_REVERSE[f_no_ext]):04x}']
            file_name = f'ctp-{FONT_ALIAS}-arabic.data.tex'
        case _ if dir == str(OTHER_SYMBOLS_DIR):
            name_in_coor = MAP_OTHER_SYMBOLS[ f'u{ord(OTHER_SYMBOLS_REVERSE[f_no_ext]):04x}']
            file_name = f'ctp-{FONT_ALIAS}-others.data.tex'
        case _:
            raise Exception("Wrong mapping type.")
    return (name_in_coor, file_name)

if EXTRACT_COOR:
    for dir in FONTABLE_SVG_DIR:
        for f in dir.iterdir():
            if f.suffix == '.svg':
                f_no_ext = f.name[:-4]  # remove .svg extension
                target_file = os.path.join(dir, f_no_ext + '.pgf')
                # 1. convert svg to pgf using svg2tikz
                subprocess.run([
                    "svg2tikz", 
                    "--codeoutput=figonly",
                    str(f),
                    "--output", target_file
                ], check=True)
                print('---------> new symbol <---------')
                print("SVG to PGF :" + f.name, "->", target_file)
                # 2. extract pgf path coordinates
                # 2.1 split char data:
                # extract_tikz_path(
                #     f_no_ext, 
                #     str(target_file), 
                #     str(target_file) + '.coor'
                # ) # with 'w'
                # 2.2 merge char data:
                name_in_coor = dir_to_unicode_map(str(dir))[0]
                file_name = dir_to_unicode_map(str(dir))[1]
                extract_tikz_path(
                    '{'+name_in_coor+'}', 
                    str(target_file),
                    DATA_DIR+file_name
                ) # with 'a'
                print("PGF to TikZ:" + target_file, "->", target_file+f' -> {{{name_in_coor}}}')