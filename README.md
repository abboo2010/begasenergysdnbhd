# BEGAS Energy Sdn Bhd: website redesign

- `site/`: the static website (deploy this folder; `netlify.toml` already sets `publish = "site"`)
- `design/`: the design source file
- `assets/`: logo (transparent) and favicons
- `joomla/`: early Joomla template skeleton, parked for now
- `tools/`: script that regenerates `site/` from the design

## Deploying
Netlify: connect this repo, no build command needed. The enquiry form uses Netlify Forms (honeypot spam protection); enable form notifications to admin@begasenergy.com in the Netlify dashboard.
Each page also exists as its own folder (`/about/`, `/services/` ...), so it can be copied to any host, including cloudaccess.net, but the form then needs a different handler.

## Information still required from BEGAS
Vector logo, approved photographs, confirmation of services beyond those published, certifications and HSE documents, approval for case studies and team details, privacy policy text. No certifications, clients or statistics are shown unless verified.
