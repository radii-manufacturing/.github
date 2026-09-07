"""Bahnschrift (DIN 1451) outlines -> SVG path data. Technical-drawing lettering."""
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen

_CACHE = {}

def _inst(wght, wdth):
    key = (wght, wdth)
    if key not in _CACHE:
        f = TTFont(r'C:\Windows\Fonts\bahnschrift.ttf')
        v = instancer.instantiateVariableFont(f, {'wght': wght, 'wdth': wdth}, inplace=False)
        _CACHE[key] = (v, v.getGlyphSet(), v.getBestCmap(), v['hmtx'], v['head'].unitsPerEm)
    return _CACHE[key]


def width(s, size, tracking=0.0, wght=500, wdth=87.5):
    _, _, cmap, hmtx, upem = _inst(wght, wdth)
    k = size/upem
    w = 0.0
    for ch in s:
        g = cmap.get(ord(ch))
        if g is None:
            continue
        w += hmtx[g][0]*k + tracking
    return w - tracking if s else 0.0


def text(s, size, x, y, anchor='start', tracking=0.0, wght=500, wdth=87.5, prec=2):
    """Path data for `s` with its baseline at y, in SVG user units."""
    _, gs, cmap, hmtx, upem = _inst(wght, wdth)
    k = size/upem
    if anchor == 'middle':
        x -= width(s, size, tracking, wght, wdth)/2
    elif anchor == 'end':
        x -= width(s, size, tracking, wght, wdth)
    out, pen_x = [], x
    for ch in s:
        g = cmap.get(ord(ch))
        if g is None:
            pen_x += size*0.4 + tracking
            continue
        pen = SVGPathPen(gs, ntos=lambda v: repr(round(v, 1)))
        gs[g].draw(pen)
        d = pen.getCommands()
        if d:
            out.append(f'<g transform="translate({round(pen_x,prec)} {round(y,prec)}) '
                       f'scale({round(k,6)} {round(-k,6)})"><path d="{d}"/></g>')
        pen_x += hmtx[g][0]*k + tracking
    return ''.join(out)
