# char2path

A LaTeX package that converts characters into TikZ paths

REF:
* https://www.gust.org.pl/projects/e-foundry/latin-modern/download
* https://www.unicode.org/standard/standard.html


# generate svg from font

## use inkscape

1. set text font to latin modern mono;
2. click `Object` -> `Object to path` ;
3. save as `Plain SVG` ;

> Note: The default unit in Inkscape is millimeters (`mm`), while in svg2tikz it is centimeters (`cm`).

## use fonts2svg

generate svg from Open True Type font (use package `opentypesvg`):

```shell
fonts2svg lmmonolt10-regular.otf -av
```

Convert the generated SVG files to TikZ files, and

```TeX
\def\globalscale{0.01350000}
```

# generate pgf from svg

```shell
# full mwe
svg2tikz lmm_8.svg --output lmm_export_8.tikz

# just `scope' env
svg2tikz --codeoutput=codeonly lmm_8.svg --output lmm_export_8.tikz

# batch mode(powershell)
for ($i=0; $i -le 9; $i++) {svg2tikz --codeoutput=codeonly lmm_$i.svg --output lmm_export_$i.tikz}
```
