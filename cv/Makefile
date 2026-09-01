.PHONY: all pubs offline pdf publish clean check

PDF  := minimal-resume.pdf
TEX  := minimal-resume.tex
GEN  := generated/pubs-lead.tex generated/pubs-colead.tex \
        generated/pubs-other.tex generated/pubs-counts.tex

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

$(PDF): $(TEX) $(GEN) config/minimal-resume.sty
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
	@echo "   commit assets/cv.pdf to put it live."

# Fonts embedded, and no LaTeX errors left in the log.
check: $(PDF)
	@pdffonts $(PDF) | awk 'NR>2 && $$5!="yes" {print "NOT EMBEDDED:", $$1; bad=1} \
	  END {if (!bad) print "all fonts embedded"}'
	@! grep -q '^!' minimal-resume.log || (echo "LaTeX errors in log"; exit 1)
	@echo "check passed"

clean:
	rm -f *.aux *.log *.out *.toc $(PDF)
