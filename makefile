report.pdf: report.tex figures4 figures5 figures6
	pdflatex -interaction=nonstopmode -halt-on-error report.tex
	pdflatex -interaction=nonstopmode -halt-on-error report.tex

figures4: section4.py sim_GLM.py fit_GLM.py
	python3 section4.py

figures5: section5.py sim_GLM.py fit_GLM.py
	python3 section5.py

figures6: section6.py
	python3 section6.py

DavisGagnerFinalProject.zip: report.pdf sim_GLM.py fit_GLM.py section4.py section5.py section6.py
	zip DavisGagnerFinalProject.zip report.pdf sim_GLM.py fit_GLM.py section4.py section5.py section6.py \
	binned_spikes_cell_1.txt binned_spikes_cell_2.txt binned_stim_cell_1.txt binned_stim_cell_2.txt ISIsimulated.txt

clean:
	rm -f report.aux report.out report.log figures? *.pdf
