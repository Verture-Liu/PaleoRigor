# Schematic figures

`make_figure1.py` and `make_graphical_abstract.py` write the SVG sources of Figure 1 and the graphical abstract to `figures/manuscript/`.
`render.py` turns an SVG into the PNG used in the manuscript (Figure 1 at scale 1, 3600 × 900 px; graphical abstract at scale 2, 3600 × 1960 px):

```
python analysis/schematics/make_figure1.py
python analysis/schematics/render.py figures/manuscript/figure1_workflow.svg figures/manuscript/figure1_workflow.png 1
python analysis/schematics/make_graphical_abstract.py
python analysis/schematics/render.py figures/manuscript/graphical_abstract.svg figures/manuscript/graphical_abstract.png 2
```

`excavation_drawing.svg` is the author-drawn excavation scene used in the graphical abstract. Rendering needs Playwright with Chromium.
