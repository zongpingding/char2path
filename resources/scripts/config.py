import os
import tomllib
from pathlib import Path


#####  aux commands  #####
# join path/path to string
def path_join(path1, *extra_path):
    return Path(os.path.join(path1, *extra_path))
def path_to_str(path1, *extra_path):
    return str(os.path.join(path1, *extra_path))
# convert string to bool
def str2bool(v):
    if v == None:
        return False
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', '0'):
        return False
    else:
        raise Exception("Boolean value expected.")


#####  read cfg from toml  #####s
with open("config.toml", "rb") as f:
    config = tomllib.load(f)
def get_config(level_1:str, level_2:str) -> str:
    # print(, type(config.get(level_1).get(level_2)))
    tmp = config.get(level_1).get(level_2)
    if tmp == None:
        return ''
    else:
        return config.get(level_1).get(level_2)

METHOD:str   = get_config('flow', 'method')
GEN_SVG:bool = str2bool(get_config('flow', 'gensvg'))
EXT_SVG:bool = str2bool(get_config('flow', 'extsvg'))
GEN_TKZ:bool = str2bool(get_config('flow', 'gentkz'))

FONT_FOLDER:str = get_config('font_spec', 'folder')
FONT_NAME:str   = get_config('font_spec', 'name')
FONT_ALIAS:str  = get_config('font_spec', 'alias')

SVG_DIR_MAIN:str  = config.get('svg_dir')['folder']
SVG_NUMS:str      = path_join(SVG_DIR_MAIN, get_config('svg_dir', 'nums'))
SVG_CAPS:str      = path_join(SVG_DIR_MAIN, get_config('svg_dir', 'caps'))
SVG_SMALL:str     = path_join(SVG_DIR_MAIN, get_config('svg_dir', 'small'))
SVG_OTHERS:str    = path_join(SVG_DIR_MAIN, get_config('svg_dir', 'others'))

TKZ_DIR:str         = get_config('tkz_data', 'folder')
TKZ_NAME_NUMS:str   = get_config('tkz_data', 'nums'  )
TKZ_NAME_CAPS:str   = get_config('tkz_data', 'caps'  )
TKZ_NAME_SMALL:str  = get_config('tkz_data', 'small' )
TKZ_NAME_OTHERS:str = get_config('tkz_data', 'others')
TKZ_COOR_X:str      = get_config('tkz_data', 'coor_x')
TKZ_COOR_Y:str      = get_config('tkz_data', 'coor_y')
TKZ_DIGITS:int      = get_config('tkz_data', 'digits')

SVG_DIR:list[str]     = [ SVG_NUMS, SVG_CAPS, SVG_SMALL, SVG_OTHERS ]
RAW_SVG_DIR:list[str] = [
    path_join(SVG_DIR_MAIN, get_config('svg_dir', 'sub_1')), 
    path_join(SVG_DIR_MAIN, get_config('svg_dir', 'sub_2'))
]

# print(config["flow"]["gensvg"])
# print(config["font_spec"]["folder"])
# print(SVG_SMALL, TKZ_NAME_OTHERS, TKZ_DIR, FONT_NAME)
# print(config['font_spec']['xxx'])     # raise error
# print(config['font_spec'].get('xxx')) # --> None

# reload config by argparser(cli args come first)
def reload_config(level:list[str], parser_val:str) -> str:
    if parser_val == None:
        return get_config(level[0], level[1])
    else:
        return parser_val