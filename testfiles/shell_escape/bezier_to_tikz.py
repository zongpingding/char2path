###         convert to tikz path        ###

# scale = 0.001  # turn TikZ unit to 'pt'
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