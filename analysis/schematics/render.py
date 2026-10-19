"""Render an SVG to PNG with headless Chromium (Playwright): python render.py IN.svg OUT.png SCALE"""
import asyncio, sys, re
from playwright.async_api import async_playwright
async def main(src, out, scale):
    svg = open(src).read()
    m = re.search(r'<svg[^>]*width="(\d+)"[^>]*height="(\d+)"', svg)
    w, h = int(m.group(1)), int(m.group(2))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
        await pg.set_content(f'<html><body style="margin:0;background:white">{svg}</body></html>')
        await pg.locator("svg").first.screenshot(path=out)
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1))
