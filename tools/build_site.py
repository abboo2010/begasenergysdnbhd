import re, os, shutil, json
R='/home/claude/begasenergysdnbhd'
src=open(R+'/design/Main.dc.html').read()
css=re.search(r'<style>(.*?)</style>',src,re.S).group(1)
body=src[src.index('<div id="top">'):src.index('</x-dc>')]

order=['home','about','services','onshore','offshore','manpower','hse','experience','contact']
labels={'home':'Home','about':'About Us','services':'Services','onshore':'Onshore','offshore':'Offshore','manpower':'Manpower Outsourcing','hse':'HSE & Quality','experience':'Experience','contact':'Contact Us'}
paths={p:('/' if p=='home' else '/'+p) for p in order}
paths['manpower']='/manpower-outsourcing'
labels['privacy']='Privacy Policy'
paths['privacy']='/privacy-policy'
allpages=order+['privacy']
meta={
'home':('BEGAS Energy Sdn Bhd | Oil & Gas Engineering and Maintenance, Kota Kinabalu','Civil, mechanical and electrical engineering and maintenance services for the oil and gas industry, onshore and offshore. Based in Kota Kinabalu, Sabah.'),
'about':('About Us | BEGAS Energy Sdn Bhd','BEGAS Energy Sdn Bhd was incorporated in Kota Kinabalu in 2008. Meet the leadership and team behind our oil and gas maintenance services.'),
'services':('Services | BEGAS Energy Sdn Bhd','Six capability groups: offshore engineering, onshore fabrication and civil works, electrical and instrumentation, mechanical, marine support and pipeline solutions.'),
'onshore':('Onshore Capabilities | BEGAS Energy Sdn Bhd','Onshore fabrication, civil, electrical, instrumentation and HVAC maintenance for industrial facilities in Sabah.'),
'offshore':('Offshore Capabilities | BEGAS Energy Sdn Bhd','Offshore construction, maintenance, marine support and manpower services for oil and gas operations.'),
'manpower':('Manpower Outsourcing | BEGAS Energy Sdn Bhd','Manpower outsourcing for the oil and gas industry: professional and support services, technical or non-technical, from BEGAS Energy Sdn Bhd.'),
'privacy':('Privacy Policy | BEGAS Energy Sdn Bhd','How BEGAS Energy Sdn Bhd handles personal data shared through this website.'),
'hse':('HSE & Quality | BEGAS Energy Sdn Bhd','Safety in every task. Quality in every delivery. BEGAS Energy health, safety, environment and quality commitments.'),
'experience':('Experience | BEGAS Energy Sdn Bhd','Project experience and case studies from BEGAS Energy Sdn Bhd.'),
'contact':('Contact Us | BEGAS Energy Sdn Bhd','Contact BEGAS Energy Sdn Bhd, KK Times Square, Kota Kinabalu. Email admin@begasenergy.com.'),
}
# extract page sections
pages={}
for m in re.finditer(r'<sc-if value="\{\{show\.(\w+)\}\}"[^>]*>\s*<div class="\{\{cls\.\w+\}\}">(.*?)\n</div>\n</sc-if>',body,re.S):
    pages[m.group(1)]=m.group(2)
assert set(pages)==set(order+['privacy']),set(order+['privacy'])^set(pages)

def conv(h):
    h=re.sub(r'<a ([^>]*?)href="#" onClick="\{\{g\.(\w+)\}\}"',lambda m:'<a %sdata-go="%s" href="%s"'%(m.group(1),m.group(2),paths[m.group(2)]),h)
    return h
contact_form='''
<div class="wrap contact">
  <div>
    <div class="eyebrow">Request an enquiry</div>
    <h2 id="ct-h2" style="margin-bottom:36px">Send us your enquiry.</h2>
    <div class="sent" id="form-sent" role="status" tabindex="-1" hidden>
      <h3>Thank you. Your enquiry has been sent.</h3>
      <p>The BEGAS team will respond as soon as possible. For anything urgent, email admin@begasenergy.com.</p>
      <button class="btn btn-dark" type="button" id="form-again">Send another enquiry</button>
    </div>
    <form class="form" id="enquiry" name="enquiry" method="POST" action="/contact" data-netlify="true" data-netlify-honeypot="bot-field" novalidate>
      <input type="hidden" name="form-name" value="enquiry">
      <div class="field"><label for="fullName">Full name <small>(required)</small></label><input type="text" id="fullName" name="fullName" autocomplete="name" aria-describedby="fullName-err"><span class="err" id="fullName-err" hidden></span></div>
      <div class="field"><label for="company">Company</label><input type="text" id="company" name="company" autocomplete="organization"></div>
      <div class="field"><label for="email">Email address <small>(required)</small></label><input type="email" id="email" name="email" autocomplete="email" aria-describedby="email-err"><span class="err" id="email-err" hidden></span></div>
      <div class="field"><label for="phone">Telephone</label><input type="tel" id="phone" name="phone" autocomplete="tel" aria-describedby="phone-err"><span class="err" id="phone-err" hidden></span></div>
      <div class="field full"><label for="service">Service of interest</label>
        <select id="service" name="service"><option value="">Select a service group</option><option>Instrumentation &amp; Offshore Installation</option><option>Onshore Fabrication &amp; Specialist Commissioning</option><option>Offshore Construction, Maintenance &amp; Repairs</option><option>Electrical Engineering &amp; Construction</option><option>Field Instrumentation Maintenance</option><option>Marine Transportation &amp; Vessel Cleaning</option><option>Other or not sure</option></select></div>
      <div class="field full"><label for="message">Your requirement <small>(required)</small></label><textarea id="message" name="message" aria-describedby="message-err"></textarea><span class="err" id="message-err" hidden></span></div>
      <p class="hp" aria-hidden="true"><label>Do not fill this in: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <div class="field full"><label class="check" for="consent"><input type="checkbox" id="consent" name="consent" aria-describedby="consent-err"><span>I agree that BEGAS Energy may contact me about this enquiry and store the details I provide for that purpose, as described in the <a href="/privacy-policy" data-go="privacy" style="text-decoration:underline">Privacy Policy</a>.</span></label><span class="err" id="consent-err" hidden></span></div>
      <div class="field full" style="flex-direction:row;align-items:center;gap:18px;flex-wrap:wrap"><button class="btn btn-dark" type="submit">Send Enquiry</button><span style="font-size:14px;color:#44596B">Or email <a href="mailto:admin@begasenergy.com" style="font-weight:700;color:#071B2B;border-bottom:2px solid #F5A623">admin@begasenergy.com</a></span></div>
    </form>
  </div>
'''
c=pages['contact']
i=c.index('<div class="wrap contact">'); j=c.index('<aside>')
pages['contact']=c[:i]+contact_form+'  '+c[j:]

nav_links=''.join('<a href="%s" data-go="%s">%s</a>'%(paths[p],p,labels[p]) for p in order)
mob_links=''.join('<a class="ml" href="%s" data-go="%s">%s</a>'%(paths[p],p,labels[p]) for p in order)
foot_company=''.join('<li><a href="%s" data-go="%s">%s</a></li>'%(paths[p],p,labels[p]) for p in order)

# header / footer from design body
head=re.search(r'<header class="nav">.*?</header>',body,re.S).group(0)
foot=re.search(r'<footer class="foot">.*?</footer>',body,re.S).group(0)
header='''<header class="nav">
  <div class="wrap nav-in">
    <a class="brand" href="/" data-go="home" aria-label="BEGAS Energy Sdn Bhd, home"><img src="/assets/begas-logo.png" alt="" width="69" height="46"><div class="brand-txt"><b>BEGAS</b><span>ENERGY SDN BHD</span></div></a>
    <nav class="nav-links" aria-label="Primary">'''+nav_links+'''</nav>
    <a class="btn btn-sm nav-cta" href="/contact" data-go="contact">Request an Enquiry</a>
    <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu"><svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" aria-hidden="true"><path d="M3 6h16M3 11h16M3 16h16"/></svg></button>
  </div>
  <div class="mpanel" id="mobile-menu" hidden>'''+mob_links+'''<div style="margin-top:20px"><a class="btn" style="width:100%" href="/contact" data-go="contact">Request an Enquiry</a></div></div>
</header>'''
foot=re.sub(r'<sc-for list="\{\{navItems\}\}".*?</sc-for>',foot_company,foot,flags=re.S)
foot=conv(foot)
foot=foot.replace('<span>© 2026 BEGAS Energy Sdn Bhd. All rights reserved.</span>','<span>&copy; 2026 BEGAS Energy Sdn Bhd. All rights reserved.</span>')
foot=foot.replace('<img src="/_blob/9ce8bf379ce8e5b5f54bc2858c21dc84" alt="">','<img src="/assets/begas-logo.png" alt="" width="69" height="46">')

extra_css='''
.panel[hidden]{display:none}
.mpanel[hidden]{display:none}
@media (min-width:1181px){.mpanel{display:none!important}}
.mpanel{padding:8px 20px 28px}
.err{display:block}
.err[hidden]{display:none}
.sent[hidden]{display:none}
main:focus{outline:none}
'''
css=css+extra_css

ld=json.dumps({"@context":"https://schema.org","@type":"Organization","name":"BEGAS Energy Sdn Bhd","url":"https://begasenergy.com/","logo":"https://begasenergy.com/assets/begas-logo.png","foundingDate":"2008-09-04","email":"admin@begasenergy.com","address":{"@type":"PostalAddress","streetAddress":"I-49-3A, Signature Office, KK Times Square, Off Coastal Highway, Jalan Coastal","addressLocality":"Kota Kinabalu","addressRegion":"Sabah","postalCode":"88100","addressCountry":"MY"}},indent=1)

js=open(os.path.join(os.path.dirname(__file__),'site.js')).read()
SITE='https://begasenergy.com'
def page_html(active):
    t,d=meta[active]
    panels=''
    for p in allpages:
        inner=conv(pages[p])
        inner=re.sub(r'<sc-for.*?</sc-for>','',inner,flags=re.S)
        hid='' if p==active else ' hidden'
        panels+='<div class="panel" data-page="%s"%s>%s</div>\n'%(p,hid,inner)
    nav_active=header.replace('data-go="%s"'%active,'data-go="%s" aria-current="page" class="on"'%active) if False else header
    return '''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s%s">
<meta name="theme-color" content="#071B2B">
<meta property="og:type" content="website"><meta property="og:site_name" content="BEGAS Energy Sdn Bhd"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s%s">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">%s</script>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<div class="sr" role="status" aria-live="polite" id="announce"></div>
%s
<main id="main" class="stage" tabindex="-1">
%s</main>
%s
<script src="/assets/site.js" defer></script>
</body>
</html>
'''%(t,d,SITE,paths[active],t,d,SITE,paths[active],ld,header,panels,foot)

S=R+'/site'
shutil.rmtree(S,ignore_errors=True)
os.makedirs(S+'/assets')
shutil.copy(R+'/assets/begas-logo.png',S+'/assets/')
shutil.copytree(R+'/assets/images',S+'/assets/images')
for f in os.listdir(R+'/assets/favicon'): shutil.copy(R+'/assets/favicon/'+f,S+'/'+f)
open(S+'/assets/site.css','w').write(css)
open(S+'/assets/site.js','w').write(js)
meta_js='window.BEGAS_META='+json.dumps({paths[p]:{'p':p,'t':meta[p][0],'d':meta[p][1]} for p in allpages})+';\n'
open(S+'/assets/site.js','w').write(meta_js+js)
for p in allpages:
    d=S if p=='home' else S+paths[p]
    os.makedirs(d,exist_ok=True)
    open(d+'/index.html','w').write(page_html(p))
open(S+'/robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n'%SITE)
open(S+'/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>%s%s</loc></url>\n'%(SITE,paths[p]) for p in allpages)+'</urlset>\n')
open(S+'/404.html','w').write(page_html('home').replace('<title>','<title>Page not found | ',1))
open(R+'/netlify.toml','w').write('''[build]
  publish = "site"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "SAMEORIGIN"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
''')
print('ok')
