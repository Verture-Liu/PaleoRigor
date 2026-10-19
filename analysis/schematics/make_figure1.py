"""Figure 1: workflow schematic (no in-figure title). Writes figures/manuscript/figure1_workflow.svg; render to PNG with render.py."""
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "figures" / "manuscript"
FONT="font-family:Arial,'Liberation Sans',Helvetica,sans-serif"
W,H=3600,900
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
 f'<style>text{{{FONT}}}</style>',
 '<defs><marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#a3afbc"/></marker>',
 '<marker id="ab" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2b78a0"/></marker></defs>',
 f'<rect width="{W}" height="{H}" fill="white"/>']
boxes=[("Question","source files","#2b78a0"),("Plan","LLM · workflow JSON","#2b78a0"),("Review","provenance","#c96018"),("Execute","local tools","#1f2933"),("Outputs","audit records","#2b78a0")]
bw,bh,y0=560,250,40
xs=[120+i*700 for i in range(5)]
for (t,sub,c),x in zip(boxes,xs):
    o.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="28" fill="white" stroke="#a9b3be" stroke-width="6"/>')
    o.append(f'<text x="{x+bw/2}" y="{y0+112}" text-anchor="middle" style="font-size:66px;font-weight:700;fill:{c}">{t}</text>')
    o.append(f'<text x="{x+bw/2}" y="{y0+190}" text-anchor="middle" style="font-size:46px;fill:#5f6b7a">{sub}</text>')
for x in xs[:-1]:
    o.append(f'<path d="M{x+bw+22},{y0+bh/2} L{x+bw+118},{y0+bh/2}" stroke="#a3afbc" stroke-width="9" marker-end="url(#ag)"/>')
pills={1:"plan review",3:"run approval",4:"result audit"}
for i,lab in pills.items():
    cx=xs[i]+bw/2 - (60 if i==3 else 0)
    o.append(f'<rect x="{cx-170}" y="{y0+bh+45}" width="340" height="82" rx="22" fill="#fdf4e8" stroke="#efcfa5" stroke-width="4"/>')
    o.append(f'<text x="{cx}" y="{y0+bh+100}" text-anchor="middle" style="font-size:40px;font-weight:700;fill:#c96018">{lab}</text>')
ax=xs[3]+bw-80
o.append(f'<path d="M{ax},{y0+bh+8} L{ax},560" stroke="#2b78a0" stroke-width="8" marker-end="url(#ab)"/>')
o.append('<text x="440" y="545" style="font-size:52px;font-weight:700;fill:#1f2933">Ancient-data skill / tool layer</text>')
o.append('<path d="M440,585 L3160,585" stroke="#d3d9df" stroke-width="7"/>')
skills=[("Peptide / CSV","curation"),("Sequencing","QC"),("Source-data","audit"),("Ancient-DNA","extensions")]
for i,(a,b) in enumerate(skills):
    x=440+i*700
    o.append(f'<rect x="{x}" y="650" width="620" height="210" rx="14" fill="#f7f9fb" stroke="#d6dde4" stroke-width="5"/>')
    o.append(f'<text x="{x+310}" y="742" text-anchor="middle" style="font-size:54px;font-weight:700;fill:#1f2933">{a}</text>')
    o.append(f'<text x="{x+310}" y="808" text-anchor="middle" style="font-size:54px;font-weight:700;fill:#1f2933">{b}</text>')
o.append('</svg>')
open(OUT / 'figure1_workflow.svg','w').write('\n'.join(o))
