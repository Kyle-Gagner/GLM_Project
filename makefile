report.pdf: report.tex figures
	pdflatex -interaction=nonstopmode -halt-on-error report.tex

figures: main.py
	python3 main.py

clean:
	rm -f report.aux report.out report.log figures *.pdf
