import re
from typing import Callable
from config import path_to_str, TKZ_DIR, TKZ_COOR_X, TKZ_COOR_Y, TKZ_DIGITS, TKZ_NAME_NUMS, TKZ_NAME_CAPS, TKZ_NAME_SMALL, TKZ_NAME_OTHERS


# regex pattern
COORS_PATTERN = re.compile(r'^\s*\\path\[fill=black\]\s*(.*);\s*$')
SINGLE_COOR_PATTERN = re.compile(r"\(([-+]?[0-9]*\.?[0-9]+),\s*([-+]?[0-9]*\.?[0-9]+)\)")

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

# bezier to tikz
def bezier_to_tikz(data: list, scale: float) -> str:
    tikz_path = []
    for cmd, pts in data:
        if cmd == "moveTo":
            x, y = pts[0]
            tikz_path.append(f"({x * scale:.3f},{y * scale:.3f})")
        elif cmd == "lineTo":
            x, y = pts[0]
            tikz_path.append(f"-- ({x * scale:.3f},{y * scale:.3f})")
        elif cmd == "curveTo":
            (x1, y1), (x2, y2), (x3, y3) = pts
            tikz_path.append(
                f".. controls ({x1 * scale:.3f},{y1 * scale:.3f}) and "
                f"({x2 * scale:.3f},{y2 * scale:.3f}) .. ({x3 * scale:.3f},{y3 * scale:.3f})"
            )
        elif cmd == "qCurveTo":
            n = len(pts)
            if n < 2:
                continue
            for i in range(n - 1):
                cx, cy = pts[i]
                ex, ey = pts[i + 1]
                tikz_path.append(
                    f".. controls ({cx * scale:.3f},{cy * scale:.3f}) .. ({ex * scale:.3f},{ey * scale:.3f})"
                )
        elif cmd == "closePath":
            tikz_path.append("-- cycle")
        
    tikz_path = "\\path " + " ".join(tikz_path) + ";"
    return tikz_path