"""Trace the radii wordmark out of the org avatar into per-glyph SVG path data."""
import math
import os
from PIL import Image

AVATAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'org_avatar.png')
# geometry measured from the avatar (native pixels)
CIRCLE = (137.5, 242.5, 119.0)   # cx, cy, r
DOT    = (431.0, 268.5, 15.0)
ORIGIN = (19.0, 124.0)           # top-left of the logo's overall bbox


def _load():
    im = Image.open(AVATAR).convert('RGBA')
    W, H = im.size
    px = im.load()
    ink = [[False]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if a >= 128 and (0.2126*r + 0.7152*g + 0.0722*b) < 110:
                ink[y][x] = True
    return ink, W, H


def _loops(m, W, H):
    edges = {}
    def add(a, b):
        edges.setdefault(a, []).append(b)
    for y in range(H):
        for x in range(W):
            if not m[y][x]:
                continue
            if y == 0 or not m[y-1][x]:     add((x, y), (x+1, y))
            if x+1 >= W or not m[y][x+1]:   add((x+1, y), (x+1, y+1))
            if y+1 >= H or not m[y+1][x]:   add((x+1, y+1), (x, y+1))
            if x == 0 or not m[y][x-1]:     add((x, y+1), (x, y))
    out = []
    while edges:
        start = next(iter(edges))
        loop = [start]; cur = start
        while True:
            nxts = edges.get(cur)
            if not nxts:
                break
            nxt = nxts.pop()
            if not nxts:
                del edges[cur]
            loop.append(nxt); cur = nxt
            if cur == start:
                break
        if len(loop) > 12:
            out.append(loop)
    return out


def _dp(pts, eps):
    def simp(seq):
        if len(seq) < 3:
            return seq
        ax, ay = seq[0]; bx, by = seq[-1]
        dx, dy = bx-ax, by-ay
        n = math.hypot(dx, dy)
        best, bi = -1.0, 0
        for i in range(1, len(seq)-1):
            cx, cy = seq[i]
            d = abs(dy*cx - dx*cy + bx*ay - by*ax)/n if n else math.hypot(cx-ax, cy-ay)
            if d > best:
                best, bi = d, i
        if best > eps:
            return simp(seq[:bi+1])[:-1] + simp(seq[bi:])
        return [seq[0], seq[-1]]
    if pts[0] == pts[-1]:
        pts = pts[:-1]
    k = len(pts)//2
    return simp(pts[:k+1])[:-1] + simp(pts[k:] + [pts[0]])[:-1]


def glyph_paths(scale, eps=0.6, prec=2):
    """Return [d, ...] one path per glyph of the wordmark, left to right,
    in logo-local units (origin at the logo bbox top-left, y down)."""
    ink, W, H = _load()
    loops = _loops(ink, W, H)
    rings = []
    for lp in loops:
        s = _dp(lp, eps)
        if len(s) < 3:
            continue
        xs = [p[0] for p in s]
        rings.append((min(xs), max(xs), s))
    # cluster rings into glyphs by overlapping x-extent
    rings.sort(key=lambda r: r[0])
    groups = []
    for lo, hi, s in rings:
        for g in groups:
            if lo <= g['hi'] and hi >= g['lo']:
                g['lo'] = min(g['lo'], lo); g['hi'] = max(g['hi'], hi)
                g['rings'].append(s)
                break
        else:
            groups.append({'lo': lo, 'hi': hi, 'rings': [s]})
    # merge groups that ended up overlapping after growing
    merged = True
    while merged:
        merged = False
        for i in range(len(groups)):
            for j in range(i+1, len(groups)):
                a, b = groups[i], groups[j]
                if a['lo'] <= b['hi'] and b['lo'] <= a['hi']:
                    a['lo'] = min(a['lo'], b['lo']); a['hi'] = max(a['hi'], b['hi'])
                    a['rings'] += b['rings']; groups.pop(j)
                    merged = True; break
            if merged:
                break
    groups.sort(key=lambda g: g['lo'])
    ox, oy = ORIGIN
    out = []
    for g in groups:
        d = []
        for s in g['rings']:
            for i, (x, y) in enumerate(s):
                X = round((x-ox)*scale, prec); Y = round((y-oy)*scale, prec)
                d.append(('M' if i == 0 else 'L') + f'{X} {Y}')
            d.append('Z')
        out.append(' '.join(d))
    return out


def geom(scale):
    ox, oy = ORIGIN
    cx, cy, r = CIRCLE
    dx, dy, dr = DOT
    return {
        'circle': ((cx-ox)*scale, (cy-oy)*scale, r*scale),
        'dot': ((dx-ox)*scale, (dy-oy)*scale, dr*scale),
        'w': (446.0-ox)*scale,
        'h': (361.0-oy)*scale,
    }
