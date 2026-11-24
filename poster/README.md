# Poster kit

A conference poster in the house style, with a preset for each A* venue. The rules, venue sizes and layout families are in [GUIDELINE.md, section 14](../GUIDELINE.md#14-posters). All example content and data are invented.

For other kinds of posters, see the [A* poster styles gallery](https://claude.ai/artifact/UB3VM4DruyVZcn5Avxb5M2): real ICML 2026 posters grouped by layout family, and the main template repos. For NeurIPS, the house style here stays the standard.

| Demo | Preset | Layout |
|---|---|---|
| [18_poster.png](../demos/18_poster.png) | `neurips` (140 × 90 cm) | 3 columns |
| [18b_poster_cvpr.png](../demos/18b_poster_cvpr.png) | `cvpr` (84 × 42 in) | 4 columns |
| [18c_poster_a0.png](../demos/18c_poster_a0.png) | `a0` (AAAI, IJCAI, ACL, UAI) | 2 columns, portrait |
| [18d_poster_workshop.png](../demos/18d_poster_workshop.png) | `neurips-workshop` (61 × 85 cm) | 2 columns, compact |
| [18e_poster_sizes.png](../demos/18e_poster_sizes.png) | every preset, drawn to the same scale | |

## Start a poster

1. Copy `template/` next to your paper and rename it, for example `my_paper_poster/`.
2. In `poster.tex`, set the venue: `\providecommand{\venue}{cvpr}`. Presets:

   | Key | Size | Layout |
   |---|---|---|
   | `neurips`, `neurips-workshop` | 140 × 90 cm; 61 × 85 cm | 3 columns; 2 columns, compact |
   | `iclr`, `iclr-workshop` | 185 × 90 cm; 61 × 91 cm | 4 columns; 2 columns, compact |
   | `icml-48`, `icml`, `icml-72`, `icml-workshop` | 48, 60, 72 × 36 in; 24 × 36 in | 3, 3, 4 columns; 2 columns, compact |
   | `cvpr`, `iccv`, `cvpr-workshop` | 84 × 42 in; 42 × 21 in | 4 columns; 3 columns, compact |
   | `aaai`, `ijcai`, `acl`, `emnlp`, `uai`, `a0` | A0 portrait | 2 columns |
   | `kdd`, `kdd-workshop` | 3.5 × 3 ft; 3 × 3.5 ft | 3 columns; 2 columns, compact |
   | `custom` | define `\posterwidth`, `\posterheight` (cm), `\posterscale` and `\posterlayout` | `columns3`, `columns4` or `portrait2` |

   Sizes were read from the venues' pages on 2026-11-24 (GUIDELINE.md, 14.1). Check your venue's current page, and use `custom` for ECCV, whose size comes with the acceptance e-mail.
3. Replace the header text and the nine `\Block...` macros. The layout places them and numbers them in reading order; compact presets drop blocks 2, 5 and 8.
4. Replace the example plots in `figures.tex` with your data. Keep the styles from `posterplots.tex`: `s ours`, `s a`, ..., `b ours`, `b a`, ..., `\Dumbbell`. Insert figures with `\includegraphics[width=\linewidth, height=\teaserH, keepaspectratio]{...}` so they respect the layout's height cap.
5. Put the conference logo in `fig/logos/conference.png` (a grey placeholder shows until then) and set the two QR-code URLs.
6. Build: `tectonic -X compile poster.tex`. With plain `xelatex`, compile twice (the body height is read from the previous run). On Overleaf, zip the folder, upload it, and compile `poster.tex` with XeLaTeX.

## Files

| File | Contents | Edit? |
|---|---|---|
| `template/poster.tex` | Venue, header text, footer line, the nine blocks | Yes |
| `template/figures.tex` | Example plots and their (invented) data, one macro per plot | Yes |
| `template/venues.tex` | Page size, type scale and layout of each preset | To add a venue |
| `template/layouts/` | `columns3`, `columns4`, `portrait2`: column widths, block order, figure sizes; `header.tex`: the header and the body height | Rarely |
| `template/posterstyle.tex` | Fonts, colours, blocks and helpers (`\take`, `\ours`, `\smallprint`, `\chip`, `\refcell`, `\takeaway`, `\largertext`, `\placeholder`, `\logofile`, `\minsize`) | Rarely |
| `template/posterplots.tex` | The guide's colour roles, chrome, legends, bar shades and hatches, `\famlabel`, `\Dumbbell`, all scaled by `\posterscale` | No |
| `svg2tikz.py` | Turns a flat SVG logo into a TikZ macro that prints as vectors | |

## Fitting

Every column is a fixed-height box that ends 1.8 cm (at scale 1.36) above the page edge; `\blockgap` spreads spare height between blocks. After each build, search the log:

- `Overfull \vbox`: a column ran long. Shrink a figure (the size macros at the top of `layouts/<layout>.tex` can be redefined in `poster.tex`), cut text, or lower `\posterscale` a little.
- `Overfull \hbox`: something is wider than its column, usually a figure or a table.
- `The heading of block N wraps`: shorten that block's title.

If a column has spare height, `\largertext` at its top steps its body text up one size; plot text stays the same.

## Logos

```bash
python3 poster/svg2tikz.py downloaded_logo.svg template/fig/logos/funderlogo.tex funderlogo
```

Then `\input{fig/logos/funderlogo}` in the preamble and `\funderlogo{3cm}` where it goes. Look at the result next to the original: the script reports what it skipped. Funders normally go in the footer as text; add a logo only if a funder requires it, and check its usage policy first, because some organisations require a written licence.
