"""Convert a flat SVG logo to TikZ, so it prints as vectors at any poster size.

    python3 svg2tikz.py logo.svg fig/logos/mylogo.tex mylogo

Then in LaTeX: \\input{fig/logos/mylogo} once in the preamble, and \\mylogo{3cm} wherever the logo
goes (the argument is its height). The macro name must be letters only.

Handles filled shapes, which covers most organisation logos: polygon, polyline, rect (with a
matrix/translate/rotate transform), circle, ellipse, and path with M L H V C S Q T Z (absolute
and relative). Fill colour comes from fill="" or style="fill:...", inherited through <g>.
Anything it cannot convert (strokes, gradients, text, embedded images, <use>, transforms on
groups or paths, arcs) is reported on stderr; check the result against the original either way.
If the SVG only wraps a PNG (some sites do this), extract the PNG and use \\includegraphics.

Always check a logo's usage policy before printing it. Some organisations (DARPA, for one)
require a written trademark licence for any use.
"""
import math
import re
import sys
import xml.etree.ElementTree as ET

NUM = r'[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?'
SVG = '{http://www.w3.org/2000/svg}'
NAMED = {'black': '#000000', 'white': '#FFFFFF', 'red': '#FF0000', 'none': 'none'}
warnings = set()


def fmt(v):
    return ('%.3f' % v).rstrip('0').rstrip('.')


def warn(msg):
    if msg not in warnings:
        warnings.add(msg)
        print('svg2tikz: ' + msg, file=sys.stderr)


def fill_of(el, inherited):
    fill = el.get('fill', inherited)
    style = el.get('style', '')
    m = re.search(r'fill\s*:\s*([^;]+)', style)
    if m:
        fill = m.group(1).strip()
    if el.get('class'):
        warn('class attributes (CSS) are ignored; colours may be wrong')
    s = re.search(r'(?:^|;)\s*stroke\s*:\s*([^;]+)', style)
    stroke = s.group(1).strip() if s else el.get('stroke')
    if stroke not in (None, 'none'):
        warn('strokes are ignored; only fills are drawn')
    fill = NAMED.get(fill.lower(), fill) if fill else fill
    if fill.startswith('url('):
        warn('gradient or pattern fills are not supported; drawn in black')
        return '#000000'
    if re.fullmatch(r'#[0-9a-fA-F]{3}', fill):
        fill = '#' + ''.join(ch * 2 for ch in fill[1:])
    return fill


def matrix_of(tr):
    """SVG transform -> (a, b, c, d, e, f). Supports matrix, translate, scale, rotate."""
    a, b, c, d, e, f = 1, 0, 0, 1, 0, 0
    for name, args in re.findall(r'(\w+)\s*\(([^)]*)\)', tr):
        v = [float(x) for x in re.findall(NUM, args)]
        if name == 'matrix':
            m = v
        elif name == 'translate':
            m = [1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0]
        elif name == 'scale':
            m = [v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0]
        elif name == 'rotate':
            t = math.radians(v[0]); cx, cy = (v[1], v[2]) if len(v) == 3 else (0, 0)
            co, si = math.cos(t), math.sin(t)
            m = [co, si, -si, co, cx - co * cx + si * cy, cy - si * cx - co * cy]
        else:
            warn('transform %s() is not supported' % name)
            continue
        a, b, c, d, e, f = (a * m[0] + c * m[1], b * m[0] + d * m[1], a * m[2] + c * m[3],
                            b * m[2] + d * m[3], a * m[4] + c * m[5] + e, b * m[4] + d * m[5] + f)
    return a, b, c, d, e, f


def path_to_tikz(d):
    t = re.findall(r'[A-Za-z]|' + NUM, d)
    i = 0; out = []
    cx = cy = sx = sy = 0.0; last_c = last_q = None; cmd = None

    def nxt():
        nonlocal i
        v = float(t[i]); i += 1
        return v

    def pt(x, y):
        return '(%s,%s)' % (fmt(x), fmt(y))

    while i < len(t):
        if re.match(r'[A-Za-z]', t[i]):
            cmd = t[i]; i += 1
        rel = cmd.islower(); C = cmd.upper()
        ox, oy = (cx, cy) if rel else (0.0, 0.0)
        if C == 'Z':
            out.append('-- cycle'); cx, cy = sx, sy; last_c = last_q = None
            continue
        if C == 'M':
            x, y = nxt() + ox, nxt() + oy
            out.append(pt(x, y)); cx, cy, sx, sy = x, y, x, y
            cmd = 'l' if rel else 'L'; last_c = last_q = None
        elif C == 'L':
            x, y = nxt() + ox, nxt() + oy
            out.append('-- ' + pt(x, y)); cx, cy = x, y; last_c = last_q = None
        elif C == 'H':
            x = nxt() + ox
            out.append('-- ' + pt(x, cy)); cx = x; last_c = last_q = None
        elif C == 'V':
            y = nxt() + oy
            out.append('-- ' + pt(cx, y)); cy = y; last_c = last_q = None
        elif C in 'CS':
            if C == 'C':
                x1, y1 = nxt() + ox, nxt() + oy
            else:
                x1, y1 = (2 * cx - last_c[0], 2 * cy - last_c[1]) if last_c else (cx, cy)
            x2, y2, x, y = nxt() + ox, nxt() + oy, nxt() + ox, nxt() + oy
            out.append('.. controls %s and %s .. %s' % (pt(x1, y1), pt(x2, y2), pt(x, y)))
            cx, cy = x, y; last_c = (x2, y2); last_q = None
        elif C in 'QT':
            if C == 'Q':
                qx, qy = nxt() + ox, nxt() + oy
            else:
                qx, qy = (2 * cx - last_q[0], 2 * cy - last_q[1]) if last_q else (cx, cy)
            x, y = nxt() + ox, nxt() + oy
            # quadratic -> cubic
            out.append('.. controls %s and %s .. %s' % (pt(cx + 2 / 3 * (qx - cx), cy + 2 / 3 * (qy - cy)),
                                                        pt(x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y)), pt(x, y)))
            cx, cy = x, y; last_q = (qx, qy); last_c = None
        else:
            raise SystemExit('svg2tikz: path command %s (arcs) is not supported; convert arcs to curves first' % cmd)
    return ' '.join(out)


def main(src, dst, name):
    if not re.fullmatch(r'[A-Za-z]+', name):
        raise SystemExit('svg2tikz: the macro name must be letters only')
    root = ET.parse(src).getroot()
    vb = [float(v) for v in re.findall(NUM, root.get('viewBox') or '0 0 %s %s' % (root.get('width'), root.get('height')))]
    shapes, colors = [], {}

    def cname(hexc):
        if hexc not in colors:
            colors[hexc] = '%s%s' % (name, chr(ord('A') + len(colors)) if len(colors) < 26 else str(len(colors)))
        return colors[hexc]

    def emit(fill, body):
        if fill != 'none':
            shapes.append('\\fill[%s] %s;' % (cname(fill), body))

    def walk(el, fill):
        tag = el.tag.replace(SVG, '')
        if tag in ('defs', 'title', 'desc', 'metadata', 'style', 'clipPath', 'mask'):
            if tag in ('style', 'clipPath', 'mask'):
                warn('<%s> is ignored' % tag)
            return
        if tag in ('text', 'image', 'use', 'line'):
            warn('<%s> elements are skipped' % tag)
            return
        fill = fill_of(el, fill)
        tr = el.get('transform')
        if tr and tag not in ('rect', 'circle', 'ellipse', 'polygon', 'polyline'):
            warn('transform on <%s> is ignored; flatten transforms in an editor first' % tag)
        m = matrix_of(tr) if tr else None

        def apply(x, y):
            if not m:
                return x, y
            a, b, c, d, e, f = m
            return a * x + c * y + e, b * x + d * y + f

        def poly(points):
            return ' -- '.join('(%s,%s)' % tuple(map(fmt, apply(x, y))) for x, y in points) + ' -- cycle'

        if tag in ('polygon', 'polyline'):
            v = [float(x) for x in re.findall(NUM, el.get('points'))]
            emit(fill, poly(list(zip(v[0::2], v[1::2]))))
        elif tag == 'rect':
            x, y, w, h = (float(el.get(k, 0)) for k in ('x', 'y', 'width', 'height'))
            if el.get('rx') or el.get('ry'):
                warn('rounded rect corners are drawn square')
            emit(fill, poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)]))
        elif tag in ('circle', 'ellipse'):
            cx, cy = float(el.get('cx', 0)), float(el.get('cy', 0))
            rx = float(el.get('r') or el.get('rx')); ry = float(el.get('r') or el.get('ry'))
            pts = [(cx + rx * math.cos(2 * math.pi * k / 72), cy + ry * math.sin(2 * math.pi * k / 72)) for k in range(72)]
            emit(fill, poly(pts))
        elif tag == 'path':
            emit(fill, path_to_tikz(el.get('d')))
        for ch in el:
            walk(ch, fill)

    walk(root, '#000000')
    with open(dst, 'w') as o:
        o.write('%% %s: converted from %s by svg2tikz.py (paper-figure-guide). viewBox %s\n'
                % (name, src.split('/')[-1], ' '.join(map(fmt, vb))))
        for hexc, cn in colors.items():
            o.write('\\definecolor{%s}{HTML}{%s}\n' % (cn, hexc.lstrip('#').upper()))
        o.write('\\newcommand{\\%s}[1]{%% #1 = height\n' % name)
        o.write('  \\resizebox{!}{#1}{\\begin{tikzpicture}[x=1pt, y=-1pt]\n')
        o.write('    \\useasboundingbox (%s,%s) rectangle (%s,%s);\n'
                % tuple(map(fmt, (vb[0], vb[1], vb[0] + vb[2], vb[1] + vb[3]))))
        for s in shapes:
            o.write('    ' + s + '\n')
        o.write('  \\end{tikzpicture}}}\n')
    print('svg2tikz: %d shapes, %d colours -> %s' % (len(shapes), len(colors), dst))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    main(*sys.argv[1:4])
