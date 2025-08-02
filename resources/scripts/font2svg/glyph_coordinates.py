import re
from typing import Callable
from config import path_to_str, TKZ_DIR, TKZ_COOR_X, TKZ_COOR_Y, TKZ_DIGITS


# regex pattern
COORS_PATTERN = re.compile(r'^\s*\\path\[fill=black\]\s*(.*);\s*$')
SINGLE_COOR_PATTERN = re.compile(r"\(([-+]?[0-9]*\.?[0-9]+),\s*([-+]?[0-9]*\.?[0-9]+)\)")

# clear previous data
def tkz_data_clear(font_alias:str) -> None:
    open(path_to_str(TKZ_DIR, f'ctp-{font_alias}-arabic.data.tex'), 'w')
    open(path_to_str(TKZ_DIR, f'ctp-{font_alias}-alpha-caps.data.tex'), 'w')
    open(path_to_str(TKZ_DIR, f'ctp-{font_alias}-alpha-small.data.tex'),'w')
    open(path_to_str(TKZ_DIR, f'ctp-{font_alias}-others.data.tex'), 'w')

# modify coordinates format
# add '\ctpXshift' and '\ctpYshift' to x/y in '(x, y)'
def coor_transform(
        data: str,
        func: Callable[[float, float], str]
    ) -> str:
    def replacer(match: re.Match) -> str:
        x = float(match.group(1))
        y = float(match.group(2))
        return func(x, y)
    
    return SINGLE_COOR_PATTERN.sub(replacer, data)

# only extract tikz coordinates
# svg2tikz --codeoutput=codeonly lmm_8.svg --output lmm_8.pgf
# sed -n 's/^[[:space:]]*\\path\[fill=black\][[:space:]]*\(.*\);[[:space:]]*$/{\1}/p' eight.pgf > eight.pgf.coor
def extract_tikz_path(char_name:str, input_file:str, output_file:str) -> None:
    with open(input_file, 'r', encoding='utf-8') as infile, \
        open(output_file, 'a', encoding='utf-8') as outfile:

        for line in infile:
            match = COORS_PATTERN.match(line)
            if match:
                content = match.group(1)
                content_modify = coor_transform(
                        content, 
                        lambda x, y:
                            f"({x + 20:.{TKZ_DIGITS}f}{TKZ_COOR_X}," +
                            f"{y:.{TKZ_DIGITS}f}{TKZ_COOR_Y})"
                    )
                outfile.write(f'{char_name} = {{{content_modify}}},\n')