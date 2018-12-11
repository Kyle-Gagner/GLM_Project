report.pdf: report.tex figures4 figures5 figures6
	pdflatex -interaction=nonstopmode -halt-on-error report.tex
	pdflatex -interaction=nonstopmode -halt-on-error report.tex

figures4: section4.py sim_GLM.py fit_GLM.py
	python3 section4.py

figures5: section5.py sim_GLM.py fit_GLM.py
	python3 section5.py

figures6: section6.py
	python3 section6.py

clean:
	rm -f report.aux report.out report.log figures? *.pdf
