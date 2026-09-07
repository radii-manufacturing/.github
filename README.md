# .github

Organization defaults for Radii. The page that renders at
[github.com/radii-manufacturing](https://github.com/radii-manufacturing) is
`profile/README.md`, and its artwork is in `profile/assets/`.

## The hero

`profile/assets/hero-light.svg` and `hero-dark.svg` are a technical drawing of the
Radii mark that draws itself: sheet frame, grid, the disc outline, the wordmark, the
dimensions, the notes and the title block arrive in that order, then the colour
lands and the drawing resolves into the logo. One ten-second loop, CSS keyframes
only, no JavaScript. The sequence is skipped for anyone whose system asks for
reduced motion, and the artwork then shows its finished state.

Both files are generated, not hand-edited. The wordmark is traced from the
organization avatar rather than set in a font, because fonts do not load inside an
SVG that GitHub renders as an image. Lettering is Bahnschrift, Microsoft's cut of
DIN 1451, converted to outlines for the same reason.

To regenerate them, run both build scripts from `tools/`. They write straight into
`profile/assets/`.

```
cd tools
uv run --with pillow --with fonttools python build.py
uv run --with pillow --with fonttools python build_rule.py
```

`build.py` holds the palettes, the layout and the animation timeline; `lib_trace.py`
traces the mark; `lib_text.py` turns strings into outlines. Bahnschrift is read from
the system font directory, so regenerating on a machine without it needs that path
changed. Edit the SVGs by hand only for a one-line colour fix.

## Changing the page

`profile/README.md` is ordinary Markdown. Asset links must stay absolute
`raw.githubusercontent.com` URLs; relative paths do not resolve on the organization
profile page.
