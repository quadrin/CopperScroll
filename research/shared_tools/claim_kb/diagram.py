"""Deterministic editable SVG; no source images or geographic geometry."""
from html import escape
from pathlib import Path


def render(destination=None):
    destination=destination or Path(__file__).with_name('schema.svg')
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1170" viewBox="0 0 1440 1170">',
         '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10" fill="#526761"/></marker></defs>',
         '<rect width="1440" height="1170" fill="#faf9f5"/>',
         '<style>text{font-family:Arial,sans-serif;fill:#253333}.title{font-size:25px;font-weight:bold}.head{font-size:16px;font-weight:bold}.body{font-size:14px}.edge{font-size:14px;fill:#345c53}.id{font:13px monospace;fill:#53645d}</style>',
         '<text x="40" y="44" class="title">Copper Scroll · Claim-centred pilot</text>',
         '<text x="40" y="74" class="body">Typed IDs preserve original record IDs. Arrows carry named relations; they do not measure confidence.</text>',
         '<path d="M870 105 V1090" stroke="#c9d3cf"/>',
         '<text x="45" y="125" class="head">Abstract schema</text>',
         '<text x="910" y="125" class="head">Populated chain · Entry 11 / Entry 60</text>']
    def box(x,y,w,h,title,lines,id=None,color='#edf3ed'):
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{color}" stroke="#8fa79c"/>')
        svg.append(f'<text x="{x+16}" y="{y+28}" class="head">{escape(title)}</text>')
        for i,line in enumerate(lines):svg.append(f'<text x="{x+16}" y="{y+56+i*23}" class="body">{escape(line)}</text>')
        if id:svg.append(f'<text x="{x+16}" y="{y+h-15}" class="id">{escape(id)}</text>')
    def arrow(x1,y1,x2,y2,label,tx=None,ty=None):
        svg.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="#526761" stroke-width="1.7" marker-end="url(#arrow)"/>')
        svg.append(f'<text x="{tx if tx is not None else (x1+x2)/2+7}" y="{ty if ty is not None else (y1+y2)/2-8}" class="edge">{escape(label)}</text>')
    box(45,160,355,160,'1 · Text, witnesses, readings',[
        'Entry ↔ edition numbering ↔ locus', 'Segment / original / replica / reconstruction',
        'Letters, restorations, lexical sense, syntax', 'Interpretation → derived requirement'])
    box(455,160,355,160,'4 · Sources and observations',[
        'Work → edition → digital copy → locator','Archive / campaign / original observation',
        'Inspection, rights, hashes, exact pages','Observed / reconstruction / inference'])
    box(45,430,355,140,'2 · Names and attestations',[
        'Written occurrence ≠ proposed referent','Document findspot ≠ mentioned place',
        'Composition / object / described dates'])
    box(455,430,355,140,'3 · Places and feature states',[
        'Feature identity → state → event','Measurement endpoints, phase and frame',
        'Local plan; registration needed for world'])
    box(240,680,390,150,'5 · Claims and hypotheses',[
        'Subject + relationship + object / value','Supporting / conflicting / prerequisite claims',
        'Fixed feature assignment under each branch','Separate uncertainty dimensions; revisions'])
    box(240,930,390,140,'6 · Tests, coverage, dependencies',[
        'Frozen specification + controls + decision rule','Requirement result ≠ inspection ≠ test outcome',
        'Explicit gap → acquisition → conditional effect'])
    arrow(400,225,455,225,'cites',409,208)
    arrow(220,430,220,320,'at_locus',128,383)
    arrow(635,320,635,430,'about',648,382)
    arrow(220,570,330,680,'proposed_same_referent',52,638)
    arrow(540,680,635,570,'assigns / about',637,640)
    arrow(455,680,400,285,'under_branch',350,356)
    arrow(415,680,455,285,'supports / conflicts',260,610)
    arrow(435,830,435,930,'evaluates / depends_on',447,886)
    box(910,160,480,125,'Exploratory result: contradicted',[
        'RB-M · early window (50 BCE–70 CE)',
        'Fixed pool = 1898 reservoir; pit = NS1'],
        'relationships-jericho-modern-ns1-RB-M-early', '#f7ece4')
    arrow(1150,285,1150,335,'depends_on · requirement check',920,315)
    box(910,335,480,125,'Pool-period requirement check',[
        'Pool must be accessible in the selected window.',
        'The assigned reservoir postdates this window.'],
        '…-jericho-modern-ns1-RB-M-early-pool-period')
    arrow(1150,460,1150,510,'conflicts · chronology claim',920,492)
    box(910,510,480,145,'Chronology claim',[
        'Construction year recorded as 1898',
        'Evidence kind: published reconstruction',
        'Other pool identities retain separate results.'],
        'claim/relationships-modern-reservoir-chronology')
    arrow(1150,655,1150,705,'derived_from · original observation record',920,687)
    box(910,705,480,145,'Underlying observation',[
        'Dorrell’s historical reservoir reconstruction',
        'Historical irregular basin remains distinct.',
        'Earlier construction / accessible use unresolved.'],
        'observation/relationships-modern-reservoir-chronology')
    arrow(1150,850,1150,900,'cites · exact source locator',930,881)
    box(910,900,480,140,'Underlying source and revision dependency',[
        'Dorrell 1993 pp. 95–97, 110–112; Figs. 1–4, 20–21',
        'Changed date → reassess dependent branches.',
        'Preserve earlier result and its input hashes.'],
        'source/relationships-dorrell')
    svg += ['<text x="45" y="1120" class="body">Legend: pale green = record groups; pale tan = conditional result. Null = unestablished. Geometry stays null when unestablished.</text>',
            '<text x="45" y="1146" class="body">Source-plan frames stay local. Repeated reports retain one original-observation lineage. Compatibility supplies no identification confidence.</text>', '</svg>']
    destination.write_text('\n'.join(svg)+'\n',encoding='utf-8')
    return destination


if __name__=='__main__':print(render())
