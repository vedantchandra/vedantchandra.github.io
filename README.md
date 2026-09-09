# vedantchandra.com

My personal website — a Jekyll site served by GitHub Pages — together with the
LaTeX source for my CV.

## Updating the CV

Edit `cv/minimal-resume.tex`. In VS Code, LaTeX Workshop rebuilds on save;
`.vscode/settings.json` pins XeLaTeX, which this template requires. Then:

    make cv

That rebuilds the PDF, checks it, copies it to `assets/cv.pdf`, commits, and
pushes. GitHub Pages redeploys in about a minute — `make status` shows the build.

The three refereed publication sections are generated from ADS, not typed by
hand. To refresh them from ADS and publish in one step:

    make cv-pubs

Corrections go in `cv/pubs/overrides.yaml`. Never edit `cv/generated/*.tex` —
every build overwrites it. Details in `cv/pubs/README.md`.

## Updating the website

Edit `index.md` (about, publications, contact), `research.md`, or `friends.md`.
Then:

    make site

`_layouts/default.html` holds the header and nav bar; `_sass/` holds the styling.

## Requirements

- XeLaTeX (MacTeX / TeX Live) and `latexmk`
- `pdfinfo` and `pdffonts` (poppler)
- for `make cv-pubs`: Python 3 with PyYAML, and an ADS token in `~/.ads/dev_key`
- for `make status`: the GitHub CLI (`gh`)

Run `make` with no arguments for the full list of targets.
