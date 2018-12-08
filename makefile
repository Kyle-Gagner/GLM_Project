report.pdf: report.tex figures4 figures5
	pdflatex -interaction=nonstopmode -halt-on-error report.tex

figures4: section4.py
	python3 section4.py

figures5: section5.py
	python3 section5.py

clean:
	rm -f report.aux report.out report.log figures4 figures5 *.pdf
