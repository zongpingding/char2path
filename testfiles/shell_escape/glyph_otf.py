from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen

from bezier_to_tikz import bezier_to_tikz



font = TTFont("../../resources/Fonts/ChironSungHK-R.otf")
char = "你"

# CFF CharStrings('CFF' table only for OTF)
cff = font["CFF "].cff
top_dict = cff.topDictIndex[0]
charstrings = top_dict.CharStrings
glyph_name = font.getBestCmap().get(ord(char))
if not glyph_name:
    print(f"Font does NOT contain Glyph of '{char}'")
    exit()

# get contour (bezier path)
pen = RecordingPen()
charstrings[glyph_name].draw(pen)

def bezier_path(data: list):
    for cmd, pts in pen.value:
        print(cmd, pts)


res = bezier_to_tikz(pen.value, 0.001)
print(res)