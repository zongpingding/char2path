from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen

from bezier_to_tikz import bezier_to_tikz



font = TTFont("../../Fonts/arial.ttf")
glyph_set = font.getGlyphSet() # 'Glyph Set' only for TTF
glyph = glyph_set["B"]

pen = RecordingPen()
glyph.draw(pen)

def bezier_path(data: list):
    for cmd, pts in data:
        print(cmd, pts)

# bezier_path(pen.value)
res = bezier_to_tikz(pen.value, 0.001)
print(res)


#  Output data
# letter 'A':
# \path (-0.003,0.000) -- (0.560,1.466) -- (0.769,1.466) -- (1.369,0.000) -- (1.148,0.000) -- (0.977,0.444) -- (0.364,0.444) -- (0.203,0.000) -- cycle (0.420,0.602) -- (0.917,0.602) -- (0.764,1.008) .. controls (0.694,1.193) .. (0.660,1.312) .. controls (0.632,1.171) .. (0.581,1.032) -- cycle;

# letter 'B':
# \path (0.150,0.000) -- (0.150,1.466) -- (0.700,1.466) .. controls (0.868,1.466) .. (1.071,1.377) .. controls (1.071,1.377) .. (1.186,1.192) .. controls (1.186,1.192) .. (1.186,1.091) .. controls (1.186,0.997) .. (1.084,0.831) .. controls (1.084,0.831) .. (0.981,0.780) .. controls (1.114,0.741) .. (1.257,0.553) .. controls (1.257,0.553) .. (1.257,0.425) .. controls (1.257,0.322) .. (1.170,0.145) .. controls (1.170,0.145) .. (1.042,0.049) .. controls (1.042,0.049) .. (0.849,0.000) .. controls (0.849,0.000) .. (0.709,0.000) -- cycle (0.344,0.850) -- (0.661,0.850) .. controls (0.790,0.850) .. (0.846,0.867) .. controls (0.920,0.889) .. (0.995,0.991) .. controls (0.995,0.991) .. (0.995,1.068) .. controls (0.995,1.141) .. (0.925,1.252) .. controls (0.925,1.252) .. (0.795,1.293) .. controls (0.795,1.293) .. (0.637,1.293) -- (0.344,1.293) -- cycle (0.344,0.173) -- (0.709,0.173) .. controls (0.803,0.173) .. (0.841,0.180) .. controls (0.908,0.192) .. (0.998,0.248) .. controls (0.998,0.248) .. (1.056,0.355) .. controls (1.056,0.355) .. (1.056,0.425) .. controls (1.056,0.507) .. (0.972,0.628) .. controls (0.972,0.628) .. (0.823,0.677) .. controls (0.823,0.677) .. (0.683,0.677) -- (0.344,0.677) -- cycle;