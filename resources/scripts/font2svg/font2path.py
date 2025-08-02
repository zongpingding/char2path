import argparse
import subprocess
from fonttable import *
from glyph_coordinates import *
from config import *


#####  cli args parse  #####
parser = argparse.ArgumentParser(
    prog="font2path",
    usage='%(prog)s [options] font',
    description="font2path: a tool that converts font into TikZ paths.",
    formatter_class=argparse.RawTextHelpFormatter
)
# cli arguments spec
parser.add_argument('-p', '--folder', type=str,      default=None, metavar="",       help="set font folder.")
parser.add_argument('-d', '--data',   type=str,      default=None, metavar="",       help="set tikz path data folder.")
parser.add_argument('-a', '--alias',  type=str,      default=None, metavar="",       help="set font name alias.")
parser.add_argument('-g', '--gensvg', type=str2bool, default=None, metavar="(Bool)", help="set 'True' to generate SVGs from font.")
parser.add_argument('-e', '--extsvg', type=str2bool, default=None, metavar="(Bool)", help="set 'True' to extract SVGs from previous run.")
parser.add_argument('-c', '--gentkz', type=str2bool, default=None, metavar="(Bool)", help="set 'True' to generate tikz path from previous run.")
parser.add_argument('-f', '--font',   type=str,      default=None, metavar="",       help="font name('*.ttf' or '*.otf').")
args = parser.parse_args()

# reload config use argparser
if args.font == None and get_config('font_spec', 'name') == '':
    raise Exception("font name can NOT be empty !")
GEN_SVG     = reload_config(['flow'     , 'gensvg'], args.gensvg)
EXT_SVG     = reload_config(['flow'     , 'extsvg'], args.extsvg)
GEN_TKZ     = reload_config(['flow'     , 'gentkz'], args.gentkz)
TKZ_DIR     = reload_config(['tkz_data' , 'folder'], args.data)
FONT_NAME   = reload_config(['font_spec', 'name'  ], args.font)
FONT_ALIAS  = reload_config(['font_spec', 'alias' ], args.alias)
FONT_FOLDER = reload_config(['font_spec', 'folder'], args.folder)


#####  class 'Font2path'  #####
def run_if_enabled(val:bool):
    def decorator(func:Callable[[], None]):
        if val:
            return func
        else:
            print('nothing happens ...')
            return lambda obj: None
    return decorator
class Font2tikz:
    def __init__(self, font):
        self.font = font

    # generate SVGs from font
    @run_if_enabled(GEN_SVG)
    def gensvg(self):
        os.makedirs(SVG_DIR_MAIN, exist_ok=True)
        subprocess.run([
            "fonts2svg",
            self.font,
            "-av", # cancel view adjust to get the baseline --> still fails
            "-o",
            SVG_DIR_MAIN
            ], check=True)

    # extract some SVGs from previous run
    @run_if_enabled(EXT_SVG)
    def extractsvg(self):
        # make dir
        os.makedirs(SVG_CAPS,  exist_ok=True)
        os.makedirs(SVG_SMALL, exist_ok=True)
        os.makedirs(SVG_NUMS,  exist_ok=True)
        os.makedirs(SVG_OTHERS,exist_ok=True)
        # start extracting ...
        for svg_dir in RAW_SVG_DIR:
            for f in svg_dir.iterdir():
                f_no_ext = f.name[:-4]  # remove .svg extension
                if f.suffix == '.svg':
                    char = f_no_ext
                    match True:
                        case _ if char in OTHER_SYMBOLS.values(): # type of 'dict_values'
                            target_dir = SVG_OTHERS
                        case _ if char in NUM_LIST.values():
                            target_dir = SVG_NUMS
                        case _ if char in ALPHA_CAPS.values():
                            target_dir = SVG_CAPS
                        case _ if char in ALPHA_SMALL.values():
                            target_dir = SVG_SMALL
                        case _:
                            continue
                    subprocess.run(["cp", f, target_dir], check=True)
                    print(f.name, "->", target_dir)

    # generate tikz path from svg
    @staticmethod
    def glyph_classify(dir:str, f_no_ext:str) -> (str):
        match True:
            case _ if dir == SVG_CAPS:
                path_name = MAP_ALPHA_CAPS[ f'u{ord(ALPHA_CAPS_REVERSE[f_no_ext]):04x}']
                file_name = f'ctp-{FONT_ALIAS}-alpha-caps.data.tex'
            case _ if dir == SVG_SMALL:
                path_name = MAP_ALPHA_SMALL[ f'u{ord(ALPHA_SMALL_REVERSE[f_no_ext]):04x}']
                file_name = f'ctp-{FONT_ALIAS}-alpha-small.data.tex'
            case _ if dir == SVG_NUMS:
                path_name = MAP_NUMS[ f'u{ord(NUM_LIST_REVERSE[f_no_ext]):04x}']
                file_name = f'ctp-{FONT_ALIAS}-arabic.data.tex'
            case _ if dir == SVG_OTHERS:
                path_name = MAP_OTHER_SYMBOLS[ f'u{ord(OTHER_SYMBOLS_REVERSE[f_no_ext]):04x}']
                file_name = f'ctp-{FONT_ALIAS}-others.data.tex'
            case _:
                raise Exception("Wrong extracting glyph type.")
        return (path_name, file_name)
    @run_if_enabled(GEN_TKZ)
    def gentikz(self):
        os.makedirs(TKZ_DIR, exist_ok=True)
        tkz_data_clear(FONT_ALIAS)
        for dir in SVG_DIR:
            for f in dir.iterdir():
                if f.suffix == '.svg':
                    f_no_ext = f.name[:-4]  # remove .svg extension
                    target_file = path_to_str(dir, f_no_ext+".pgf")
                    print(target_file)
                    # 1. convert svg to pgf using svg2tikz
                    subprocess.run([
                        "svg2tikz", 
                        "--codeoutput=figonly",
                        str(f),
                        "--output", target_file
                    ], check=True)
                    print('---------> new symbol <---------')
                    print("SVG to PGF : " + f.name, "->", target_file)
                    # 2. extract pgf path coordinates
                    # 2.1 split char data:
                    # extract_tikz_path(
                    #     f_no_ext, 
                    #     target_file, 
                    #     target_file + '.coor'
                    # ) # with 'w'
                    # 2.2 merge char data:
                    path_name = self.glyph_classify(dir, f_no_ext)[0]
                    file_name = self.glyph_classify(dir, f_no_ext)[1]
                    extract_tikz_path(
                        '{'+path_name+'}',
                        target_file,
                        path_to_str(TKZ_DIR, file_name)
                    ) # with 'a'
                    print("PGF to TikZ: " + target_file, "->", target_file+f' -> {{{path_name}}}')


# function '__main__':
if __name__ == "__main__":
    font = Font2tikz(FONT_FOLDER + FONT_NAME)
    font.gensvg()
    font.extractsvg()
    font.gentikz()