# Publication list pipeline

`build_pubs.py` turns three ADS libraries into the three refereed publication
sections of the CV. `minimal-resume.tex` `\input`s the result.

```bash
make            # refresh from ADS + rebuild the PDF
make offline    # rebuild from the cached ADS response (no network)
make check      # fonts embedded, no LaTeX errors
```

## Division of labour

- **`build_pubs.py` owns content.** Author lists, journal strings, ordering,
  counters.
- **`minimal-resume.tex` and `config/` own appearance.** Fonts, spacing,
  section headings.

If you find yourself parsing text in the `.tex`, or setting font sizes in
Python, the change is in the wrong file.

**Never hand-edit `generated/*.tex`** — every build clobbers it. Corrections
go in `overrides.yaml`.

## How the sections are split

Three nested ADS libraries, differenced:

| CV section | set |
|---|---|
| Lead-Author Publications | `lead` |
| Publications as Co-Lead or Supervising Author | `leadcolead − lead` |
| Co-Authored Publications | `all − leadcolead` |

No author-position parsing: membership is whatever you curated in ADS. Move a
paper between sections by moving it between libraries. The build asserts
`lead ⊆ leadcolead ⊆ all` and stops if that breaks, so a paper filed in only
the small library is an error rather than a silent omission.

`Unrefereed Publications` is **not** generated — it is hand-written in
`minimal-resume.tex`, because white papers, astrobites and press pieces are
not consistently in ADS.

## `overrides.yaml`

Everything ADS cannot know:

| key | purpose |
|---|---|
| `libraries` | the three ADS library IDs |
| `self_ads_name` | who to bold |
| `advisees` | who gets the `$^\ast$` |
| `name_fixes` | ADS spells some people two ways; normalise before matching |
| `exclude` | in a library but not a refereed CV entry (e.g. the Via overview) |
| `journal_overrides` | where an eprint was submitted — ADS has no such field |
| `year_overrides` | force a display year |
| `refereed_only` | count only `doctype=article` in `\ntot` |

The build warns about **stale** overrides — a `journal_overrides` entry whose
paper is now published — so the file cleans itself up as papers progress.

Papers with no ADS record are deliberately out of scope: the CV shows exactly
what is in the libraries. To add a paper, add it to ADS.

## Warnings are the point

A clean run is not the goal; read the warnings. They flag the three things
that need a human:

1. `NO journal known for preprint …` — add it to `journal_overrides`.
2. `journal read from arXiv comment …` — guessed from free text; pin it if wrong.
3. `no final pagination yet` — rendered as "in press"; correct until the
   volume/page appear, then it fixes itself.

## The token

Read from `~/.ads/dev_key` (chmod 600) or `$ADS_DEV_KEY`. Deliberately never
read from inside the repo, so it cannot be committed. Get one at
<https://ui.adsabs.harvard.edu/user/settings/token>.

## Known cosmetic difference

ADS title case is not uniform across journals — MNRAS records come back
sentence-cased ("Computational tools for the spectroscopic analysis…") while
ApJ records are title-cased. The old hand-written CV title-cased everything.
Normalising this automatically is risky (`SDSS-V`, `LP 398-9`, `r-process`),
so it is left as ADS provides it.
