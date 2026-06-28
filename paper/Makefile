PDF=main.pdf
EXTENDED_PDF=extended_abstract.pdf

.PHONY: all clean tables brief extended

all: $(PDF) $(EXTENDED_PDF)

tables:
	cd .. && /home/eston/anaconda3/envs/global_judge/bin/python src/export_paper_tables.py

brief:
	cd .. && /home/eston/anaconda3/envs/global_judge/bin/python src/make_results_brief.py

$(PDF): main.tex references.bib colm2026_conference.sty colm2026_conference.bst fancyhdr.sty natbib.sty tables/*.tex figures/*.png
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

extended: $(EXTENDED_PDF)

$(EXTENDED_PDF): extended_abstract.tex references.bib
	latexmk -pdf -interaction=nonstopmode -halt-on-error extended_abstract.tex

clean:
	latexmk -C main.tex
	latexmk -C extended_abstract.tex
