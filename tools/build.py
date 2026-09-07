# -*- coding: utf-8 -*-
"""Generate the radii org-profile SVGs: a technical drawing that draws itself."""
import math
import os

import lib_trace
import lib_text

S = 0.8824                      # logo scale -> circle diameter = 210 units
T = 10.0                        # animation cycle, seconds
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'profile', 'assets')

THEMES = {
    'light': dict(paper='#F3F4F1', grid='#DBDFD9', ink='#23282C',
                  dim='#7C858A', orange='#EB9500', on_orange='#23282C'),
    'dark':  dict(paper='#0A1E30', grid='#143753', ink='#DCEAF6',
                  dim='#6E97B8', orange='#F5A623', on_orange='#0A1E30'),
}


def pct(t):
    return round(t / T * 100, 3)


def kf_draw(name, t0, t1):
    return ('@keyframes ' + name + '{0%,' + str(pct(t0)) + '%{stroke-dashoffset:1}'
            + str(pct(t1)) + '%,100%{stroke-dashoffset:0}}')


def kf_fade(name, t0, t1):
    return ('@keyframes ' + name + '{0%,' + str(pct(t0)) + '%{opacity:0}'
            + str(pct(t1)) + '%,100%{opacity:1}}')


def arrow(x, y, ang, L=13.0, W=4.4):
    """Filled dimension arrowhead, tip at (x,y), pointing along ang (radians)."""
    bx, by = x - L * math.cos(ang), y - L * math.sin(ang)
    nx, ny = -math.sin(ang) * W / 2, math.cos(ang) * W / 2
    return 'M%.2f %.2fL%.2f %.2fL%.2f %.2fZ' % (x, y, bx + nx, by + ny, bx - nx, by - ny)


def circle_path(cx, cy, r):
    return ('M%.2f %.2fA%.2f %.2f 0 1 0 %.2f %.2fA%.2f %.2f 0 1 0 %.2f %.2fZ'
            % (cx - r, cy, r, r, cx + r, cy, r, r, cx - r, cy))


def hero(theme):
    c = THEMES[theme]
    VW, VH = 1200, 440
    glyphs = lib_trace.glyph_paths(S)
    g = lib_trace.geom(S)
    TX, TY = 182.0, 96.0
    cx, cy, r = TX + g['circle'][0], TY + g['circle'][1], g['circle'][2]
    dx, dy, dr = TX + g['dot'][0], TY + g['dot'][1], g['dot'][2]
    right = TX + g['w']

    frame = 'M10 10H1190V430H10Z M22 22H1178V418H22Z'

    gl = []
    x = 40
    while x < 1178:
        gl.append('M%d 22V418' % x)
        x += 20
    y = 40
    while y < 418:
        gl.append('M22 %dH1178' % y)
        y += 20
    grid = ''.join(gl)

    ext = 26
    clines = ('M%.2f %.2fH%.2f M%.2f %.2fV%.2f'
              % (cx - r - ext, cy, cx + r + ext, cx, cy - r - ext, cy + r + ext))

    yd1, yd2 = 336.0, 388.0
    xL, xR = cx - r, cx + r
    extl = ('M%.2f %.2fV396 M%.2f %.2fV%.2f M%.2f %.2fV396'
            % (xL, cy + 7, xR, cy + 7, yd1 + 8, right, dy + dr + 7))
    dimlines = ('M%.2f %.2fH%.2f M%.2f %.2fH%.2f'
                % (xL, yd1, xR, xL, yd2, right))
    heads = ''.join([arrow(xL, yd1, math.pi), arrow(xR, yd1, 0.0),
                     arrow(xL, yd2, math.pi), arrow(right, yd2, 0.0)])
    t1 = lib_text.text(u'Ø210', 21, (xL + xR) / 2, yd1 - 9, 'middle', tracking=1.2)
    t2 = lib_text.text('377', 21, (xL + right) / 2, yd2 - 9, 'middle', tracking=1.2)

    # notes, right column, sitting above the title block
    NOTES = ['AEROSPACE AND AUTOMOTIVE COMPONENTS.',
             'QUOTED FROM CAD MODELS AND 2D DRAWINGS.',
             'MACHINED BY A NETWORK OF PARTNER SHOPS.']
    nx, ny = 722.0, 196.0
    note_head = lib_text.text('NOTES', 11.5, nx, ny, tracking=1.7, wght=400)
    note_body = []
    for i, line in enumerate(NOTES):
        yy = ny + 27 + i * 25
        note_body.append(lib_text.text('%d' % (i + 1), 15, nx, yy, tracking=1.2))
        note_body.append(lib_text.text(line, 15, nx + 22, yy, tracking=1.2))
    note_rule = 'M%.0f %.0fH%.0f' % (nx, ny + 9, nx + 456)

    # title block, flush with the inner frame's bottom-right corner
    bx0, by0, bx1, by1 = 722.0, 316.0, 1178.0, 418.0
    ymid, xmid = 367.0, 950.0
    tb_rules = ('M%.0f %.0fH%.0fV%.0fH%.0fZ M%.0f %.0fH%.0f M%.0f %.0fV%.0f'
                % (bx0, by0, bx1, by1, bx0, bx0, ymid, bx1, xmid, by0, by1))
    cells = [(bx0, by0, 'TITLE', 'RADII'),
             (xmid, by0, 'SCALE', '1:1'),
             (bx0, ymid, 'PROCESS', 'CNC MACHINING'),
             (xmid, ymid, 'ORIGIN', 'MEXICO')]
    tb_lab, tb_val = [], []
    for x0, y0, lab, val in cells:
        tb_lab.append(lib_text.text(lab, 11.5, x0 + 15, y0 + 21, tracking=1.7, wght=400))
        tb_val.append(lib_text.text(val, 22, x0 + 15, y0 + 44, tracking=1.4, wght=600))

    defs = ''.join('<path id="g%d" pathLength="1" d="%s"/>' % (i, d)
                   for i, d in enumerate(glyphs))
    wm_fill = ''.join('<use href="#g%d" xlink:href="#g%d"/>' % (i, i)
                      for i in range(len(glyphs)))
    wm_line = ''.join('<use class="dr an w%d" href="#g%d" xlink:href="#g%d"/>' % (i, i, i)
                      for i in range(len(glyphs)))

    disc = circle_path(cx, cy, r)
    dotp = circle_path(dx, dy, dr)

    k = [kf_draw('kfr', 0.00, 0.80), kf_fade('kgr', 0.40, 1.30),
         kf_draw('kdc', 0.90, 2.20), kf_draw('kdt', 2.90, 3.30),
         kf_draw('kcl', 3.00, 3.80), kf_draw('kdm', 3.50, 4.40),
         kf_fade('kdv', 4.10, 4.60), kf_draw('knr', 3.90, 4.50),
         kf_fade('knt', 4.30, 4.95), kf_draw('ktb', 4.60, 5.30),
         kf_fade('ktv', 5.00, 5.60), kf_fade('kfl', 5.40, 6.50)]
    for i in range(len(glyphs)):
        k.append(kf_draw('kw%d' % i, 1.70 + 0.14 * i, 2.30 + 0.14 * i))
    k.append('@keyframes kwo{0%,54%{opacity:1}65%,100%{opacity:0}}')
    k.append('@keyframes ksh{0%,89%{opacity:1}97%,99.99%{opacity:0}100%{opacity:1}}')
    wm_rules = ''.join('.w%d{animation-name:kw%d}' % (i, i) for i in range(len(glyphs)))

    css = (
        '.paper{fill:%(paper)s}'
        '.grid{stroke:%(grid)s;stroke-width:1;fill:none;shape-rendering:crispEdges}'
        '.frame{stroke:%(ink)s;stroke-width:1.6;fill:none}'
        '.cl{stroke:%(dim)s;stroke-width:1;fill:none;stroke-dasharray:22 4 5 4}'
        '.disc{stroke:%(ink)s;stroke-width:1.7;fill:none}'
        '.dr{fill:none;stroke:%(ink)s;stroke-width:1.35;stroke-linejoin:round}'
        '.fo{fill:%(orange)s}'
        '.fi{fill:%(ink)s;fill-rule:evenodd}'
        '.dim{stroke:%(dim)s;stroke-width:1.1;fill:none}'
        '.head{fill:%(dim)s;stroke:none}'
        '.val{fill:%(ink)s;stroke:none}'
        '.lab{fill:%(dim)s;stroke:none}'
        '.tb{stroke:%(ink)s;stroke-width:1.3;fill:none}'
        '.nr{stroke:%(dim)s;stroke-width:1;fill:none}'
        '.note{fill:%(ink)s;stroke:none}'
        '.on{fill:%(on_orange)s}'
        '.wo{opacity:0}'
    ) % c
    css += (
        '@media (prefers-reduced-motion:no-preference){'
        + ''.join(k)
        + '.sheet{animation:ksh %ss linear infinite}' % T
        + '.an{animation-duration:%ss;animation-timing-function:cubic-bezier(.4,0,.2,1);'
          'animation-iteration-count:infinite}' % T
        + '.dr,.disc,.frame,.cl,.dim,.tb,.nr{stroke-dasharray:1;stroke-dashoffset:0}'
          '.frame{animation-name:kfr}.gridg{animation-name:kgr}.disc{animation-name:kdc}'
          '.dotl{animation-name:kdt}.cl{animation-name:kcl}.dimg{animation-name:kdm}'
          '.valg{animation-name:kdv}.tb{animation-name:ktb}.tbt{animation-name:ktv}'
          '.fills{animation-name:kfl}.nr{animation-name:knr}.nt{animation-name:knt}'
          '.wo{animation-name:kwo}'
        + wm_rules
        + '}'
    )

    parts = []
    parts.append('<svg xmlns="http://www.w3.org/2000/svg" '
                 'xmlns:xlink="http://www.w3.org/1999/xlink" '
                 'viewBox="0 0 %d %d" width="%d" height="%d" role="img" '
                 'aria-label="Technical drawing of the radii logo. An orange disc '
                 'dimensioned 210, and a title block reading RADII, scale 1 to 1, '
                 'CNC machining, Mexico.">' % (VW, VH, VW, VH))
    parts.append('<title>radii — CNC parts, quoted and sourced in Mexico</title>')
    parts.append('<style>%s</style>' % css)
    parts.append('<defs>%s<path id="disc" pathLength="1" d="%s"/>'
                 '<path id="dot" pathLength="1" d="%s"/>'
                 '<clipPath id="cin"><path d="%s"/></clipPath>'
                 '<mask id="mout"><rect width="%d" height="%d" fill="#fff"/>'
                 '<path d="%s" fill="#000"/></mask>'
                 '</defs>' % (defs, disc, dotp, disc, VW, VH, disc))
    parts.append('<rect class="paper" width="%d" height="%d"/>' % (VW, VH))
    parts.append('<g class="sheet">')
    parts.append('<g class="gridg an"><path class="grid" d="%s"/></g>' % grid)
    parts.append('<path class="frame an" pathLength="1" d="%s"/>' % frame)
    parts.append('<path class="cl an" pathLength="1" d="%s"/>' % clines)
    parts.append('<g class="fills an"><use class="fo" href="#disc" xlink:href="#disc"/></g>')
    parts.append('<use class="disc an" href="#disc" xlink:href="#disc"/>')
    xf = 'transform="translate(%.2f %.2f)"' % (TX, TY)
    parts.append('<g class="wo an" %s>%s</g>' % (xf, wm_line))
    parts.append('<g class="fills an">'
                 '<g clip-path="url(#cin)"><g class="fi on" %s>%s</g></g>'
                 '<g mask="url(#mout)"><g class="fi" %s>%s</g></g>'
                 '</g>' % (xf, wm_fill, xf, wm_fill))
    parts.append('<g class="fills an"><use class="fo" href="#dot" xlink:href="#dot"/></g>')
    parts.append('<use class="dotl disc an" href="#dot" xlink:href="#dot"/>')
    parts.append('<path class="dim dimg an" pathLength="1" d="%s %s"/>'
                 % (extl, dimlines))
    parts.append('<g class="valg an"><path class="head" d="%s"/>'
                 '<g class="val">%s%s</g></g>' % (heads, t1, t2))
    parts.append('<path class="tb an" pathLength="1" d="%s"/>' % tb_rules)
    parts.append('<g class="tbt an"><g class="lab">%s</g><g class="val">%s</g></g>'
                 % (''.join(tb_lab), ''.join(tb_val)))
    parts.append('<path class="nr an" pathLength="1" d="%s"/>' % note_rule)
    parts.append('<g class="nt an"><g class="lab">%s</g><g class="note">%s</g></g>'
                 % (note_head, ''.join(note_body)))
    parts.append('</g></svg>')
    return '\n'.join(parts)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for nm in ('light', 'dark'):
        p = os.path.join(OUT, 'hero-%s.svg' % nm)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(hero(nm))
        print(p, os.path.getsize(p), 'bytes')
