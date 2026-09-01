#!/usr/bin/env python3
"""Generate the CV publication sections from ADS libraries.

    python3 pubs/build_pubs.py            # fetch from ADS, write generated/*.tex
    python3 pubs/build_pubs.py --offline  # rebuild from pubs/cache/ads_raw.json

Sections are split by set arithmetic over three nested ADS libraries:

    lead    = L_lead
    colead  = L_leadcolead - L_lead
    other   = L_all        - L_leadcolead

This needs no author-position parsing: membership is whatever you curated in
ADS. The nesting is asserted on every run, so a paper filed in the wrong
library is a build error rather than a silently missing entry.

This script owns *content*. minimal-resume.tex and config/ own *appearance*.
Never hand-edit anything in generated/ -- every run clobbers it. Corrections
belong in pubs/overrides.yaml.
"""

import argparse
import html
import json
import pathlib
import re
import sys
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
CACHE = HERE / "cache" / "ads_raw.json"
OUT = ROOT / "generated"

API = "https://api.adsabs.harvard.edu/v1"
ABS = "https://ui.adsabs.harvard.edu/abs/{}/abstract"

# A real page: 146, L24, e12. Not: stag1254 (MNRAS advance access).
PAGE_RE = re.compile(r"^[Le]?\d+$")

# Fields pulled from ADS. Keep in sync with what render_item() uses.
FL = "bibcode,title,author,year,pub,volume,page,doctype,pubdate,pubnote"


# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------

def load_overrides():
    import yaml
    with open(HERE / "overrides.yaml") as fh:
        return yaml.safe_load(fh) or {}


def token():
    """Read the ADS token from ~/.ads/dev_key or $ADS_DEV_KEY.

    Deliberately never read from the repo, so the key cannot be committed.
    """
    import os
    if os.environ.get("ADS_DEV_KEY"):
        return os.environ["ADS_DEV_KEY"].strip()
    p = pathlib.Path.home() / ".ads" / "dev_key"
    if p.exists():
        return p.read_text().strip()
    sys.exit("No ADS token. Put one in ~/.ads/dev_key or set $ADS_DEV_KEY.\n"
             "Get one at https://ui.adsabs.harvard.edu/user/settings/token")


# --------------------------------------------------------------------------
# ADS fetch
# --------------------------------------------------------------------------

def _req(url, data=None, ctype="application/json"):
    hdr = {"Authorization": f"Bearer {token()}", "Content-Type": ctype}
    return json.load(urllib.request.urlopen(
        urllib.request.Request(url, data=data, headers=hdr)))


def fetch_library(libid):
    """All bibcodes in a library, paginating past the 100-row page size."""
    bibs, start = [], 0
    while True:
        d = _req(f"{API}/biblib/libraries/{libid}?rows=100&start={start}")
        docs = d["documents"]
        bibs += docs
        total = d.get("metadata", {}).get("num_documents", len(bibs))
        if not docs or len(bibs) >= total:
            return bibs
        start += 100


def fetch_metadata(bibcodes):
    """One bigquery call for every paper, rather than N search calls."""
    payload = ("bibcode\n" + "\n".join(bibcodes)).encode()
    url = f"{API}/search/bigquery?q=*:*&fq=%7B!bitset%7D&rows=2000&fl={FL}"
    docs = _req(url, payload, "big-query/csv")["response"]["docs"]
    got = {d["bibcode"] for d in docs}
    missing = [b for b in bibcodes if b not in got]
    if missing:
        sys.exit(f"ADS returned no metadata for: {missing}")
    return docs


def fetch_hindex(bibcodes):
    payload = json.dumps({"bibcodes": bibcodes}).encode()
    d = _req(f"{API}/metrics", payload)
    return int(d["indicators"]["h"])


def fetch_all(cfg):
    libs = {k: fetch_library(v) for k, v in cfg["libraries"].items()}
    for k, v in libs.items():
        print(f"  {k:12s} {len(v):3d}")
    raw = {
        "libraries": libs,
        "docs": fetch_metadata(libs["all"]),
        "hindex": fetch_hindex(libs["all"]),
    }
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(raw, indent=1))
    return raw


# --------------------------------------------------------------------------
# text sanitising
# --------------------------------------------------------------------------

# ADS serves titles with HTML entities, SGML sub/sup tags, and -- reliably --
# U+2500 BOX DRAWINGS LIGHT HORIZONTAL where an en-dash belongs ("Mass─Radius").
UNICODE_MATH = {
    "⊙": r"\odot", "⊕": r"\oplus", "±": r"\pm",
    "≤": r"\leq", "≥": r"\geq", "−": "-", "×": r"\times",
}
DASHES = {"─": "--", "—": "---", "–": "--", "‐": "-"}
ESCAPE = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_"}


def _escape_outside_math(s):
    """Escape LaTeX specials, leaving $...$ spans untouched."""
    out = []
    for i, seg in enumerate(s.split("$")):
        if i % 2:                      # inside math
            out.append(seg)
        else:
            for k, v in ESCAPE.items():
                seg = seg.replace(k, v)
            out.append(seg)
    return "$".join(out)


def clean(s, warn=None):
    s = html.unescape(s)
    s = re.sub(r"<SUB>(.*?)</SUB>", r"$_{\1}$", s, flags=re.I)
    s = re.sub(r"<SUP>(.*?)</SUP>", r"$^{\1}$", s, flags=re.I)
    s = re.sub(r"</?[A-Za-z]+>", "", s)          # any stray SGML
    for k, v in DASHES.items():
        s = s.replace(k, v)
    for k, v in UNICODE_MATH.items():            # only meaningful in math
        s = s.replace(k, v)
    s = _escape_outside_math(s)
    s = re.sub(r"\s+", " ", s).strip()
    # A stray backslash outside math is almost always an ADS artefact.
    if warn is not None and re.search(r"\\(?![a-zA-Z&%#_])", s):
        warn.append(f"odd backslash in: {s[:60]}")
    return s


def flip(name):
    """ADS 'Chandra, Vedant' -> CV 'Vedant Chandra'."""
    if "," in name:
        last, first = name.split(",", 1)
        return f"{first.strip()} {last.strip()}".strip()
    return name.strip()


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def render_authors(authors, cfg):
    me = cfg["self_ads_name"]
    advisees = {a for a in cfg.get("advisees", [])}
    fixes = cfg.get("name_fixes", {})

    def one(a):
        # Normalise first: ADS spells some people more than one way, so self
        # and advisee matching must happen on the canonical form.
        canon = fixes.get(a, a)
        disp = clean(flip(canon))
        if canon == me:
            return r"\textbf{" + disp + "}"
        if canon in advisees:
            return disp + r"$^\ast$"
        return disp

    n = len(authors)
    if n == 1:
        return one(authors[0])
    if n == 2:
        return f"{one(authors[0])} \\& {one(authors[1])}"
    if n <= cfg["max_authors"]:
        return ", ".join(one(a) for a in authors)
    return ", ".join(one(a) for a in authors[:cfg["etal_authors"]]) + ", et al."


# Free-text arXiv comments, e.g. "submitted to ApJ", "Submitted to the Open
# Journal of Astrophysics", "accepted for publication in ApJ", "to appear in
# MNRAS". Authors write these however they like, hence the tolerance.
JOURNAL_HINT = re.compile(
    r"(?P<verb>submitted|accepted|to appear|in press)"
    r"(?:\s+(?:for\s+publication|to\s+be\s+published))?"
    r"\s+(?:to|in|at|by)\s+(?:the\s+)?"
    r"(?P<journal>[A-Za-z][\w .&'-]+)", re.I)

# Canonical journal names, keyed by lowercased abbreviation *and* by
# lowercased full name so that "OJAp" and "Open Journal of Astrophysics"
# converge on one spelling.
_JOURNALS = [
    ("The Astrophysical Journal", ["apj"]),
    ("The Astrophysical Journal Letters", ["apjl"]),
    ("The Astrophysical Journal Supplement Series", ["apjs"]),
    ("The Astronomical Journal", ["aj"]),
    ("Monthly Notices of the Royal Astronomical Society", ["mnras"]),
    ("The Open Journal of Astrophysics", ["ojap"]),
    ("Publications of the Astronomical Society of the Pacific", ["pasp"]),
    ("Astronomy and Astrophysics", ["a&a", "aap", "astronomy & astrophysics"]),
    ("Nature Astronomy", []),
    ("Nature", []),
    ("Science", []),
]
CANON = {}
for _full, _abbrs in _JOURNALS:
    CANON[_full.lower()] = _full
    CANON[re.sub(r"^the ", "", _full.lower())] = _full
    for _a in _abbrs:
        CANON[_a] = _full


def canonical_journal(name):
    key = name.strip().lower()
    return CANON.get(key) or CANON.get(re.sub(r"^the ", "", key)) or name.strip()


def render_journal(doc, cfg, warn):
    """Journal string. Published papers come straight from ADS; preprints need
    a hint, because ADS does not know where an eprint was submitted."""
    bib = doc["bibcode"]
    ov = cfg.get("journal_overrides", {})

    if doc.get("pub") != "arXiv e-prints":
        if bib in ov:
            warn.append(f"stale journal_override (now published): {bib}")
        pub = clean(doc["pub"])
        vol = doc.get("volume")
        page = (doc.get("page") or [None])[0]
        # Advance-access papers carry a submission id ("stag1254") rather than
        # a page. Printing that as a page number would be wrong.
        if page and not PAGE_RE.match(page):
            warn.append(f"{bib}: no final pagination yet (page={page!r}) "
                        f"-- rendering as 'in press'")
            page = None
        if vol and page:
            return f"{pub}, {vol}, {page}"
        if vol:
            return f"{pub}, {vol}, in press"
        return f"{pub}, in press"

    if bib in ov:
        return clean(str(ov[bib]))

    # Fall back to parsing the free-text arXiv comment field.
    note = " ".join(doc.get("pubnote") or [])
    m = JOURNAL_HINT.search(html.unescape(note))
    if m:
        raw = re.split(r"[.,;]| comments| \d", m.group("journal"))[0]
        name = canonical_journal(raw)
        status = "submitted" if m.group("verb").lower() == "submitted" \
            else "in press"
        warn.append(f"journal read from arXiv comment for {bib}: "
                    f"{name!r} ({status}) -- pin it in overrides.yaml if wrong")
        return f"{clean(name)}, {status}"

    warn.append(f"NO journal known for preprint {bib} -- add to "
                f"journal_overrides in overrides.yaml")
    return "submitted"


def render_item(doc, cfg, warn):
    authors = render_authors(doc["author"], cfg)
    title = clean(doc["title"][0], warn)
    year = cfg.get("year_overrides", {}).get(doc["bibcode"], doc["year"])
    url = ABS.format(doc["bibcode"])
    journal = render_journal(doc, cfg, warn)
    return (f"    \\item {authors} ({year}) \\\\\n"
            f"    ``{{{title}}}'' \\\\ "
            f"\\textit{{\\href{{{url}}}{{{journal}}}}}\n")


PREAMBLE = (r"\begin{etaremune}\fontsize{1em}{1em}\fontspec[Path = fonts/,"
            r"LetterSpace= 0,BoldFont=CrimsonText-Bold,"
            r"ItalicFont=CrimsonText-Italic]{CrimsonText-Roman}")


def render_section(docs, cfg, warn):
    body = "\n".join(render_item(d, cfg, warn) for d in docs)
    return ("% GENERATED by pubs/build_pubs.py -- do not edit.\n"
            "% Corrections go in pubs/overrides.yaml.\n"
            f"{PREAMBLE}\n\n{body}\n\\end{{etaremune}}\n")


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true",
                    help="rebuild from pubs/cache/ads_raw.json")
    args = ap.parse_args()

    cfg = load_overrides()

    if args.offline:
        if not CACHE.exists():
            sys.exit(f"No cache at {CACHE}; run once without --offline.")
        raw = json.loads(CACHE.read_text())
        print(f"Using cached ADS data ({CACHE}).")
    else:
        print("Fetching ADS libraries...")
        raw = fetch_all(cfg)

    libs = {k: set(v) for k, v in raw["libraries"].items()}
    excluded = set(cfg.get("exclude", []))

    # The libraries must nest, or the set arithmetic below is meaningless.
    for small, big in (("lead", "leadcolead"), ("leadcolead", "all")):
        orphans = sorted(libs[small] - libs[big])
        if orphans:
            sys.exit(f"ERROR: in '{small}' but not '{big}': {orphans}\n"
                     f"Fix the libraries in ADS, then re-run.")

    groups = {
        "lead":   libs["lead"],
        "colead": libs["leadcolead"] - libs["lead"],
        "other":  libs["all"] - libs["leadcolead"],
    }

    by_bib = {d["bibcode"]: d for d in raw["docs"]}
    warn = []

    for stale in sorted(excluded - libs["all"]):
        warn.append(f"stale exclude (not in any library): {stale}")

    counts, kept = {}, []
    OUT.mkdir(exist_ok=True)
    for name, bibs in groups.items():
        docs = [by_bib[b] for b in bibs if b not in excluded]
        # newest first; etaremune numbers downward so the top item is highest
        docs.sort(key=lambda d: (d.get("pubdate") or "", d["bibcode"]),
                  reverse=True)
        counts[name] = len(docs)
        kept += docs
        path = OUT / f"pubs-{name}.tex"
        path.write_text(render_section(docs, cfg, warn))
        print(f"  wrote {path.relative_to(ROOT)}  ({len(docs)} items)")

    refereed = sum(1 for d in kept if d.get("doctype") == "article")
    total = len(kept) if not cfg.get("refereed_only") else refereed

    counts_tex = (
        "% GENERATED by pubs/build_pubs.py -- do not edit.\n"
        f"\\renewcommand{{\\ntot}}{{{total}}}\n"
        f"\\renewcommand{{\\nlead}}{{{counts['lead']}}}\n"
        f"\\renewcommand{{\\nco}}{{{counts['colead']}}}\n"
        f"\\renewcommand{{\\hindex}}{{{raw['hindex']}}}\n")
    (OUT / "pubs-counts.tex").write_text(counts_tex)

    print(f"\n  lead={counts['lead']}  colead={counts['colead']}  "
          f"other={counts['other']}")
    print(f"  \\ntot={total} (all={len(kept)}, refereed-only={refereed})  "
          f"h-index={raw['hindex']}")
    if excluded & libs["all"]:
        print(f"  excluded {len(excluded & libs['all'])}: "
              f"{sorted(excluded & libs['all'])}")

    if warn:
        print(f"\n{len(warn)} warning(s):")
        for w in sorted(set(warn)):
            print(f"  ! {w}")


if __name__ == "__main__":
    main()
