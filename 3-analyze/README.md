# Analyzing the results

In this folder you find scripts to help you analyze your results.

(Note: the folder `eos_utils` is needed by the scripts, you don't need to modify it).

## `get_errors.py`

Run it to store some information on the EOS workchains that failed.
It expects that you already created the file `../plugin_name.txt` (see README file in the folder `1-preliminary` for more details). It will generate a file `outputs/errors-<PLUGIN_NAME>.json` with a summary of UUIDs, exit status, and the `verdi process report` output of the EOS workchains that did not finish with a 0 exit status.

## `get_results.py`

The main script to get results from your calculations.
It expects that you already created the file `../plugin_name.txt` (see README file in the folder `1-preliminary` for more details).

After you run your simulations, just run this script it with `verdi run` and wait.
It will fit all EOS, and create a couple of files in the `outputs` folder, that you can inspect and then share (either by committing those here when they are final, or by copying them in the shared Google Drive).
In particular, it will create:
- `results-<PLUGIN_NAME>.json` with all energy-vs-volume datapoints and the Birch-Murnaghan fit for each material
- `results-warnings-<PLUGIN_NAME>.txt` with some textual information on warnings (the same that are also printed on screen when running the `get_results.py` script).

## Generating the plots
In the `outputs` folder you will find a file `generate_plots.py`. Just run it to create a number of PNG plots of the systems you have run. These PNGs will be stored in a subfolder `plots-<PLUGIN_NAME>`, and each PNG will contain the data points and the fit, if successful, for those systems where the EOS workchains succeeded and generated the EOS energy-vs-volume points.

If you want to generate comparison plots of your code with one of the other codes, you can then instead pass an additional parameter to the `generate_plots.py` with the code you want to compare with (i.e. `./generate_plots.py <OTHER_PLUGIN>`, where `<OTHER_PLUGIN>` is e.g. `quantum_espresso`, `cottenier-wien2k`, ...). NOTE: You need to first put the corresponding `results-warnings-<PLUGIN_NAME>.txt` in the same folder.
These PNGs will be stored in a subfolder `plots-<PLUGIN_NAME>-vs-<OTHER_PLUGIN>`. The PNGs will be very similar to those without comparison, but in addition (where available) the fit of the other plugin will be shown, as well as a red region highlighting the difference in EOS between the two plugins.

## Creating a single collated PDF
If you want to create a single PDF from all PNG plots, to inspect graphically the results do the following:

- go in the folder `collate-plots`
- run the `create_latex_file.py`:
  - if you want to collate the plots of your plugin only, just run `create_latex_file.py`
  - if you want to collate the plots of your plugin compared with another plugin `<OTHER_PLUGIN>`, specify the name of the other plugin as a parameter: `create_latex_file.py <OTHER_PLUGIN>` (you need, of course, to have generated the right plots in the previous step).
- enter the `tex-template` subfolder
- run `pdflatex results.tex`
- inspect the output `results.pdf`, possibly rename it appropriately (with your plugin name and possibly the plugin you are comparing with) and share it on the Google Drive.
