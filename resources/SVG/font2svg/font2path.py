import os
import subprocess
from pathlib import Path
# font table data
from fonttable import *



#####  bool control  #####
EXTRACT_SVG_FROM_FONT = True 
EXTRACT_SVG = False
EXTRACT_COOR = False


#####    assign font     #####
FONT_FOLDER = "../../Fonts/"
FONT_NAME = "latin-modern-roman.mroman10-regular.otf"
FONT = FONT_FOLDER + FONT_NAME


#####  SVG directories  #####
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
                    case _ if char in NUM_LIST:
                        target_dir = NUMS_DIR
                    case _ if (len(char)==1 and char.isupper()):
                        target_dir = CAPS_DIR
                    case _ if (len(char)==1 and char.islower()):
                        target_dir = SMALL_DIR
                    case _:
                        continue
                subprocess.run(["cp", f, target_dir], check=True)
                print(f.name, "->", target_dir)


#####   generate pgf from svg   #####
# svg2tikz --codeoutput=codeonly lmm_8.svg --output lmm_export_8.tikz
# sed -n 's/^[[:space:]]*\\path\[fill=black\][[:space:]]*\(.*\);[[:space:]]*$/{\1}/p' eight.pgf > output.txt 
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
                print(f.name, "->", target_file)
                # 2. extract pgf path coordinates
                with open(str(target_file) + '.coor', 'w') as out_file:
                    subprocess.run([
                        "sed",
                        "-n",
                        r"s/^[[:space:]]*\\path\[fill=black\][[:space:]]*\(.*\);[[:space:]]*$/{\1}/p",
                        target_file
                    ], stdout=out_file, check=True)
                    print(target_file, "->", target_file+'.coor')

