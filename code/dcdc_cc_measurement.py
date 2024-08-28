from exp_lib.experiment_base import ExperimentLogger

from exp_lib.generator_smc100a import Generator_SMC100A

from exp_lib.detector_ds2302a import DetectorDS2302A
from exp_lib.detector_dl3021a import DetectorDL3021A
from exp_lib.detector_multiplex import DetectorMultiplex

from exp_lib.sweep_utils import generate_all_combinations, generate_freqs, generate_sequence
from exp_lib.utils import VariableData, format_freq

import asyncio
import time

async def main():
    #device and placement of antenna
    conv = "dcdc1_below"
    
    vload = 7
    ilim = 1
    
    #Generate file name component by replacing . with symbol
    tmp = (str(vload) + ".").split(".")
    if(len(tmp[1]) > 0 and float(tmp[1]) == 0):
        tmp[1] = ""
    vload_str = tmp[0] + "V" + tmp[1]

    tmp = (str(ilim) + ".").split(".")
    if(len(tmp[1]) > 0 and float(tmp[1]) == 0):
        tmp[1] = ""
    ilim_str = tmp[0] + "A" + tmp[1]

    generator = Generator_SMC100A(None)

    detector_scope = DetectorDS2302A(None, [1], [1])

    #V sense channel
    detector_scope.instr.setDefaults(1)
    detector_scope.instr.setBW(1, "20M")
    detector_scope.instr.setScale(1, 0.5)
    detector_scope.instr.setOffset(1, -vload)

    #I sense channel
    #detector_scope.instr.setDefaults(2)
    #detector_scope.instr.setBW(2, "20M")
    #detector_scope.instr.setScale(2, 0.2)
    #detector_scope.instr.setOffset(2, -0.6)

    #2ms/div, to safely cover the ripple
    detector_scope.instr.setTimebase(0.002)

    detector_load = DetectorDL3021A(None)

    detector_load.instr.setLoadOn(False)
    detector_load.instr.setLoadMode("VOLT", vload)
    detector_load.instr.setLoadOn(True)

    # Wait for scope to settle
    time.sleep(4)
    input("Press enter when ready")

    experiment = ExperimentLogger(
        0.5,
        generator,
        DetectorMultiplex([detector_scope, detector_load]),

        variables=[
            VariableData("freq", "%f", "Frequency", format_freq),
            VariableData("power", "%f", "Power"),
        ],
        data = generate_sequence([(50e6, -100)],generate_all_combinations(
            generate_freqs(50e6, 2e6, 0.002, 3000e6),
            [13],
            order=[1,0]
        ),[(50e6, -100)]),
        savefile=f"dcdc_cc/{conv}_{ilim_str}_{vload_str}.csv",
        user_metadata={
            "description": "Constant current measurement"
        },
    )
    await experiment.run()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Closing app")
