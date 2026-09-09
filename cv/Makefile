.PHONY: all pubs offline pdf publish clean check

PDF  := minimal-resume.pdf
TEX  := minimal-resume.tex
GEN  := generated/pubs-lead.tex generated/pubs-colead.tex \
        generated/pubs-other.tex generated/pubs-counts.tex
LOG  := minimal-resume.log
CFG  := $(wildcard config/*.tex config/*.sty)

# Where the Jekyll site serves the CV from. Relative, so the whole cv/
# directory stays movable.
SITE_PDF := ../assets/cv.pdf

# Refresh publications from ADS, rebuild, and update the copy the site serves.
all: pubs pdf publish

# Hit the ADS API and regenerate generated/*.tex.
pubs:
	python3 pubs/build_pubs.py

# Same, but from the cached ADS response -- works on a plane.
offline:
	python3 pubs/build_pubs.py --offline

# Two passes: etaremune needs the second to settle its numbering.
pdf: $(PDF)

$(PDF): $(TEX) $(GEN) $(CFG)
	xelatex -interaction=nonstopmode $(TEX) >/dev/null
	xelatex -interaction=nonstopmode $(TEX) >/dev/null
	@pdfinfo $(PDF) | grep -E '^(Pages|Page size)'

# Overwrite the PDF the website serves. Runs check first: a CV with a
# dropped font or a LaTeX error should never reach assets/.
publish: check
	@test -d $(dir $(SITE_PDF)) || { \
	  echo "no $(dir $(SITE_PDF)) -- is cv/ still inside the website repo?"; \
	  exit 1; }
	cp $(PDF) $(SITE_PDF)
	@echo "published -> $(SITE_PDF) ($$(pdfinfo $(SITE_PDF) | awk '/^Pages/{print $$2}') pages)"
	@echo "   run 'make cv' from the repo root to commit + push it live."

# Fonts embedded, and no LaTeX errors left in the log.
check: $(PDF)
	@pdffonts $(PDF) | awk 'NR==1 {emb=index($$0,"emb")} \
	  NR>2 && substr($$0,emb,3)!="yes" {print "NOT EMBEDDED:", $$1; bad=1} \
	  END {if (!bad) print "all fonts embedded"}'
	@# Two error formats: bare xelatex writes "! msg", latexmk (and the VS Code
	@# build) passes -file-line-error and writes "./file.tex:42: msg".
	@! grep -Eq '^!|^[^ ]+:[0-9]+: ' $(LOG) || { \
	  echo "LaTeX errors in $(LOG):"; \
	  grep -E '^!|^[^ ]+:[0-9]+: ' $(LOG) | head -5; exit 1; }
	@echo "check passed"

clean:
	rm -f *.aux *.log *.out *.toc *.xdv *.fls *.fdb_latexmk *.synctex.gz $(PDF)
