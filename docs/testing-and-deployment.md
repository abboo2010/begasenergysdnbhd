# Testing report and deployment checklist (October 2026)

## Automated checks run
- 10 pages (Home, About, Services, Onshore, Offshore, Manpower Outsourcing, HSE & Quality, Experience, Contact, Privacy Policy) at 1440px and 390px wide.
- axe-core, WCAG 2.0/2.1/2.2 A and AA rules: **0 violations** on every page (one contrast issue found and fixed).
- No horizontal scrolling on any page at 390px. No duplicate element ids. No dead (`#`) links.
- Page navigation, browser back button, mobile menu and form validation tested in Chromium.
- UK English spelling sweep done.

## Not yet tested (needs the live site)
- Enquiry form delivery (Netlify Forms) and email notification.
- Real-device and Safari/Firefox testing; Lighthouse performance on the live host.
- Screen-reader walkthrough.

## Deployment checklist
1. Netlify: Add new site > Import from Git > `begasenergysdnbhd`, no build command, publish folder `site` (already set in `netlify.toml`).
2. Netlify > Forms: confirm the `enquiry` form appears, add an email notification to info@begasenergy.com, send a test enquiry.
3. Replace placeholders with real content: photos, certifications and HSE documents, case studies, team photos, privacy policy confirmations (retention, data contact, legal review).
4. Confirm with BEGAS: services listed are all delivered; "most dependable manpower agency in Malaysia" claim; team and leadership wording.
5. Domain: add begasenergy.com in Netlify and update DNS at the registrar (or cloudaccess.net), enable HTTPS.
6. Redirects: old Joomla URLs (`/index.php/...`) to the new pages with 301s in `netlify.toml`, after listing the live URLs.
7. Back up the existing site and database before switching DNS.
8. Submit `https://begasenergy.com/sitemap.xml` to Google Search Console.
