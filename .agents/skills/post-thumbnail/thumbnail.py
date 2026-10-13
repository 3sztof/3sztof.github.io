#!/usr/bin/env python3
"""Render a 1200x630 post thumbnail: one logo or Lucide icon centred on a flat background.

Needs rsvg-convert (librsvg) and, for --bg-from, ImageMagick's `magick`.

Examples:
  thumbnail.py --logo https://pi.dev/logo-auto.svg --out content/posts/x/featured.png
  thumbnail.py --lucide database --color "#1f2937" --bg "#f3f4f6" --out featured.png
  thumbnail.py --logo logo.svg --bg-from content/posts/x/screenshot.png --out featured.png
"""
import argparse
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.parse

W, H = 1200, 630
# Safe content area: logos are fitted inside this box, centred on the canvas.
# x 128-1072 is the card-crop-safe width (see SKILL.md); height is kept generous
# but leaves top/bottom margins. A logo is scaled to fill this box on whichever
# axis binds first (width for wide logos, height for tall/square ones), so a
# 9:1 wordmark and a 1:1 glyph end up with a visually comparable footprint.
FIT_W, FIT_H = 820, 380
LUCIDE_URL = "https://unpkg.com/lucide-static@latest/icons/{}.svg"


def fetch(src: str) -> str:
    scheme = urllib.parse.urlparse(src).scheme
    if scheme:
        if scheme != "https":  # only https downloads; no file:, ftp:, or plain http
            sys.exit(f"refusing {scheme}: URL, use https or a local path")
        # curl --proto =https also refuses redirects to other schemes
        cmd = ["curl", "-fsSL", "--proto", "=https", "--max-time", "30", "-A", "post-thumbnail/1.0", src]
        return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    return pathlib.Path(src).read_text()


def border_colour(image: str) -> str:
    """Mean colour of the outermost pixels of an image (first frame for GIFs)."""
    cmd = [
        "magick", f"{image}[0]", "-alpha", "off", "-resize", "100x100!",
        "(", "-clone", "0", "-crop", "100x1+0+0", ")",
        "(", "-clone", "0", "-crop", "100x1+0+99", ")",
        "(", "-clone", "0", "-crop", "1x100+0+0", "-rotate", "90", ")",
        "(", "-clone", "0", "-crop", "1x100+99+0", "-rotate", "90", ")",
        "-delete", "0", "+repage", "-append", "-scale", "1x1!",
        "-format", "#%[hex:p{0,0}]", "info:",
    ]
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout.strip()[:7]


def nest(svg: str, scale: float, colour: str | None) -> str:
    """Nest a standalone SVG, fitted into the FIT_W x FIT_H safe box and centred.

    The logo is scaled to fill the fit box on whichever axis binds first, so wide
    wordmarks and square glyphs get a comparable visual footprint. `scale` shrinks
    the fit box uniformly (1.0 = fill it, 0.9 = 90% of it) for breathing room.
    """
    svg = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>|<!--.*?-->", "", svg, flags=re.S).strip()
    m = re.match(r"<svg\b([^>]*)>", svg, flags=re.S)
    if not m:
        sys.exit("logo is not an SVG")
    attrs = m.group(1)
    # Determine the logo's intrinsic aspect ratio from viewBox or width/height.
    try:
        vb = re.search(r'\bviewBox="[\d.\s-]*?([\d.]+)[,\s]+([\d.]+)\s*"', attrs)
        if vb:
            lw, lh = float(vb.group(1)), float(vb.group(2))
        else:
            w = re.search(r'\bwidth="([\d.]+)', attrs)
            h = re.search(r'\bheight="([\d.]+)', attrs)
            if not (w and h):
                sys.exit("logo SVG has no viewBox or width/height")
            lw, lh = float(w.group(1)), float(h.group(1))
            attrs += f' viewBox="0 0 {lw} {lh}"'
    except ValueError:
        sys.exit("logo SVG has an unparseable viewBox/width/height")
    aspect = lw / lh if lh else 1.0
    # Fit into the (scaled) safe box, preserving aspect ratio.
    fit_w, fit_h = FIT_W * scale, FIT_H * scale
    if aspect >= fit_w / fit_h:        # width-bound (wide logo)
        box_w, box_h = fit_w, fit_w / aspect
    else:                               # height-bound (tall/square logo)
        box_w, box_h = fit_h * aspect, fit_h
    attrs = re.sub(r'\s(width|height|x|y|class|style)="[^"]*"', "", attrs)
    if colour:
        attrs = re.sub(r'\scolor="[^"]*"', "", attrs) + f' color="{colour}"'
    x, y = (W - box_w) / 2, (H - box_h) / 2
    return f'<svg x="{x:.1f}" y="{y:.1f}" width="{box_w:.1f}" height="{box_h:.1f}"{attrs}>' + svg[m.end():]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--logo", help="SVG logo: file path or URL")
    src.add_argument("--lucide", help="Lucide icon name, e.g. database (https://lucide.dev/icons/)")
    bg = p.add_mutually_exclusive_group()
    bg.add_argument("--bg", default="#ffffff", help="background hex colour (default #ffffff)")
    bg.add_argument("--bg-from", help="image whose border colour becomes the background")
    p.add_argument("--color", help="icon colour; sets currentColor (Lucide icons, mono logos)")
    p.add_argument("--scale", type=float, default=None, help="share of the safe fit box to fill (default 0.92 for logos, 0.62 for Lucide icons); lower = more margin")
    p.add_argument("--out", required=True, help="output PNG, normally <post>/featured.png")
    p.add_argument("--keep-svg", action="store_true", help="also write the composed SVG next to the PNG")
    a = p.parse_args()

    svg = fetch(a.logo or LUCIDE_URL.format(a.lucide))
    colour = a.color or ("#1f2937" if a.lucide else None)
    background = border_colour(a.bg_from) if a.bg_from else a.bg
    # Lucide icons are square line-art; fill a smaller share so they don't dwarf logos.
    scale = a.scale if a.scale is not None else (0.62 if a.lucide else 0.92)
    source = a.logo or LUCIDE_URL.format(a.lucide)

    out = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
        f"  <!-- source: {source} -->\n"
        f'  <rect width="{W}" height="{H}" fill="{background}"/>\n'
        f"  {nest(svg, scale, colour)}\n</svg>\n"
    )
    png = pathlib.Path(a.out)
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as f:
        f.write(out)
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), f.name, "-o", str(png)], check=True)
    if a.keep_svg:
        png.with_suffix(".svg").write_text(out)
    print(f"{png} ({W}x{H}, background {background}, source {source})")


if __name__ == "__main__":
    main()
