# BEGAS Joomla template (v0.1)

Targets Joomla 4/5 (the live site runs Cassiopeia, so Joomla 4+). **Confirm the exact version in the admin before install.**

## Install
1. Zip the `templates/begas` folder contents (so `templateDetails.xml` is at the zip root).
2. Test site first, not live: System > Install > Extensions > upload.
3. System > Site Templates > set BEGAS as default style.
4. Back up the live site and database before any change.

## Module positions
`menu` (Main Menu, mod_menu), `cta`, `breadcrumbs`, `banner`, `footer-1` to `footer-4`, `footer-bar`, `main-top`, `main-bottom`.
All page content (hero, capabilities, HSE, etc.) is entered as normal Joomla articles/Custom modules, so it stays editable in the admin.

## Still to do
- Page layouts as article content / custom modules (from `design/`)
- Contact form with server-side validation and spam protection
- Menu item aliases and 301 redirects from existing URLs
- SEO: meta, sitemap, structured data
