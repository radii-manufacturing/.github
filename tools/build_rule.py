# -*- coding: utf-8 -*-
"""A section divider drawn as a dimension line, with the logo's period as its centre mark."""
import os
from build import THEMES, arrow, OUT
import math

VW, VH = 1200, 24
MID, GAP = 600.0, 34.0


def rule(theme):
    c = THEMES[theme]
    y = 12.0
    ticks = 'M2 5V19 M1198 5V19'
    line = 'M2 %.0fH%.0f M%.0f %.0fH1198' % (y, MID - GAP, MID + GAP, y)
    heads = arrow(2, y, math.pi, L=11, W=4.0) + arrow(1198, y, 0.0, L=11, W=4.0)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
        'height="%d" role="img" aria-label="">'
        '<style>.l{stroke:%s;stroke-width:1.1;fill:none}.h{fill:%s}.o{fill:%s}</style>'
        '<path class="l" d="%s %s"/><path class="h" d="%s"/>'
        '<circle class="o" cx="%.0f" cy="%.0f" r="5.5"/>'
        '</svg>'
    ) % (VW, VH, VW, VH, c['dim'], c['dim'], c['orange'], ticks, line, heads, MID, y)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for nm in ('light', 'dark'):
        p = os.path.join(OUT, 'rule-%s.svg' % nm)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(rule(nm))
        print(p, os.path.getsize(p), 'bytes')
