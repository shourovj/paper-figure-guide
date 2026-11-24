# Figure guideline for NeurIPS, ICML, ICLR, and CVPR papers

Version 1.4, 2026-11-24. The code that applies these rules is [paperplot.py](paperplot.py), and every rule is shown in [demos/](demos/) (made by [make_demos.py](make_demos.py), with invented data only). Posters follow Section 14 and the kit in [poster/](poster/), with presets for NeurIPS, ICLR, ICML, CVPR, ICCV, ECCV, AAAI, IJCAI, the ACL family, KDD and UAI.

```python
import matplotlib.pyplot as plt
import paperplot as pp

pp.use("cvpr")                                          # or icml, neurips, iclr, iccv
fig, ax = plt.subplots(figsize=pp.size("single", h=2.0))
pp.line(ax, x, y, "ours", lo=y_lo, hi=y_hi)
pp.save(fig, "figures/my_plot")                         # .pdf + .png, then automatic checks
```

## 1. Start with the claim

1. Write the one sentence the figure must prove before you plot anything. If it needs two sentences, make two figures or two panels.
2. Choose the form from the claim (table below). If exact values are the point, use a table.
3. Make "ours" the first thing the eye lands on. A reviewer skimming the page should get the claim from the figure and its caption alone.

| The claim is about | Use | Demo |
|---|---|---|
| Progress over training or steps | Line + band, small multiples per dataset | 01 |
| Selective prediction or abstention | Risk-coverage curve with AURC in the legend | 02 |
| A few methods on a few datasets | Grouped bars from zero, or dots with CIs | 03, 04 |
| Aggregate performance over many tasks | Interval plot (IQM, mean, optimality gap) | 04 |
| Before vs. after for many categories | Dumbbell, sorted by gain | 05 |
| Calibration | Reliability curve + confidence histogram | 06 |
| Two categorical factors | Annotated heatmap | 07 |
| Run-to-run distribution and significance | Violin + points + paired test | 08 |
| Trade-off between two metrics | Scatter with Pareto front | 09 |
| What each component contributes | Ablation bars, one hue getting stronger | 10 |
| Robust comparison of score distributions | Performance profile | 11 |
| Hyperparameter sensitivity | Log-x line with baseline band and default marker | 12 |
| Part-to-whole outcomes | 100% stacked bars | 13 |
| How the method works | Method figure with a worked example (Section 9) | 15 |
| The whole method on one page | Multi-panel overview figure (Section 9) | 17 |
| What the model actually says | Qualitative response cards (Section 10) | 16 |
| The whole paper on one page | Conference poster (Section 14) | 18 |

Avoid pie charts, 3D plots, radar charts for numeric comparison, and dual y-axes. Split two scales into two panels.

## 2. Author at the final printed size

Set `figsize` to the printed size and include the PDF at full width, so 8 pt in code is 8 pt on paper. Large canvases shrunk in LaTeX make fonts and lines unpredictable.

| Venue | Column (in) | Full width (in) | Source |
|---|---|---|---|
| CVPR / ICCV | 3.28125 | 6.875 | `cvpr.sty` in this repo |
| ICML | 3.25 | 6.75 | `icml2025.sty` |
| NeurIPS | one column | 5.5 | `neurips_2023.sty` |
| ICLR | one column | 5.5 | `iclr2026_conference.sty` |

Check these against each year's kit. Typical heights: a single-column plot 2.0-2.4 in, a row of small multiples 1.3-1.7 in.

```latex
\includegraphics[width=\linewidth]{figures/my_plot.pdf}   % one column
\includegraphics[width=\textwidth]{figures/my_plot.pdf}   % inside figure*
```

Never use `bbox_inches="tight"`: it changes the output width, so LaTeX rescales the figure. `paperplot` uses constrained layout at the exact size.

## 3. Text

- Axis labels 8 pt, ticks and legend 7-7.5 pt, nothing below 6 pt.
- Computer Modern serif by default, matching the math in the paper. Use `font="sans"` for slides and posters (Section 14). Long model responses in qualitative cards are set in sans. Overview diagrams use `font="diagram"`: Arial labels with Computer Modern math, so symbols match the paper's equations.
- Lowercase axis labels with units: `accuracy (%)`. Capitalize only proper names and method names.
- Regular weight in plots, with bold only for panel tags. Method figures use bold component labels, and qualitative cards use bold titles.
- No figure titles; the caption does that job. Panel titles name the dataset or condition.
- Use math mode for real minus signs and symbols: `$-1.2$`, not `-1.2`.

## 4. Color and encoding

The fixed slots below passed a palette validator (all-pairs, white background): worst deuteranopia ΔE 7.9, worst normal-vision ΔE 18.1, all contrasts at least 3:1. A ΔE below 8 is acceptable only with a second encoding, so every slot has one.

| Role | Hex | Marker | Line | Hatch | Use |
|---|---|---|---|---|---|
| `ours` | `#2E7BD6` | circle | solid, thicker | none | The proposed method, always |
| `a` | `#C9302C` | square | solid | `////` | Strongest baseline |
| `b` | `#BF8700` | triangle | dashed | `\\\\` | Baseline |
| `c` | `#A23BA6` | diamond | dash-dot | dots | Baseline |
| `d` | `#159E86` | down triangle | dotted | `xxxx` | Baseline |
| `base` | `#8C8C8C` | circle | solid | none | Untreated model, background points |
| `oracle` | `#333333` | none | long dash | none | Upper bound or reference |

- A method keeps its color in every figure in the paper. Assign slots once and never by rank.
- At most five methods in one panel. Beyond that, show the best few and move the rest to the supplement.
- Variants of one idea share a hue. Ablations use tints of `ours`.
- Sequential data: `viridis`. Signed data: `BrBG`, centred at exactly zero. Never `jet` or rainbow.
- Do not use red and green to mean good and bad in heatmaps, because colorblind readers confuse them and red is a method color.
- Light bar shades do not separate methods by color alone. At the default shades the validator gives a worst normal-vision ΔE of 8.0, a worst colorblind ΔE of 3.8, and contrast of 1.6-2.4:1 against white. Every baseline bar therefore keeps its hatch, drawn in the full role color.
- Text is ink or muted gray, not the series color. The one exception is a wrong span in a qualitative card, which is red and underlined.

## 5. Marks and chrome

- Thin full frame (0.6 pt), no tick marks, light solid grid (0.5 pt) behind the data.
- 3-5 ticks per axis. Remove the grid along a categorical axis.
- Lines 1.2 pt, `ours` 1.7 pt, nothing under 0.5 pt (ICML template).
- Bands: same hue at 18% opacity, no edge. Whiskers: 0.6 pt dark with small caps.
- Bars use light shades, mixed with white so gridlines do not show through: 46% of the role color for baselines and 66% for `ours`, so ours still reads first (`pp.bar`). Use small white gaps, no outlines, and hatches in the full role color.
- Markers only with few x positions. Dense curves rely on color and dash.

## 6. Honest axes

- **Bars start at zero.** If the interesting range is narrow, switch to dots or dumbbells, which can use a tight axis.
- Lines, dots, and heatmaps may use a tight range. Say so in the axis or caption if it could mislead.
- Log axes are labeled as such, with readable powers.
- Panels being compared share y-limits. Use `sharey=True` wherever units match.
- Put "lower is better" on the axis or title if the direction is not obvious.

## 7. Uncertainty and statistics

- No point estimate without an interval when runs vary. Every band or whisker is defined in the caption: statistic, level, number of seeds.
- Prefer 95% bootstrap CIs (`pp.boot_ci`) over bare standard deviations. With few runs on many tasks, report IQM and optimality gap as interval estimates (`pp.iqm`), following Agarwal et al.
- Show individual runs when n is below about 30 (demo 08).
- Use paired tests for paired runs (`pp.paired_p`, a sign-flip permutation test). Print the actual p-value, not stars. Bracket only the comparisons the claim needs, and correct for multiple comparisons (for example Holm) when you make several.
- State exactly what is averaged over and what the unit of variation is.

## 8. Legends, labels, and panels

- Put the legend at the best location: the free spot inside the plot that covers no line, band, bar, or label. `pp.legend` finds it and verifies it. Call it last, after the limits are set.
- If no spot is free, add headroom by raising the y-limit while keeping the ticks in the real range (demos 02, 03), and stop reference lines short of the free area (demo 12).
- Multiple panels: one legend, `Ours` first, in whichever panel has room.
- A legend goes below the figure only when the plot truly has no free space, as with 100% stacked bars or dense small multiples (demos 01, 13). `pp.legend` falls back to this by itself.
- Few, well-separated curves can use direct labels instead of a legend.
- Never put a label or legend on top of data. `pp.save` warns if you do.
- Label values only where the reader needs them, usually `ours` or the best baseline. Otherwise use a table.
- Show y-labels only on the leftmost panel with shared axes. Use one shared x-label (`pp.shared_xlabel`).
- Use `pp.tag` for (a), (b), (c) only when the text refers to individual panels.

## 9. Method figures

Demo 15 draws this style with `pp.canvas`, `pp.box`, `pp.trapezoid`, `pp.arrow`, `pp.tokens`, `pp.score_card`, and `pp.image`. The rules also apply in draw.io or TikZ.

- Read left to right: the input on the left, one main path, the final answer on the right.
- Use two tones. Existing parts are pale gray (`base`), and everything the paper adds is blue (`ours`), matching the plots.
- Mark what is new twice: a dashed outline around the added module, and blue arrows for its path. Existing paths use ink arrows.
- Arrows are thick (about 1.3 pt), straight or right-angled, and do not cross.
- Run one real example through the pipeline: the actual image, the actual question, tokens as small boxes, real numbers inside the score cards, and the final answer as text with the deciding word in bold.
- Put the key equation in the flow, at the place where it happens, so the cards become its terms.
- Rounded boxes for modules, trapezoids for encoders. Labels are short and bold at 7-8 pt, never below 6 pt.
- Export as vector PDF at the printed width. Photos inside it follow the raster rules in Section 11.

### Multi-panel overview figures

Demo 17 shows the calm, panelled style for a figure that explains the whole method at once. It uses `pp.panel`, `pp.stack`, `pp.cube`, `pp.diamond`, `pp.frozen`, `pp.trainable`, `pp.cells`, and `pp.distribution`.

- **Panels.** Panel (a) holds the full pipeline across the top. Panels (b) and (c) hold the details underneath: the losses, and how the model is built. Main panels have a dashed light-gray frame and a bold 9 pt title such as "(a) Teacher-student distillation". Sub-panels have a thin solid frame and a numbered 7.5 pt title, such as "1. Answer distillation".
- **Muted fills, soft outlines.** Fill shades are 0.1-0.2 of the role color, and outlines about 0.6 (`edge=0.6`), so no box shouts. Use at most four hue families: gray for existing or frozen parts, blue for ours or trainable parts, lavender (`c`) for one data stream such as corrupted inputs, and amber (`b`) for a highlight.
- **The same color means the same thing in every panel.** The student is blue in (a), in the bar charts of (b), and in the layer strip of (c). Amber marks the matched layers in both the teacher and student strips.
- **Shapes carry meaning.** Trapezoids are encoders and rounded boxes are models. Stacked frames are a dataset or batch, and grid cubes are tokens or latents. A diamond is a choice between inputs, and pills are targets or a one-line pipeline.
- **Icons are small.** Use a gray snowflake for frozen parts and an amber flame for trainable ones, in a corner of the box. Amber, so the flame never reads as the blue of "ours". The words "frozen" and "trainable" also appear in the box, so the icons are never the only cue.
- **Show the data, not just names.** Draw the actual pictures, small output distributions with labeled bars, and layer strips with indices. Write the indices above the cells and the mapping inside them.
- **Math sits where it happens.** Write each output as an equation next to its arrow ($p_T = T(z)$). Put each loss in the sub-panel that explains it, and the total loss in the box the arrows feed.
- **Arrows** are 1.0 pt. Draw them in ink for the existing path, in blue for ours, and in the data color for a side stream. A dashed double-headed arrow means matching between two parts. Label a branch probability on its line ($p = 0.3$).
- **Text** is 7.5 pt bold for component names, 6.5 pt regular for details, and muted gray for side notes. Leave white space between panels rather than adding more boxes.
- Full width, about 4.3 in tall. Make a figure this large only when it is the paper's main method figure.

## 10. Qualitative examples

Demo 16 builds this layout with `pp.text_card` and `pp.badge`.

- Layout: image top left with the reference below it, the question in a band across the top right, and model responses stacked under the question.
- One pale card per model, in that method's color: `ours` blue, `base` gray, reference amber. No dark borders.
- Each card has a bold title and a small round badge, with the response in 7 pt sans.
- Mark only the wrong words, in red and underlined. Red alone is hard to see with deuteranopia. Leave correct text alone.
- Show every model on the same input, with outputs verbatim. If you shorten one, write `[...]` and say so in the caption.
- Say how examples were chosen, and include at least one failure of your own method in the paper or supplement.

## 11. Export

- Plots are vector PDF, with `rasterized=True` only for very dense scatters (over about 5k points).
- Raster content: PNG for sharp images, JPEG for photographs, at least 300 dpi at printed size.
- Fonts must be embedded and never Type 3. `pp.use` sets `pdf.fonttype = 42`, and `pp.save` checks with `pdffonts`.
- **ICML's template asks for embedded Type-1 only**, and matplotlib's default embeds TrueType. For ICML, render with `pp.use("icml", tex=True)` on a machine with LaTeX, then run `pdffonts paper.pdf`. NeurIPS objects to Type 3 and to non-embedded TrueType, so embedded TrueType fits its wording.
- Keep the plotting script and data next to the figure, and have the script read the data from a file. Every number in a figure must be regenerable.

## 12. Captions

- First sentence states the takeaway. Then define what is plotted, the band or whisker, n, and any abbreviations.
- Caption goes below the figure. NeurIPS asks for lower-case captions except the first word and proper nouns.
- The figure and caption should make sense without reading the main text.

## 13. Before submission

Automatic in `pp.save`: font size, line width, text clipped by the figure or frame, text collisions, text on lines, legends over data, Type 3 or unembedded fonts.

By hand:

- [ ] One sentence states what this figure proves, and the caption opens with it
- [ ] `ours` has the same color in every figure
- [ ] Bars start at zero, compared panels share limits
- [ ] Every band and whisker is defined, with n
- [ ] `pp.print_check(png)` output is readable in grayscale and deuteranopia
- [ ] Readable at 100% zoom on a laptop and on a printed page
- [ ] Figure regenerates from its script and data
- [ ] `pdffonts paper.pdf` shows no Type 3 and everything embedded
- [ ] Anonymous submission: no names, paths, or logos inside the figure

## 14. Posters

The kit in [poster/](poster/) applies these rules. `poster/template/` is a beamerposter template for Overleaf with a preset for each A* venue: pick the venue and it sets the page size, the type scale and the layout. The plots use this guide's styles in pgfplots (`posterplots.tex`), and `poster/svg2tikz.py` turns SVG logos into vector TikZ. Demos 18-18e show the presets with invented content; [18e](demos/18e_poster_sizes.png) draws every venue's poster to the same scale.

### 14.1 Venue sizes and rules

Read on 2026-11-24 from each venue's own pages (links under Sources). Venues change these from year to year, and from one venue city to the next. Read the current page before you design, and never print larger than its maximum.

| Venue | Main-conference poster | Workshop poster | Preset |
|---|---|---|---|
| NeurIPS 2026 | at most 140 × 90 cm, landscape | 61 × 85 cm, portrait | `neurips`, `neurips-workshop` |
| ICLR 2026 | at most 190 × 90 cm, landscape; its print partner asks for 185 × 90 | at most 61 × 91 cm, portrait | `iclr` (185 × 90), `iclr-workshop` |
| ICML 2026 | suggested 48, 60 or 72 × 36 in (122, 152 or 183 × 91 cm), landscape | at most 24 × 36 in (61 × 91 cm), portrait | `icml-48`, `icml`, `icml-72`, `icml-workshop` |
| CVPR 2026 | 84 × 42 in (213 × 107 cm), 2:1 landscape | half size, 42 × 21 in (107 × 53 cm); main papers may use it too | `cvpr`, `cvpr-workshop` |
| ICCV 2025 | 84 × 42 in, landscape | the same | `iccv` |
| ECCV 2026 | not published on the site (only the upload rules are) | not published | `custom`, with the size in your acceptance e-mail |
| AAAI-26 | no larger than A0 (84.1 × 118.9 cm), portrait | set by each workshop | `aaai` |
| IJCAI 2025 | A0, portrait preferred; IJCAI-ECAI 2026 had not posted its rules | not published | `ijcai` |
| ACL 2025, EACL 2026 | A0, portrait | not published | `acl` |
| EMNLP 2025, 2026 | no size published; ACL-family events use A0 portrait | not published | `emnlp` |
| KDD 2026 | 3.5 × 3 ft (107 × 91 cm) of board per paper, either orientation | 3 × 3.5 ft (91 × 107 cm) | `kdd`, `kdd-workshop` |
| UAI 2026 | A0, portrait | not published | `uai` |

- When two official pages disagree, design to the smaller size (ICLR 2026: 185 × 90 cm).
- None of NeurIPS, ICLR or ICML sets a different size for spotlight or oral posters.
- Mounting differs. ICLR and ICML forbid self-adhesive posters and supply tape. NeurIPS 2026 used command strips in Sydney, pins in Atlanta and adhesive strips in Paris. KDD 2026 supplied pushpins, and tape at its poster receptions.
- Material differs. AAAI-26 required slightly rigid paper and refused fabric, foam board, laminated, adhesive-backed and plain lightweight paper posters. KDD 2026 printed only on fabric, through its own service. CVPR's service prints on 8 mil satin paper.
- ICCV is held in odd years and ECCV in even years, so their newest pages are a year apart.

### 14.2 Choose the layout from the poster's shape

| Shape | Venues | Layout | Reading order | Scale |
|---|---|---|---|---|
| About 2:1 landscape | CVPR, ICCV, ICLR, ICML 72 in | `columns4`: four equal columns | 1-2, 3-5, 6-7, 8-9 | 1.6-1.9 |
| 1.2-1.7 landscape | NeurIPS, ICML 48 and 60 in, KDD | `columns3`: a wider middle column for the method and main result | 1-3, 4-6, 7-9 | 1.36-1.4 |
| Portrait A0 | AAAI, IJCAI, ACL-family, UAI | `portrait2`: two columns | 1-5, 6-9 | 1.12 |
| Small: workshops and CVPR's half size | NeurIPS, ICLR, ICML and KDD workshops; CVPR workshops | `portrait2` or `columns3`, compact | six blocks | 1.1-1.45 |

- Bigger posters get bigger type, not more text. The presets are tuned so the template's nine blocks fill about 85% of every column, as they do on the reference NeurIPS 2026 poster.
- Small posters drop blocks instead of shrinking type. Compact mode keeps six: the problem, how the baselines fail, the method, the main result, the table, and the ablation with the takeaway. The rest renumber themselves.
- CVPR's poster page recommends "a 3 or 4 column layout", little text, a few large figures, and not a copy of the paper. That holds for every venue.
- Each figure takes a share of the column width, capped at a share of the column height, so a plot never outgrows a short, wide column. Insert your own with `\includegraphics[width=\linewidth, height=\teaserH, keepaspectratio]{fig/teaser}`.
- The column height comes from where the columns start on the page, so no preset needs it set by hand.

Type sizes for each preset, in pt (Helvetica is set 5% smaller than nominal):

| Presets | Scale | Body (`\small`-`\normalsize`) | Small print | Block headings | First title line |
|---|---|---|---|---|---|
| `neurips`, `icml`, `icml-48` | 1.36 | 28-34 | 24 | 49 | 90 |
| `kdd` | 1.40 | 29-35 | 24 | 50 | 93 |
| `icml-72`, `iclr` | 1.60-1.62 | 33-40 | 28 | 57-58 | 106-107 |
| `cvpr`, `iccv` | 1.88 | 39-47 | 32 | 67 | 124 |
| `a0`, `aaai`, `ijcai`, `acl`, `emnlp`, `uai` | 1.12 | 23-28 | 19 | 40 | 74 |
| `cvpr-workshop` | 1.10 | 23-27 | 19 | 39 | 73 |
| `neurips-workshop` | 1.20 | 25-30 | 21 | 43 | 79 |
| `iclr-workshop`, `icml-workshop` | 1.30 | 27-32 | 22 | 47 | 86 |
| `kdd-workshop` | 1.45 | 30-36 | 25 | 52 | 96 |

### 14.3 Layout families at A* venues

From 13 ICML 2026 posters picked to show distinct layouts (posterly's anchor list) and the main template repos. Each poster's image is at `icml.cc/media/PosterPDFs/ICML%202026/<id>.png`.

The [A* poster styles gallery](https://claude.ai/artifact/UB3VM4DruyVZcn5Avxb5M2) shows these posters and the template repos side by side, with a note on what each is worth borrowing. Use it as a reference for other venues and later posters. For NeurIPS, the standard stays the house style of the `neurips` preset, which reproduces the author's NeurIPS 2026 poster.

| Family | What it is | Use it for | Examples |
|---|---|---|---|
| Columns of numbered blocks (this kit) | 3-4 columns, one claim per block | Results-driven papers; the default | FRACTAL (62396); CAM, CVPR 2015 ([bolei_awesome_posters](https://github.com/zhoubolei/bolei_awesome_posters)); [itailang/poster_guide](https://github.com/itailang/poster_guide) |
| Columns plus one focal device | A row of big numbers, a closing take-home band, a question banner, or a coloured middle column | When one number or one sentence carries the paper | Dropout universality (65205): three numbers and a closing band; ArcDAE (60839): take-home band; point clouds (60655): centre stage; Thoughtbubbles (64621): one large statement; BRIDGE (66579): question hero |
| Boxless blocks | Coloured titles over thin rules, no frames | A lighter look in the same structure | [Gemini](https://github.com/anishathalye/gemini) and the Stanford template built on it |
| Billboard | The finding in plain English across the middle, details in side strips | Workshops, or a second poster | [#betterposter](https://github.com/rafaelbailo/betterposter-latex-template) |
| Editorial cards | Numbered cards of varied size with large numerals | Benchmarks and short findings; heavy frames need short content | TadA-Bench (64736); layer scaling (63300) |
| Question as the title | A short question in huge type over text sections | Position papers | What is AI reasoning? (67122) |

- Avoid dark canvases (65626): they print and photograph worse, and this guide keeps white. Avoid four columns of tables (PhaseCoder, 61119): nothing in them reads from 2 m.
- Moves that work in any family: titles that ask a question or state a claim; a one-line TL;DR under the title; a closing take-home sentence (the kit's takeaway panel); and Bolei Zhou's 3-minute test, where anything you would skip while pitching comes off the poster.
- Automatic drafts: [Paper2Poster](https://github.com/paper2poster/paper2poster) turns a PDF into an editable .pptx, and [posterly](https://github.com/Chenruishuo/posterly) and [posterskill](https://github.com/ethanweber/posterskill) build HTML posters with agents. Treat their output as a first draft and apply this section.

### 14.4 Text

- One claim per block: a one-line intro, the figure, a one-line takeaway, and at most two or three short bullets. Prefer numbers to sentences.
- Block titles state the finding ("Remove any piece and training collapses"), not the topic ("Ablation"). They must fit on one line next to the number. The build warns "The heading of block N wraps", and narrow columns hold about 26-30 characters.
- All text in Helvetica (TeX Gyre Heros under XeLaTeX), with Times-style maths (`newtxmath`) as in the paper. Latin Modern is too thin at poster scale.
- Text is ink. The accent colours only the first title line, headings, number discs and rules.
- Each number in the text names what it measures: the method variant and the benchmarks it covers. "1.5B, multi-reward + KL-Cov: +45.9 pp over INTUITOR on GSM8K; within 1.7-6.6 pp of supervised GRPO-GT on math", not "+45.9 pp; within 1.7-6.6 pp", when the table's bold entry is a different variant.
- Limitations are said at the poster, not printed on it.

### 14.5 Colour and blocks

- One accent for headings: burnt orange `#BF5700` (white text on it is 4.6:1). Darker oranges, brick reds and blues were tried and dropped: red tones clash with a red baseline, and blue clashes with `ours`.
- Blue, the `ours` role, is reserved for our method and our key results: `\ours{...}` sets them in a slightly darker shade than the plot lines, and the takeaway sits on a light-blue panel. Titles never use blue.
- White page. Each block is a white rounded box with a bold black outline (5 pt at scale 1.36), its number and heading centred over an accent rule. Cards, equation boxes and chips are flat light-grey panels (`#EFEFEF`).

### 14.6 Plots

- Every plot rule in this guide applies. Line widths, markers and gaps scale with `\posterscale` through `\pu` (1 cm at scale 1.36). Reference values at 1.36: ours 6.3 pt, baselines 4.6 pt, reference lines 3.9 pt, frame 2.3 pt, grid 1.9 pt.
- Plot text uses the poster's sizes: ticks and legends `\small`, axis labels and panel titles `\normalsize`, value labels `\footnotesize`. If a plot looks crowded, use fewer panels, not smaller text.
- Draw plots natively in pgfplots (`posterplots.tex`), so they use the poster's fonts at exact sizes. From matplotlib, export at the printed panel size with the sizes above.
- One legend per figure, below it, with ours first. Under a line plot, text lines that start with each series' line sample (`\keyline`) can be the legend and the explanation at once.
- In a grid of panels, give one shared y label and short row labels beside the ticks. On a wide poster the rows are short, and a rotated label per row would collide.
- In narrow columns, let long axis labels wrap to the panel width (`xlabel style={text width=\plotW, align=center}`), and use fewer ticks.
- When category labels collide, split them into two levels: the size on the tick, the family underneath (`\famlabel`).
- Reference bars (oracle, supervised) at 30%, so ours reads first. With four or more bars per group, print values on ours only.
- An ablation whose claim is a before/after change is a dumbbell. If an ablated variant equals another method on the poster, it keeps that method's colour.
- Single runs get no bands. Say so when presenting.

### 14.7 Header and footer

- Left: the conference logo. Right: two QR codes, each labelled (project page, code). Funders and compute providers go in the footer as one line of text; add their logos only if a funder requires it.
- Check each logo's usage policy before printing. DARPA, for one, requires a written trademark licence for any use of its logo.
- First title line in the accent, second in black; authors bold, each name in `\mbox` so a wrapped list never splits a name; affiliations on one line.
- Use vector logos where possible: `python3 poster/svg2tikz.py logo.svg fig/logos/x.tex xlogo`. Many sites serve a white logo for a dark header; recolour it for white.

### 14.8 Online materials

| Venue | Upload | Format | Deadline |
|---|---|---|---|
| CVPR 2026 | 5-minute YouTube video, thumbnail, optional poster image | PNG, at most 5120 × 2880 px and 10 MB | video May 20, images June 3 |
| ECCV 2026 | 5-minute video (12 for orals), thumbnail, optional poster image | PNG, at most 5120 × 2880 px and 10 MB | August 31, AOE |
| ICCV 2025 | Thumbnail, poster image, 5-minute video | Not stated | October 8, AOE |
| NeurIPS, ICLR, ICML 2026 | Virtual poster and thumbnail | Not stated | At least a week before |
| ACL 2025 | Poster PDF, video and slides on Underline | PDF | June 29 |

- `pdftoppm -png -r 60 poster.pdf poster` turns an 84 × 42 in poster into 5040 × 2520 px, about 1 MB for the template.
- For the thumbnail, crop the teaser or the main result. CVPR asks for "an eye-catching graphic from your paper".

### 14.9 Printing and the session

- Order early. Print services close one to four weeks ahead: CVPR 2026's early-bird price ended on May 17 and its online orders closed on May 29, ahead of a June 3 start; ICML 2026's partner closed on June 15.
- Send a PDF at full size, with figures as vectors and raster images at 100 dpi or more at the printed size (the CVPR 2026 and ICML 2025 services both asked for 100 dpi or vector). No bleed. CVPR's service also wants your name and paper ID in the job name.
- Print a proof at A3 and read it from 1 m. Scan the QR codes from 2 m on the full-size print.
- Put the poster up no earlier than allowed: 30 minutes before the session at NeurIPS 2026, one hour at ICLR 2026.
- Carry paper in a tube. Fabric folds into a suitcase, but not every venue accepts it.

### 14.10 Build and check

- Build with `tectonic -X compile poster.tex` (XeLaTeX). The body height is read from the previous run, so with plain `xelatex` compile twice; tectonic and latexmk rerun on their own. On Overleaf, upload the folder and set the compiler to XeLaTeX.
- [ ] The log has no `Overfull \vbox` (a column ran long), no `Overfull \hbox`, and no "heading of block N wraps" warning
- [ ] Every number traces to a paper table or a data file, and the plotted values match the source data
- [ ] Each number in the text names the method variant and the benchmarks it covers
- [ ] No block contradicts another; for example, a bullet saying two baselines fail the same way next to a plot where they fail in opposite directions
- [ ] Imported paper figures agree with the poster's equations (notation, argument order, KL direction)
- [ ] The QR codes decode from the PDF to the right URLs, the labels under them match, and the links load
- [ ] The page is the venue's current size or smaller
- [ ] Nothing is below `\footnotesize` except inside imported paper figures
- [ ] A proof printed at A3 reads from 1 m
- [ ] Logo licences are checked, and the funding acknowledgment is in the footer

### 14.11 LaTeX pitfalls

- Beamer already defines `\note`, `\logo` and the colour `fg`. Do not reuse those names.
- A `tabular` inside an `\if...\fi` branch inside a frame fails with "Incomplete \ifx", and so does `\qrcode{\macro}`. Build such pieces in the preamble and pass literal URLs. The layouts choose their blocks in the preamble for the same reason.
- `\color` at the start of a tabularx `X` cell opens an empty line. Put `\leavevmode` first (`\refcell`).
- `\rowcolor` with `\extracolsep` leaves white gaps between cells. Use tabularx.
- Under XeLaTeX, `helvet` has no fonts in the TU encoding. Load TeX Gyre Heros through fontspec, as `posterstyle.tex` does.
- In a groupplot, set `/pgf/bar width`, not `bar width`. Nodes inside an axis are clipped unless the axis has `clip=false`.
- A style defined in a pgfplots option list does not reach `\node`. Give such nodes their options directly, as `\famlabel` does.
- `patterns.meta` builds a name from its options, so give it plain values (`\the\hatchSep`), not length registers, or the build stops with "Missing \endcsname".
- TikZ cannot parse `\dimexpr` or `\ifdim`. Compute a size into a length first (`\setlength{\figH}{\teaserH}`) and pass the length.
- A drawn outline adds its line width to a node's size. Leave room for it, or a box the width of its column overflows by that much.

## 15. Where the sources disagreed

| Topic | Swarm-Visualization | arXiv:2609.12278 | figures4papers | Decision |
|---|---|---|---|---|
| Background | `darkgrid` | White, full box, light grid | White, top/right removed | White, thin full box, light grid |
| Text | Bold, 20 pt, LaTeX | Regular CM serif, lowercase | Helvetica, 16-24 pt | Regular CM serif at true 8 pt |
| Canvas | Not set (20 pt fonts imply shrinking) | Small panels | Up to 45×12 in | Exact print size |
| Y-axis on bars | Not specified | Zero (Fig. 8) | Tightened to the data | Zero, or switch to dots |
| Value labels | Not specified | None | On every bar | Selective |
| Bar fill | Seaborn default | Plain fill | Black edges, hatch | Light shades, white gaps, role-colored hatch |
| Ours color | Not specified | Red | Blue | Blue |
| Legend | `loc="best"` | Shared, below | Dedicated panel | Best free spot inside the plot, verified; below only if none |
| Statistics | Wilcoxon annotations | Shaded bands | Optional bands | Intervals always, exact paired p-values |
| File output | 600 dpi `savefig` | Embedded rasters | PNG + PDF | Vector PDF + preview PNG |

Taken from each: from Swarm, best-location legends, paired significance testing and run-level distributions; from arXiv:2609.12278, the overall look, shared legends, baseline bands on sweeps; from figures4papers, semantic color roles, hatches for print, tint-based ablations, consistent helper functions. The method-figure and qualitative-card styles and the light bar shades follow MARINE (arXiv:2402.08680). The multi-panel overview style follows an example diagram the author supplied: a shared-latent decoder distillation figure. Added from wider guidance: exact venue geometry and font rules, validated color, interval estimates, and automated checks. The poster rules (Section 14) follow a UT Austin poster the author supplied as the model layout, and feedback rounds on a NeurIPS 2026 poster.

The venue pages behind Section 14.1 disagreed in places:

| Topic | What the pages said | Decision |
|---|---|---|
| ICLR 2026 size | Poster guide: at most 1.90 × 0.90 m. Print partner: 185 × 90 cm | Design at 185 × 90 cm, which satisfies both |
| ICLR 2026 print deadline | The same page gives April 6 and April 1 | Use the earlier date |
| KDD 2026 deadline | FAQ: "no deadline". Printing page: fabric orders by August 4 | August 4; KDD printed only through its service |
| NeurIPS 2026 page | Covers three venues (Sydney, Atlanta, Paris); Paris affinity sessions use the workshop size | Check the size for your session's venue |
| Body font | The first kit used Times for body text at scale 1.24 | All-Helvetica at larger scales, after feedback that the poster was dull and its type too small |

## Sources

- [Swarm-Visualization](https://github.com/UTAustin-SwarmLab/Swarm-Visualization) (`general_utils.py`, `statistics_utils.py`)
- [Palafox and Fridovich-Keil, arXiv:2609.12278](https://arxiv.org/pdf/2609.12278) (Figs. 4-8)
- [figures4papers](https://github.com/ChenLiu-1996/figures4papers) (`design-theory.md`, `api.md`, `common-patterns.md`)
- [MARINE, Mitigating Object Hallucination in Large Vision-Language Models via Image-Grounded Guidance, arXiv:2402.08680](https://arxiv.org/abs/2402.08680) (method figure, qualitative example, bar shades)
- [Rougier, Droettboom, and Bourne, Ten Simple Rules for Better Figures](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4161295/)
- [Agarwal et al., Deep RL at the Edge of the Statistical Precipice](https://arxiv.org/pdf/2108.13264)
- [Paul Tol's color schemes, via khroma](https://rdrr.io/cran/khroma/man/tol.html), and the Okabe-Ito palette
- Machado, Oliveira, and Fernandes (2009), for the color-vision simulation matrix
- Venue poster pages, read 2026-11-24: [NeurIPS 2026](https://neurips.cc/Conferences/2026/PosterInstructions); [ICLR 2026](https://www.iclr.cc/Conferences/2026/PosterInstructions) and its [printing page](https://iclr.cc/Conferences/2026/PosterSessionOnline-Printing); [ICML 2026](https://icml.cc/Conferences/2026/PosterInstructions) and [ICML 2025](https://icml.cc/Conferences/2025/PosterInstructions); [CVPR 2026 printing](https://cvpr.thecvf.com/Conferences/2026/PosterPrinting) and [uploads](https://cvpr.thecvf.com/Conferences/2026/YouTubeVideoPosterUpload); [ICCV 2025 printing](https://iccv.thecvf.com/Conferences/2025/PosterPrinting) and [uploads](https://iccv.thecvf.com/Conferences/2025/YouTubeVideoPosterUpload); [ECCV 2026 uploads](https://eccv.ecva.net/Conferences/2026/YouTubeVideoPosterUpload) and [FAQ](https://eccv.ecva.net/Conferences/2026/FAQ); [AAAI-26](https://aaai.org/conference/aaai/aaai-26/poster-guidelines/); [IJCAI 2025](https://2025.ijcai.org/?p=1701); [ACL 2025 FAQ](https://2025.aclweb.org/faq/); [EACL 2026 printing](https://2026.eacl.org/participants/poster-printing); [KDD 2026](https://kdd2026.kdd.org/author-presentation-instructions/); [UAI 2026](https://auai.org/uai2026/poster_instructions)
- [A* poster styles gallery](https://claude.ai/artifact/UB3VM4DruyVZcn5Avxb5M2) (the posters and repos below, side by side)
- Poster layouts: 13 ICML 2026 posters (`icml.cc/media/PosterPDFs/ICML%202026/<id>.png`) chosen from [posterly's design axes](https://github.com/Chenruishuo/posterly/blob/main/templates/DESIGN-AXES.md); [itailang/poster_guide](https://github.com/itailang/poster_guide); [zhoubolei/bolei_awesome_posters](https://github.com/zhoubolei/bolei_awesome_posters); [paper2poster](https://github.com/paper2poster/paper2poster); [Gemini](https://github.com/anishathalye/gemini); [betterposter-latex-template](https://github.com/rafaelbailo/betterposter-latex-template); [posterskill](https://github.com/ethanweber/posterskill)
- [beamerposter](https://ctan.org/pkg/beamerposter), and [DARPA's usage policy](https://www.darpa.mil/policy/usage-policy) (logos)
- Author kits: [CVPR 2026 guidelines](https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines), `cvpr.sty`, the ICML 2025 example paper and style, the NeurIPS 2023 template, and the ICLR 2026 template

Venues change their kits. The CVPR 2026 guidelines page has no figure-specific rules beyond using the template, so recheck the current kit before each deadline.
