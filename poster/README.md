# Poster kit

A conference poster in the house style. The rules are in [GUIDELINE.md, section 14](../GUIDELINE.md#14-posters), and [demos/18_poster.png](../demos/18_poster.png) shows the template as it builds. All example content and data are invented.

## Start a poster

1. Copy `template/` next to your paper and rename it, for example `my_paper_poster/`.
2. In `poster.tex`, set the page size for your venue, then replace the header text and the nine blocks.
3. Replace the example plots in `figures.tex` with your data. Keep the styles from `posterplots.tex`: `s ours`, `s a`, ..., `b ours`, `b a`, ..., `\Dumbbell`.
4. Put logos in `fig/logos/` (`conference.png`, `funder.png`, `compute.png`; missing files show as grey placeholders) and set the two QR-code URLs.
5. Build: `tectonic -X compile poster.tex`. On Overleaf, zip the folder, upload it (New Project, Upload Project) and compile `poster.tex` with XeLaTeX.

## Files

| File | Contents | Edit? |
|---|---|---|
| `template/poster.tex` | Page size, column widths, plot sizes, accent colour, header, all block text | Yes |
| `template/figures.tex` | Example plots and their (invented) data, one macro per plot | Yes |
| `template/posterstyle.tex` | Fonts, colours, numbered blocks, helpers (`\take`, `\smallprint`, `\chip`, `\refcell`, `\takeaway`, `\largertext`, `\placeholder`, `\logofile`) | Rarely |
| `template/posterplots.tex` | The guide's colour roles, chrome, legends, bar shades and hatches, `\famlabel`, `\Dumbbell` in pgfplots | No |
| `svg2tikz.py` | Turns a flat SVG logo into a TikZ macro that prints as vectors | |

## Fitting

Every column is a fixed-height box. After each build, search the log for `Overfull`. An `Overfull \vbox` means a column ran long: shrink a plot height in `poster.tex` (`\rowH`, `\gridH`, `\barH`, `\ablH`), or cut text. If a column has spare height, `\largertext` at its top steps its body text up one size; plot text stays the same.

## Logos

```bash
python3 poster/svg2tikz.py downloaded_logo.svg template/fig/logos/funderlogo.tex funderlogo
```

Then `\input{fig/logos/funderlogo}` in the preamble and `\funderlogo{3cm}` in the header. Look at the result next to the original: the script reports what it skipped. Check each logo's usage policy first, because some organisations require a written licence.
