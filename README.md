[![CTAN Version](https://img.shields.io/ctan/v/char2path)](https://ctan.org/pkg/char2path)
[![GitHub Release](https://img.shields.io/github/v/release/zongpingding/char2path)](https://github.com/zongpingding/char2path/releases/latest)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/zongpingding/char2path)](https://github.com/zongpingding/char2path/commits)
[![Actions Status](https://github.com/zongpingding/char2path/actions/workflows/main.yaml/badge.svg?branch=main)](https://github.com/zongpingding/char2path/actions)
[![GitHub Repo stars](https://img.shields.io/github/stars/zongpingding/char2path)](https://github.com/zongpingding/char2path)

The `char2path` Package
=======================

The `char2path` package provides a LaTeX package for converting characters into TikZ paths.

Overview
--------

The package provides the `\chartopath` and `\chartoclip` macro

    \chartopath [<keys>] {<font>} {<string>}
    \chartoclip [<keys>] {<font>} {<character>}

to print Ti*k*Z paths for characters in a string.

See `char2path.pdf` for more. Happy TeXing!

Generate Ti*k*Z paths from font
-------------------------------
First, install the dependencies. For Windows users:
```shell
cd resources/scripts/font2svg
pip install -r requirements.txt
```

for Linux users:
```python
cd resources/scripts/font2svg
pip3 install -r requirements.txt
```

on macOS, run the following command:
```shell
cd resources/scripts/font2svg
brew install cairo pkg-config
python3 -m pip install -r requirements.txt --break-system-packages
```

Next, custom your own `config.toml`, The default configuration is:
```toml
[flow]
gensvg = true
extsvg = true
gentkz = true

[font_spec]
folder = "../../Fonts/"
name   = "texgyreadventor-regular.otf"
alias  = 'texgyre'

[svg_dir]
folder = "SVGs"
sub_1  = "."
sub_2  = "_moreSVGs_"
caps   = "caps"
small  = "small"
nums   = "nums"
others = "others"

[tkz_data]
folder = "../../data"
caps   = "cpas"
small  = "small"
nums   = "nums"
others = "others"
digits = 3
# coor_x = "+\\ctpXshift"
# coor_y = "+\\ctpYshift"
```

Command-line arguments take precedence over the TOML file.
``` txt
usage: font2path [options] font

font2path: a tool that converts font into TikZ paths.

options:
  -h, --help           show this help message and exit
  -p, --folder         set font folder.
  -d, --data           set tikz path data folder.
  -a, --alias          set font name alias.
  -g, --gensvg (Bool)  set 'True' to generate SVGs from font.
  -e, --extsvg (Bool)  set 'True' to extract SVGs from previous run.
  -c, --gentkz (Bool)  set 'True' to generate tikz path from previous run.
  -f, --font           font name('*.ttf' or '*.otf').
```


Finally, run the command below:
``` shell
python font2path.py
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

Copyright (C) 2025 by Zongping Ding <[zongpingding5@outlook.com](mailto:zongpingding5@outlook.com)> and
Mingyu Xia <[myhsia@outlook.com](mailto:myhsia@outlook.com)>

This package's data is converted from
[Latin Modern family](https://www.gust.org.pl/projects/e-foundry/latin-modern),
which is based on the Computer Modern fonts released into public domain by
AMS (1997). It's under the license of
**[The GUS Font License (GFL)](https://ctan.org/license/gfl)**.

This work may be distributed and/or modified under the conditions
of the LaTeX Project Public License (LPPL), either version 1.3c of
this license or (at your option) any later version.
The latest version of this license is in

    http://www.latex-project.org/lppl.txt

and version 1.3c or later is part of all distributions of LaTeX
version 2008 or later.

This work has the LPPL maintenance status `maintained'.

The Current Maintainer of this work is **Zongping Ding** and **Mingyu Xia**.
