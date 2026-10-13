---
name: post-thumbnail
description: Create the featured.png thumbnail for a blog post or TIL in this Hugo site. Use when adding a new post, when a post has no featured image, or when the user asks to make or redo a thumbnail.
---

# Post thumbnail

Every post folder (`content/posts/<slug>/`, `content/til/<slug>/`) gets a `featured.png`. The Blowfish theme picks it up automatically for cards and link previews.

## Style rules

- 1200x630 PNG, one logo or icon centred on a flat background.
- No text, no AI-generated art, no stock photos, no mixed art styles.
- The logo must be whole: no clipping, no stretching.
- Keep everything inside the central 945x630 area (x 128-1072). Post cards crop thumbnails to 3:2 (Blowfish `thumbnailAspectRatio`, default 1.5), while link previews show the full 1200x630.
- Don't crop or resize existing photo, banner or slide thumbnails to 1200x630. The cards crop them again, so they lose twice as much. Leave them as they are unless the user asks.
- Record the image source in the post's footer or caption when its licence requires attribution.

## 1. Pick the subject

1. **The post is about a product with a logo** (pi, Raycast, Pulumi, Bedrock, ...). Use the official SVG, in this order:
   1. The product's own site or press kit (e.g. `https://pi.dev/logo-auto.svg`).
   2. [SVGL](https://svgl.app) (full-colour logos, free API: `https://api.svgl.app?search=<name>`).
   3. [Simple Icons](https://simpleicons.org) (single-colour, CC0, with the official brand hex). Raw SVG: `https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg`. Pass the brand colour with `--color`.
2. **Several products** (e.g. "X with Y"): compose the logos side by side by hand, copying `examples/two-logos.svg` or `examples/three-logos.svg` (logo boxes of the same size, evenly spaced, vertically centred). Crop a logo's viewBox if its SVG has wide padding, and remove any background rect baked into the logo.
3. **No logo** (a concept, a pattern, a story): pick a matching [Lucide](https://lucide.dev/icons/) icon by name and use `--lucide <name>`.

## 2. Pick the background

- **The post embeds an image or GIF that the thumbnail should match:** use `--bg-from <image>`. The script samples the image's border pixels, so the image appears to sit on the same background.
- **Otherwise:** white (`#ffffff`, the default and the style of most existing posts), or a light tint of the brand colour if the logo is white or very light.

## 3. Render

```bash
S=.agents/skills/post-thumbnail/thumbnail.py
python3 $S --logo https://pi.dev/logo-auto.svg --scale 0.95 --out content/posts/<slug>/featured.png
python3 $S --lucide database --out content/til/<slug>/featured.png
python3 $S --logo logo.svg --bg-from content/posts/<slug>/demo.gif --out content/posts/<slug>/featured.png
```

Options: `--scale` sets how much of the safe fit box the logo fills (default 0.92 for logos, 0.62 for Lucide icons; lower = more margin). The script measures the logo's aspect ratio and scales it to fill an 820x380 safe box on whichever axis binds first, so a wide wordmark (e.g. a 9:1 logo) and a square glyph end up with a comparable visual footprint - no more tiny wide logos floating in whitespace. Only drop `--scale` below the default if a logo has heavy built-in padding or you want extra breathing room. `--color` recolours Lucide icons and single-colour logos. `--keep-svg` saves the composed SVG next to the PNG.

Raster logos (PNG/WEBP, e.g. when no SVG exists) are not handled by this script - composite them with ImageMagick onto a 1200x630 white canvas (`magick -size 1200x630 xc:white \( logo.png -resize 760x \) -gravity center -composite out.png`). If the only available raster is low-res and looks soft when scaled up, upscale it first (see below) rather than shipping a blurry thumbnail.

### Upscaling low-res raster logos

When a logo only exists as a small raster (favicon, 100-200 px avatar) and scaling it to card size looks pixelated:

1. **Prefer a vector source first.** Re-check SVGL, Simple Icons, the brand's own site CSS/JS, and the site's `og:image` (often 1000-1200 px). A high-res raster from the brand's own CDN beats any upscaler.
2. **AI upscale** if no better source exists. [Upscayl](https://github.com/upscayl/upscayl) is a free, local, open-source GUI (Real-ESRGAN under the hood) - best for logos and art. CLI alternative: `realesrgan-ncnn-vulkan -i small.png -o big.png -s 4`. Online options: [upscale.media](https://www.upscale.media/), [Let's Enhance](https://letsenhance.io/), or Replicate's Real-ESRGAN. For flat logos, a vector trace (`vtracer`, or Illustrator/Inkscape image trace) often beats pixel upscaling and gives an infinitely scalable result.
3. **Recolour/extract** from a brand image: if the only sharp asset is a logo on a coloured background (common for `og:image`), knock out the background and recolour with ImageMagick (`-fuzz 25% -fill none -opaque <bg-hex>`, then `-fuzz 30% -fill "#1f2937" -opaque white`, then `-trim +repage`).

Requirements: `rsvg-convert` (librsvg), plus ImageMagick `magick` for `--bg-from`. The script only downloads over https.

## 4. Check it

Open the PNG and look at it before reporting done. Check that the logo is centred, whole, large enough to read at card size (about 400 px wide), and that the background matches. Then run `hugo --buildDrafts --destination /tmp/hugo-check` to confirm the site builds.
