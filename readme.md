# ACSAC 2024 - Assault and Battery

Artifacts for _Assault and Battery: Evaluating the Security of Power Conversion Systems Against Electromagnetic Injection Attacks_, accepted at ACSAC 2024.

The repository contains the code used for data collection, the data files, and code used for plotting.

## Data collection

This repository contains the data collection scripts in `code/`.
Running this code requires the same measurements instruments used to run the experiments.
It is thus provided mostly for visual inspection.

To run similair experiments, the following steps are necessary:
- Decide on the type of experiments (what e.g. what load will be applied, what voltages will be used)
- Either:
  - Obtain instruments already supported by the data collection library (signal generator, oscilloscope)
  - Implement new instruments based on the available templates
- Modify the data colection scripts:
  - To reference the relevant instruments, in the desired configuration
  - Configure the desired frequency and power ranges for the parametric sweeps.

## Data files

Raw data files from our experiments are located in `data/`.

- DCDC converters in voltage mode in `dcdc_cv`
- ACDC converters in `acdc_v`
- DCDC converters in current mode in `dcdc_cc`
- Current sensor in `cs`
- Battery chargers in `chg`
- Power measurements in `pow2`
- Multi-frequency sweep in `mf`

## Plotting

The plotting code is located in `code/plots.ipynb`.

Running all cells generates the measurement plots shown in the paper.

Requires Computer Modern (CMU Serif) font to be installed system wide for accurate plotting using the Latex font.
Remove the `'font.serif': ["CMU Serif"],` line from the plotting initialization code if this is not available.
In this case, the text on the plots will look different from those presented.

## Software version

Developed and tested using Python 3.9 on Windows.
The code does not use special features, and should be compatible with most other systems.

In addition to standard packages (numpy, pandas, matplotlib, seaborn, asycio), it requires using a custom python package `https://github.com/ssloxford/emi_experiment_lib` for collection and loading experimental data.

