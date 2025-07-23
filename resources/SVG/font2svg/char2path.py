import os
import string
import subprocess
from pathlib import Path



#####  bool control  #####
EXTRACT_SVG_FROM_FONT = False 
EXTRACT_SVG = True
EXTRACT_COOR = False


#####  directories  #####
PARENT_DIR = Path('SVGS')
SUB_DIR = Path('.')
# SUB_DIR = Path('_moreSVGs_')
SVG_DIR = Path(os.path.join(PARENT_DIR, SUB_DIR))

caps_dir = "caps"
small_dir = "small"
nums_dir = "nums"
CAPS_DIR = Path(os.path.join(PARENT_DIR, caps_dir))
SMALL_DIR = Path(os.path.join(PARENT_DIR, small_dir))
NUMS_DIR = Path(os.path.join(PARENT_DIR, nums_dir))
if EXTRACT_SVG:
    os.makedirs(CAPS_DIR, exist_ok=True)
    os.makedirs(SMALL_DIR, exist_ok=True)
    os.makedirs(NUMS_DIR, exist_ok=True)

# extract target
ALPHA_LIST = string.ascii_uppercase + string.ascii_lowercase 
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


#####  generate svg from font  #####
# fonts2svg lmmonolt10-regular.otf -av
FONT = "latin-modern-mono10.otf"
if EXTRACT_SVG_FROM_FONT:
    subprocess.run([
        "fonts2svg",
        FONT,
        "-av",
        ], check=True)


#####    extract letters and numbers from SVG_DIR      #####
if EXTRACT_SVG:
    for f in SVG_DIR.iterdir():
        # f_no_ext = f.name.split('.')[0] # this will extracts 'eight.taboldstyle', etc,
        f_no_ext = f.name[:-4]  # remove .svg extension
        if f.suffix == '.svg' and \
           (f_no_ext in ALPHA_LIST or f_no_ext in NUM_LIST):
            char = f_no_ext
            match True:
                case _ if char in NUM_LIST:
                    target_dir = NUMS_DIR
                case _ if char.isupper(): # for numbers
                    target_dir = CAPS_DIR
                case _ if char.islower():
                    target_dir = SMALL_DIR 
                case _:
                    continue
            # subprocess.run(["cp", f, target_dir], check=True)
            print(f.name, "->", target_dir)


#####   generate pgf from svg   #####
# svg2tikz --codeoutput=codeonly lmm_8.svg --output lmm_export_8.tikz
# sed -n 's/^[[:space:]]*\\path\[fill=black\][[:space:]]*\(.*\);[[:space:]]*$/{\1}/p' eight.pgf > output.txt 
if EXTRACT_COOR:
    for dir in [CAPS_DIR, SMALL_DIR, NUMS_DIR]:
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



