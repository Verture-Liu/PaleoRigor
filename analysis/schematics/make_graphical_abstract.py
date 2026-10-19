"""Graphical abstract (author-drawn; no photographs). Writes figures/manuscript/graphical_abstract.svg; render to PNG with render.py."""
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "figures" / "manuscript"
import math, re
FONT="font-family:Arial,'Liberation Sans',Helvetica,sans-serif"
dig=open(HERE / 'excavation_drawing.svg').read()
inner=re.sub(r'^.*?<svg[^>]*>','',dig,count=1,flags=re.S).rsplit('</svg>',1)[0]
inner=re.sub(r'<metadata>.*?</metadata>','',inner,flags=re.S)  # drop embedded file metadata
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="980" viewBox="0 0 1800 980">',
 f'<style>text{{{FONT}}} .panel{{font-size:34px;font-weight:700;fill:#1f2933}} .lab{{font-size:24px;font-weight:700;fill:#2b78a0}} .body{{font-size:22px;fill:#5f6b7a}} .fb{{font-size:24px;font-weight:700;fill:#c96018}}</style>',
 '<defs>'
 '<marker id="mg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#a8b6c5"/></marker>'
 '<marker id="mb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2b78a0"/></marker>'
 '<marker id="mo" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#c96018"/></marker>'
 '<marker id="mv" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3f7f5f"/></marker>'
 '</defs>',
 '<rect width="1800" height="980" fill="white"/>',
 '<text x="900" y="72" text-anchor="middle" style="font-size:54px;font-weight:700;fill:#1f2933">PaleoRigor</text>',
 '<text x="900" y="116" text-anchor="middle" style="font-size:27px;fill:#5f6b7a">Human review links source context, fragile DNA signals, and auditable local checks.</text>',
 # panels
 '<rect x="55" y="160" width="500" height="505" rx="20" fill="#fbf4eb" stroke="#eadccc" stroke-width="3"/>',
 '<rect x="650" y="160" width="500" height="505" rx="20" fill="white" stroke="#dfe7ee" stroke-width="3"/>',
 '<rect x="1245" y="160" width="500" height="505" rx="20" fill="#edf7ef" stroke="#dce8dc" stroke-width="3"/>',
 '<circle cx="78" cy="180" r="17" fill="#c96018"/><circle cx="672" cy="180" r="17" fill="#2b78a0"/><circle cx="1267" cy="180" r="17" fill="#3f7f5f"/>',
 '<text x="90" y="232" class="panel">Archaeological</text><text x="90" y="272" class="panel">source</text>',
 '<text x="690" y="232" class="panel">Ancient DNA</text><text x="690" y="272" class="panel">signal</text>',
 '<text x="1285" y="232" class="panel">PaleoRigor</text><text x="1285" y="272" class="panel">audit</text>',
 f'<svg x="102" y="300" width="406" height="242" viewBox="0 0 395 235">{inner}</svg>',
 '<rect x="125" y="572" width="360" height="54" rx="12" fill="#2b78a0"/><text x="305" y="608" text-anchor="middle" style="font-size:24px;font-weight:700;fill:white">Sample record</text>',
]
# DNA signal
cx,cy=900,425
o.append(f'<circle cx="{cx}" cy="{cy}" r="128" fill="#26343d" stroke="#e8edf2" stroke-width="7"/>')
pts1=[];pts2=[]
for i in range(0,181):
    x=cx-88+i*176/180; t=(x-(cx-88))/176*4*math.pi
    pts1.append(f"{x:.1f},{cy+42*math.sin(t):.1f}"); pts2.append(f"{x:.1f},{cy-42*math.sin(t):.1f}")
for k in range(1,16):
    x=cx-88+k*11; t=(x-(cx-88))/176*4*math.pi
    o.append(f'<line x1="{x:.1f}" y1="{cy+42*math.sin(t):.1f}" x2="{x:.1f}" y2="{cy-42*math.sin(t):.1f}" stroke="#d8dee4" stroke-width="3" opacity="0.85"/>')
o.append(f'<polyline points="{" ".join(pts1)}" fill="none" stroke="#e0a030" stroke-width="7"/>')
o.append(f'<polyline points="{" ".join(pts2)}" fill="none" stroke="#86c3dc" stroke-width="7"/>')
for (dx,dy,c) in [(-90,-62,"#2b78a0"),(62,-78,"#e0a030"),(-30,85,"#3f7f5f"),(92,72,"#c0583c")]:
    o.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="10" fill="{c}"/>')
o.append('<text x="900" y="602" text-anchor="middle" class="body">Fragmented · damaged ·</text><text x="900" y="632" text-anchor="middle" class="body">contaminated</text>')
# audit panel
def box(x,y,l1,l2):
    o.append(f'<rect x="{x}" y="{y}" width="200" height="80" rx="12" fill="white" stroke="#d7e4ef" stroke-width="3"/>')
    o.append(f'<text x="{x+100}" y="{y+34}" text-anchor="middle" class="lab">{l1}</text><text x="{x+100}" y="{y+63}" text-anchor="middle" class="lab">{l2}</text>')
box(1283,300,"Source","records"); box(1517,300,"FASTQ","QC"); box(1283,440,"Expert","review"); box(1517,440,"Audit","outputs")
for d in ["M1486,340 L1510,340","M1486,480 L1510,480","M1383,384 L1383,432","M1617,384 L1617,432"]:
    o.append(f'<path d="{d}" stroke="#2b78a0" stroke-width="3.5" marker-end="url(#mb)"/>')
o.append('<rect x="1300" y="562" width="400" height="62" rx="12" fill="white" stroke="#c9d3dc" stroke-width="3"/><text x="1500" y="603" text-anchor="middle" style="font-size:26px;font-weight:700;fill:#1f2933">Decision gate</text>')
# flow arrows between panels
o.append('<path d="M567,412 L636,412" stroke="#a8b6c5" stroke-width="6" marker-end="url(#mg)"/>')
o.append('<path d="M1162,412 L1231,412" stroke="#a8b6c5" stroke-width="6" marker-end="url(#mg)"/>')
# feedback loop (orange): gate -> down -> left through the feedback note -> back up to the source panel
o.append('<path d="M1360,626 L1360,772 L1300,772" fill="none" stroke="#c96018" stroke-width="5"/>')
o.append('<path d="M650,772 L305,772 L305,680" fill="none" stroke="#c96018" stroke-width="5" marker-end="url(#mo)"/>')
o.append('<rect x="650" y="728" width="650" height="88" rx="16" fill="white" stroke="#e8c1a6" stroke-width="3"/>')
o.append('<text x="680" y="765" class="fb">Feedback: re-check metadata, pairing, or QC</text><text x="680" y="797" class="fb">before interpretation</text>')
# continue (green)
o.append('<path d="M1625,626 L1625,722" stroke="#3f7f5f" stroke-width="5" marker-end="url(#mv)"/>')
o.append('<rect x="1500" y="730" width="250" height="60" rx="16" fill="white" stroke="#bcdcc6" stroke-width="3"/><text x="1625" y="770" text-anchor="middle" style="font-size:26px;font-weight:700;fill:#3f7f5f">Continue</text>')
o.append('<rect x="55" y="850" width="1690" height="80" rx="18" fill="#f8fafc" stroke="#dfe5ec" stroke-width="3"/>')
o.append('<text x="85" y="899" style="font-size:22px;font-weight:700;fill:#1f2933">Output bundle:</text><text x="255" y="899" style="font-size:22px;fill:#5f6b7a">final outputs · step outputs · workflow JSON · checksums</text>')
o.append('</svg>')
open(OUT / 'graphical_abstract.svg','w').write('\n'.join(o))
