[![CTAN Version](https://img.shields.io/ctan/v/char2path)](https://ctan.org/pkg/char2path)
[![GitHub Release](https://img.shields.io/github/v/release/zongpingding/char2path)](https://github.com/zongpingding/char2path/releases/latest)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/zongpingding/char2path)](https://github.com/zongpingding/char2path/commits)
[![Actions Status](https://github.com/zongpingding/char2path/actions/workflows/main.yaml/badge.svg?branch=main)](https://github.com/zongpingding/char2path/actions)
[![GitHub Repo stars](https://img.shields.io/github/stars/zongpingding/char2path)](https://github.com/zongpingding/char2path)

The `char2path` Package
=======================

The `char2path` package (conducted with LaTeX3) provides
a LaTeX package that converts characters into TikZ paths.

Overview
--------

The package provides the `\chartopath` macro

    \chartopath [<keys>] {<string>}

to print Ti*k*Z paths for characters in a string.

See `char2path.pdf` for more. Happy TeXing!

Usage
-----

### Generate `.svg` from font

#### Use `Inkscape`

1. Set text font to latin modern mono
2. Click `Object` -> `Object to path`
3. Save as `Plain SVG`

> Note: The default unit in Inkscape is millimeters (`mm`), while in svg2tikz it is centimeters (`cm`).

#### Use `fonts2svg`

### Generate `svg` from Open True Type font (use package `opentypesvg`):

```shell
fonts2svg lmmonolt10-regular.otf -av
```

Convert the generated SVG files to TikZ files, and

```tex
\def\globalscale{0.01350000}
```

### Generate `pgf` from `svg`

```shell
# full mwe
svg2tikz lmm_8.svg --output lmm_export_8.tikz

# just `scope' env
svg2tikz --codeoutput=codeonly lmm_8.svg --output lmm_export_8.tikz

# batch mode (powershell)
for ($i=0; $i -le 9; $i++) {svg2tikz --codeoutput=codeonly lmm_$i.svg --output lmm_export_$i.tikz}
```

Issues
------

The issue tracker for `char2path` is currently located
[on GitHub](https://github.com/zongpingding/char2path/issues).

Build status
------------

This project uses [GitHub Actions](https://github.com/features/actions)
as a hosted continuous integration service. For each commit, the build status
is tested using the current release of TeX Live.

_Current build status:_ ![build status](https://github.com/zongpingding/char2path/actions/workflows/main.yaml/badge.svg?branch=main)

References
----------

\[1\] https://www.gust.org.pl/projects/e-foundry/latin-modern/download

\[2\] https://www.unicode.org/standard/standard.html

Copyright and License
---------------------

Copyright (C) 2023-2025 by Eureka <[zongpingding.github.io](https://zongpingding.github.io)> and
Mingyu Xia <[myhsia@outlook.com](mailto:myhsia@outlook.com)>

This work may be distributed and/or modified under the conditions
of the LaTeX Project Public License (LPPL), either version 1.3c of
this license or (at your option) any later version.
The latest version of this license is in

    http://www.latex-project.org/lppl.txt

and version 1.3c or later is part of all distributions of LaTeX
version 2008 or later.

This work has the LPPL maintenance status `maintained'.

The Current Maintainer of this work is **Eureka** and **Mingyu Xia**.
