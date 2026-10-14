import re, html
R='/home/claude/begasenergysdnbhd'
E=lambda s: html.escape(s.strip(),quote=False)
lines=[l.strip() for l in open(R+'/tools/services-content.txt',encoding='utf-8').read().splitlines()]
names=['Instrumentation/Control Engineering & Maintenance','Transportation & Installation of Offshore Facilities','Onshore Fabrication','Commissioning of Specialist Electrical, HVAC & Instrumentation Systems','Offshore Construction','Maintenance and Repairs of Offshore Facilities','Electrical Engineering & Maintenance','Electrical Construction Work','Field Instrumentation Maintenance','Marine Transportation & Support Services','Vessel Cleaning Services']
subs=[];cur=None
for l in lines:
    if not l: continue
    if l.endswith(':') and l[:-1] in names:
        cur={'name':l[:-1],'items':[]};subs.append(cur);continue
    if cur is not None and l.endswith(':') and len(l)<80: cur['items'].append(l[:-1])
# key by (occurrence) name -> first occurrence items, except field instrumentation / dup instrumentation
def get(name,nth=0):
    c=[s for s in subs if s['name']==name]
    return c[nth]['items']
def card(title,items,off=False):
    return '<div class="gcard%s"><h3>%s</h3><ul class="cols">%s</ul></div>'%(' off' if off else '',E(title),''.join('<li>%s</li>'%E(i) for i in items))
on=[('Onshore Fabrication',get('Onshore Fabrication'),False),
    ('Commissioning of Specialist Electrical, HVAC & Instrumentation Systems',get('Commissioning of Specialist Electrical, HVAC & Instrumentation Systems'),False),
    ('Electrical Engineering & Maintenance',get('Electrical Engineering & Maintenance'),False),
    ('Electrical Construction Work',get('Electrical Construction Work'),False),
    ('Field Instrumentation Maintenance',get('Field Instrumentation Maintenance'),False)]
off=[('Offshore Construction',get('Offshore Construction'),True),
     ('Maintenance and Repairs of Offshore Facilities',get('Maintenance and Repairs of Offshore Facilities'),True),
     ('Transportation & Installation of Offshore Facilities',get('Transportation & Installation of Offshore Facilities'),True),
     ('Instrumentation/Control Engineering & Maintenance',get('Instrumentation/Control Engineering & Maintenance',0),True),
     ('Marine Transportation & Support Services',get('Marine Transportation & Support Services'),True),
     ('Vessel Cleaning Services',get('Vessel Cleaning Services'),True)]
def block(cards,more):
    return '<div class="grp">\n        '+'\n        '.join(card(t,i,o) for t,i,o in cards)+'\n      </div>\n      <a class="link-arrow" href="#" onClick="{{g.services}}">%s <span aria-hidden="true">→</span></a>'%more
p=R+'/design/Main.dc.html'
d=open(p,encoding='utf-8').read()
def repl(d,start,end,eyebrow_old,h2_old,eyebrow,h2,cards,more):
    i=d.index(start);j=d.index(end,i);b=d[i:j]
    g=b.index('<div class="grp">');ge=b.index('<div class="cta"') if False else None
    # grp block ends at the closing of grp: find '</div>\n      </div>' pattern after grp start -> use marker of following section
    k=b.index('</section>',g)
    new=block(cards,more)
    b=b[:g]+new+'\n    </div>\n  '+b[k:]
    b=b.replace(eyebrow_old,eyebrow).replace(h2_old,h2)
    return d[:i]+b+d[j:]
d=repl(d,'<!-- ================= ONSHORE','<!-- ================= OFFSHORE','What we deliver onshore','Four areas of onshore capability.','Onshore capabilities','Fabrication, commissioning, electrical and instrumentation.',on,'See full service descriptions')
d=repl(d,'<!-- ================= OFFSHORE','<!-- ================= MANPOWER','What we deliver offshore','Three areas of offshore capability.','Offshore capabilities','Construction, installation, maintenance and marine support.',off,'See full service descriptions')
css='''
.gcard ul.cols{columns:2;column-gap:36px}
.gcard ul.cols li{break-inside:avoid}
@media (max-width:620px){.gcard ul.cols{columns:1}}
'''
if '.gcard ul.cols' not in d:
    k=d.index('/* hse */'); d=d[:k]+css+d[k:]
open(p,'w',encoding='utf-8').write(d)
print([ (t,len(i)) for t,i,_ in on+off])
