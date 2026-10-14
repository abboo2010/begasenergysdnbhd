import re, html
R='/home/claude/begasenergysdnbhd'
E=lambda s: html.escape(s.strip(),quote=False)
lines=[l.strip() for l in open(R+'/tools/services-content.txt',encoding='utf-8').read().splitlines()]
groups_def=[
 ('Instrumentation/Control Engineering & Maintenance','Transportation & Installation of Offshore Facilities','Instrumentation & Offshore Installation'),
 ('Onshore Fabrication','Commissioning of Specialist Electrical, HVAC and instrumentation system','Onshore Fabrication & Specialist Commissioning'),
 ('Offshore Construction','Maintenance and Repairs of Offshore Facilities','Offshore Construction, Maintenance & Repairs'),
 ('Electrical Engineering & Maintenance','Electrical Construction Work','Electrical Engineering & Construction'),
 ('Instrumentation/Control Engineering & Maintenance','Field Instrumentation Maintenance','Field Instrumentation Maintenance'),
 ('Marine Transportation & Support Services','Vessel Cleaning Services','Marine Transportation & Vessel Cleaning'),
]
# locate group starts: a title line followed (next non-empty) by its pair title
def nxt(i):
    j=i+1
    while j<len(lines) and not lines[j]: j+=1
    return j
starts=[];pos=0
for a,b,_ in groups_def:
    for i in range(pos,len(lines)):
        if lines[i]==a and lines[nxt(i)]==b:
            starts.append(i);pos=i+1;break
    else: raise SystemExit('group not found '+a)
starts.append(len(lines))
sub_names=set()
for a,b,_ in groups_def:
    sub_names.add(a);sub_names.add(b)
sub_names|={'Commissioning of Specialist Electrical, HVAC & Instrumentation Systems'}
def parse(block):
    subs=[];cur=None;item=None
    for l in block:
        if not l: continue
        if l.endswith(':') and l[:-1] in sub_names:
            cur={'name':l[:-1],'items':[]};subs.append(cur);item=None;continue
        if cur is None: continue
        if l.endswith(':') and len(l)<80:
            item={'t':l[:-1],'d':[]};cur['items'].append(item);continue
        if item is not None and len(l)<190: item['d'].append(l)
    return subs
seen=set();out=[];chips=[]
for gi,(a,b,short) in enumerate(groups_def):
    subs=parse(lines[starts[gi]+2:starts[gi+1]])
    n=gi+1
    sub_html=''
    for si,s in enumerate(subs):
        if gi==0 and si==0: seen=set(it['t'] for it in s['items'])
        items=[it for it in s['items'] if not (gi==4 and si==0 and it['t'] in seen)]
        if not items: continue
        lis=''.join('<li><b>%s</b><span>%s</span></li>'%(E(it['t']),E(' '.join(it['d']))) for it in items)
        sub_html+='<details class="sub"%s><summary><span>%s</span><em>%d areas</em></summary><ul class="items">%s</ul></details>\n'%(' open' if si==0 else '',E(s['name']),len(items),lis)
    title=E(a)+' &amp; '+E(b) if False else None
    full = (E(a)+'<br>'+E(b)) if a!=b else E(a)
    out.append('''        <article class="svc" id="svc-%d">
          <div><i aria-hidden="true">%02d</i><h3>%s</h3><a class="btn btn-dark btn-sm" href="#" onClick="{{g.contact}}">Enquire about this service</a></div>
          <div class="subs">
%s          </div>
        </article>
'''%(n,n,full,sub_html))
    chips.append('        <li><a href="#svc-%d">%s</a></li>'%(n,E(short)))
shorts=[g[2] for g in groups_def]

p=R+'/design/Main.dc.html'
d=open(p,encoding='utf-8').read()
# services section
i=d.index('<ul class="chips"'); j=d.index('<div class="need">',i)
new='<ul class="chips" aria-label="Jump to a service group">\n'+'\n'.join(chips)+'\n      </ul>\n\n      <div style="margin-top:36px">\n'+''.join(out)+'      </div>\n\n      '
d=d[:i]+new+d[j:]
d=d.replace('Service titles follow those published on begasenergy.com. Please confirm the detailed scope, typical applications and delivery approach for each service, and which services are delivered directly or through partners, so the pages can be completed accurately.','Service descriptions follow the content supplied from the current begasenergy.com Services page. Please confirm each listed activity is delivered by BEGAS, directly or through partners, before launch.')
# home tiles
descs=['Control systems, instrumentation and the transport and installation of offshore facilities.','Onshore fabrication and commissioning of specialist electrical, HVAC and instrumentation systems.','Offshore construction, with maintenance and repair of offshore facilities.','Electrical engineering and maintenance, and electrical construction work.','Maintenance, calibration and diagnostics for field instrumentation.','Marine transportation and support services, and vessel cleaning.']
ti=d.index('<div class="tiles">'); tj=d.index('</div>',ti)
tiles='<div class="tiles">\n'+''.join('        <a class="tile" href="#" onClick="{{g.services}}"><i aria-hidden="true">%02d</i><h3>%s</h3><p>%s</p><span class="more">Explore service →</span></a>\n'%(k+1,E(shorts[k]),E(descs[k])) for k in range(6))+'      '
d=d[:ti]+new_tiles if False else d[:ti]+tiles+d[tj:]
# footer
fi=d.index('<h4>Capabilities</h4>'); fj=d.index('</ul>',fi)
d=d[:fi]+'<h4>Capabilities</h4>\n        <ul>\n'+''.join('          <li><a href="#" onClick="{{g.services}}">%s</a></li>\n'%E(s) for s in shorts)+'        '+d[fj:]
# select
si=d.index('<option value="">Select a service group</option>'); sj=d.index('<option>Other or not sure</option>',si)
d=d[:si]+'<option value="">Select a service group</option>\n'+''.join('                <option>%s</option>\n'%E(s) for s in shorts)+'                '+d[sj:]
# css
css='''
.subs{min-width:0}
.sub{border-top:1px solid #CBD7DF}
.sub:last-child{border-bottom:1px solid #CBD7DF}
.sub summary{display:flex;justify-content:space-between;align-items:center;gap:16px;min-height:60px;padding:14px 0;cursor:pointer;list-style:none;font-size:19px;font-weight:800;color:#071B2B}
.sub summary::-webkit-details-marker{display:none}
.sub summary em{margin-left:auto;font-style:normal;font-size:13px;font-weight:600;color:#44596B;white-space:nowrap}
.sub summary::after{content:"+";flex:none;display:grid;place-items:center;width:32px;height:32px;border:1.5px solid #9CB1C0;font-size:20px;font-weight:600;color:#071B2B}
.sub[open] summary::after{content:"\\2212";background:#F5A623;border-color:#F5A623}
.sub .items{border-top:0;margin:0 0 20px;padding:0}
.sub .items li{padding:13px 0 13px 26px}
.sub .items li::before{top:25px}
.sub .items b{display:block;font-size:16.5px;color:#1D3447}
.sub .items span{display:block;margin-top:4px;font-size:15px;font-weight:500;line-height:1.55;color:#44596B}
'''
k=d.index('/* environment pages */')
d=d[:k]+css+d[k:]
open(p,'w',encoding='utf-8').write(d)
# build script select
bp='/tmp/claude-0/-home-claude-begasenergysdnbhd/17968c45-2054-5a39-bd08-3abb794e1ea7/scratchpad/build_site.py'
b=open(bp).read()
b=re.sub(r'<option value="">Select a service group</option>.*?<option>Other or not sure</option>','<option value="">Select a service group</option>'+''.join('<option>%s</option>'%E(s) for s in shorts)+'<option>Other or not sure</option>',b,flags=re.S)
open(bp,'w').write(b)
import shutil;shutil.copy(bp,R+'/tools/build_site.py')
print('groups',len(out),[len(re.findall('<li><b>',o)) for o in out])
