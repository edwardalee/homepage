# homepage
Home page for Edward A. Lee

Legacy URL: https://ptolemy.berkeley.edu/~eal/

## GitHub Pages deployment

This repo builds a static copy for GitHub Pages via GitHub Actions
(`.github/workflows/pages.yml`). The build script expands SSI includes and
rewrites legacy `/~eal/` links for the deployed location.

After enabling **Settings → Pages → Source: GitHub Actions** on
`edwardalee/homepage`, pushes to `master` deploy to:

**https://edwardalee.github.io/homepage/**

### Serving under ptolemy.org/~eal/

GitHub allows only one custom domain per Pages site, so `ptolemy.org` is used
by the main [ptweb](https://github.com/icyphy/ptweb) repo. To mirror the legacy
`ptolemy.org/~eal/` URL, build this site into the ptweb artifact at `_site/~eal/`
(with `SITE_BASE_PATH=/~eal`) from the ptweb workflow, or use a subdomain such
as `eal.ptolemy.org` for this repo.

## Local Preview

This site uses Server Side Includes (SSI) for headers and footers.

1. **Static build preview** (matches GitHub Pages output):
   ```bash
   SITE_BASE_PATH=/homepage ./bin/build-for-pages
   python3 -m http.server 8000 --directory _site
   ```
   Open http://localhost:8000/index.html

2. **Live SSI preview** (legacy Berkeley-style `/~eal/` URLs):
   ```bash
   python serve.py
   ```
   Open http://localhost:8000/~eal/index.html

Press Ctrl+C to stop either server.
