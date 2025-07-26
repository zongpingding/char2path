from svgpathtools import wsvg, Line, QuadraticBezier, Path
from freetype import Face


def tuple_to_imag(t):
    return t[0] + t[1] * 1j

# set font face
face = Face('./Fonts/latin-modern-mono10.otf')
face.set_char_size(12, 12)
face.load_char('a')

# get kerning and outline points
face.get_kerning('a', 'b')
outline = face.glyph.outline
y = [t[1] for t in outline.points]
outline_points = [(p[0], max(y) - p[1]) for p in outline.points]

# pick out tags and points
start, end = 0, 0
paths = []
for i in range(len(outline.contours)):
    end = outline.contours[i]
    points = outline_points[start:end + 1]
    points.append(points[0])
    tags = outline.tags[start:end + 1]
    tags.append(tags[0])

segments = [[points[0], ], ]
for j in range(1, len(points)):
    segments[-1].append(points[j])
    if tags[j] and j < (len(points) - 1):
        segments.append([points[j], ])

for segment in segments:
    if len(segment) == 2:
        paths.append(Line(start=tuple_to_imag(segment[0]),
                                end=tuple_to_imag(segment[1])))
    elif len(segment) == 3:
        paths.append(QuadraticBezier(start=tuple_to_imag(segment[0]),
                                    control=tuple_to_imag(segment[1]),
                                    end=tuple_to_imag(segment[2])))
    elif len(segment) == 4:
        C = ((segment[1][0] + segment[2][0]) / 2.0,
                    (segment[1][1] + segment[2][1]) / 2.0)
        paths.append(QuadraticBezier(start=tuple_to_imag(segment[0]),
                                    control=tuple_to_imag(segment[1]),
                                    end=tuple_to_imag(C)))
        paths.append(QuadraticBezier(start=tuple_to_imag(C),
                                    control=tuple_to_imag(segment[2]),
                                    end=tuple_to_imag(segment[3])))

# write svg
start = end + 1
path = Path(*paths)
wsvg(path, filename="lmm_a.svg")


