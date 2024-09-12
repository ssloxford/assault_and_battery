# ACSAC 2024 - Assault and Battery

Artifacts for _Assault and Battery: Evaluating the Security of Power Conversion Systems Against Electromagnetic Injection Attacks_, accepted at ACSAC 2024.

The repository contains the code used for data collection, the data files, and code used for plotting.

## Data collection

This repository contains the data collection scripts in `code/`:
- `dcdc_cv_measurement.py`: Measurements on loaded DC-DC converters, when operating in voltage limited mode, and using a CR load.
- `dcdc_cc_measurement.py`: Measurements on loaded DC-DC converters, when operating in current limited mode, and using a CV load.
- `chg_cv_measurement.py`: Measurements on battery chargers in the CV stage.
- `chg_cc_measurement.py`: Measurements on battery chargers in the CC stage.
- `cs_measurement.py`: Measurements of current sensors being fed a set current.
- `power_measurement.py`: Measurements on various devices, where the power is varied instead of frequency.
- 
Running this code requires the same measurements instruments used to run the experiments.
They are provided as an example for using the measurement library.

To run similair experiments, the following steps are necessary:
- Decide on the type of experiments (what e.g. what load will be applied, what voltages will be used)
- Either:
  - Obtain instruments already supported by the data collection library (signal generator, oscilloscope)
  - Implement new instruments based on the available templates. Further instructions for this are described in the repository: `https://github.com/ssloxford/emi_experiment_lib`
- Modify the data colection scripts:
  - To reference the relevant instruments, in the desired configuration
  - Configure the desired frequency and power ranges for the parametric sweeps.

## Example experiment
For example, to examine how a 5V power supply reacts to EMI when loaded at 1A. This follows the `dcdc_cv_measurement.py` script:
- Measurement instruments 
  - Obtain a 5 Ohm resistor to use as load, and an oscilloscope (Rigol DS2302A is supported by the library)
  - OR obtain a DC load (the Rigol DL3021A is supported by default)
  - Configure the instruments appropriately, either manualy or from the code.
  - The code shows how to set up the channels of the oscilloscope, and change the load on the DC load
  - The chosen instruments are passed to the third arguments of the `ExperimentLogger` constructor.
- RF Source
  - Find a signal generator instrument, or an SDR. The R&S SMC 100A, USRP N210, HackRF are supported by default.
  - The chosen instrument is passed to the second arguments of the `ExperimentLogger` constructor.
  - Optionally, if high powered signals are needed, connect an RF amplifier to the source
  - Connect an appropriate antenna, and place it next to the tested device
  - It is recommended to fix the antenna and tested power supply, so that they do not move during the experiment.
- Choose the sweep parameters
  - Generate a list of frequencies to sweep through, and choose power to use. These are provided in the `data=` parameter of the `ExperimentLogger` constructor.
- Run the python file: the code connects to the instruments, and performs the sweep.

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

## Software version & Installation

Developed using Python 3.9 on Windows.
Also tested using Python 3.10.12 on Ubuntu 24.04.1 LTS.
The code does not use special features, and should be compatible with most other systems.
In addition to standard python packages (`numpy, pandas, matplotlib, seaborn, asyncio`), it requires using a custom python package `https://github.com/ssloxford/emi_experiment_lib` for collection and loading experimental data.

Installation commands (Ubuntu 24.04.1 LTS, Python 3.10.12):
```sh
#Install packages
sudo apt update
sudo apt install python3-pip jupyter-core jupyter-notebook "fonts-cmu"
# Install python modules
# Version of numpy is pinned to ensure binary compatbility with pandas
pip install matplotlib seaborn asyncio numpy==1.26.4 pandas 
# Make sure matplotlib finds the font
python3 -c "exec(\"import matplotlib.font_manager\nmatplotlib.font_manager._load_fontmanager(try_read_cache=False)\")"

# Install additional custom exp_lib package, and test it
git clone https://github.com/ssloxford/emi_experiment_lib
cd emi_experiment_lib/
pip install .
python3 demo_main.py
python3 demo_main.py
python3 demo_loader.py

cd ..

# Download main artifact code, and run
git clone https://github.com/ssloxford/assault_and_battery
cd assault_and_battery/code
jupyter execute plots.ipynb

# Generated plots can be found in ../plots
```


