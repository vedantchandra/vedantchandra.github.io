# Repo-root tasks. One command takes a CV edit all the way to the live site.
#
#   make cv        rebuild the CV -> assets/cv.pdf -> commit -> push -> Pages build
#   make cv-pubs   same, but refresh the publication list from ADS first
#   make site      commit + push everything except the CV (index.md, config, ...)
#   make status    show the GitHub Pages builds for recent pushes
#   make pdf       rebuild the CV PDF only, no git (same as editor build)
#
# Custom commit message:  make cv MSG="Add Hubble fellowship"

SITE_PDF := assets/cv.pdf
BRANCH   := master
MSG      ?=

# Exported, not interpolated into the recipe: a message with newlines or
# quotes would otherwise be pasted straight into /bin/sh and break it.
export MSG
export DEFMSG

.PHONY: help cv cv-pubs site pdf status _push
.DEFAULT_GOAL := help

help:
	@grep -E '^#' $(MAKEFILE_LIST) | head -9 | sed 's/^# \{0,1\}//'

# The usual loop: you edited cv/minimal-resume.tex, now put it on the site.
# cv/Makefile's `publish` runs `check` first, so a CV with a dropped font or
# a LaTeX error never reaches assets/.
cv:
	@$(MAKE) --no-print-directory -C cv publish
	@$(MAKE) --no-print-directory _push PATHS="cv $(SITE_PDF)" DEFMSG="Update CV"

# Same, but hit ADS first and regenerate the publication sections.
# Read the warnings it prints -- see cv/pubs/README.md.
cv-pubs:
	@$(MAKE) --no-print-directory -C cv pubs
	@$(MAKE) --no-print-directory -C cv publish
	@$(MAKE) --no-print-directory _push PATHS="cv $(SITE_PDF)" DEFMSG="Update CV"

# Everything that is not the CV. Deliberately excludes cv/ and assets/cv.pdf
# so a half-finished CV never rides along with a typo fix.
site:
	@$(MAKE) --no-print-directory _push DEFMSG="Update site" \
	  PATHS="index.md research.md friends.md robots.txt CNAME \
	         _config.yml _layouts _includes _sass assets/*.jpg assets/*.mp4 \
	         README.md Makefile .vscode .gitignore"

# Rebuild the PDF without touching git. Identical to the VS Code build.
pdf:
	@$(MAKE) --no-print-directory -C cv pdf

status:
	@gh run list --workflow=pages-build-deployment --limit 5

# ---------------------------------------------------------------------------
# Shared: stage PATHS, commit, push, tell you where to look.
# ---------------------------------------------------------------------------
_push:
	@branch=$$(git rev-parse --abbrev-ref HEAD); \
	if [ "$$branch" != "$(BRANCH)" ]; then \
	  echo "on branch '$$branch', not '$(BRANCH)'."; \
	  echo "GitHub Pages builds '$(BRANCH)' only -- not pushing."; \
	  exit 1; \
	fi; \
	if [ -z "$$(git status --porcelain -- $(PATHS) 2>/dev/null)" ]; then \
	  echo "nothing changed -- the live site already matches."; \
	  exit 0; \
	fi; \
	git add -- $(PATHS); \
	git status --short -- $(PATHS); \
	msg="$$MSG"; [ -n "$$msg" ] || msg="$$DEFMSG"; \
	git commit -q -m "$$msg"; \
	git push -q origin $(BRANCH); \
	echo; \
	echo "pushed. GitHub Pages is rebuilding (~50s):"; \
	echo "    make status                            # watch it"; \
	echo "    https://vedantchandra.com/assets/cv.pdf"
