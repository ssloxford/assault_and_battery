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
    conv = "dcdc4_below"
    
    vout = 5
    iout = 1
    
    #Generate ohms
    if iout > 0:
        load_res = vout / iout
        tmp = (str(load_res) + ".").split(".")
        if(float(tmp[1]) == 0):
            tmp[1] = ""
        load_res_str = tmp[0] + "O" + tmp[1]
    else:
        load_res_str = "NL"

    generator = Generator_SMC100A(None)

    detector_scope = DetectorDS2302A(None, [1])
    #Current channel connected to analog output of DL3021
    #detector_scope = DetectorDS2302A(None, [1,2], [1, 10], ["voltage_ds2302", "current_ds2302"])
    
    #V sense channel
    detector_scope.instr.setDefaults(1)
    detector_scope.instr.setBW(1, "20M")
    detector_scope.instr.setScale(1, 0.5)
    detector_scope.instr.setOffset(1, -vout)

    #I sense channel
    #detector_scope.instr.setDefaults(2)
    #detector_scope.instr.setBW(2, "20M")
    #detector_scope.instr.setScale(2, 0.1)
    #detector_scope.instr.setOffset(2, -0.3)

    #2ms/div, to safely cover the ripple
    detector_scope.instr.setTimebase(0.002)

    detector_load = DetectorDL3021A(None)
    if(iout > 0):
        load_res = vout / iout
        detector_load.instr.setLoadOn(False)
        detector_load.instr.wait()
        time.sleep(0.5)
        detector_load.instr.setLoadMode("RES", load_res)
        detector_load.instr.wait()
        time.sleep(0.5)
        detector_load.instr.setLoadOn(True)
    else:
        detector_load.instr.setLoadOn(False)

    detector_scope.instr.wait()
    detector_load.instr.wait()

    # Wait for scope to settle
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
            [19],
            order=[1,0]
        ),[(50e6, -100)]),
        savefile=f"dcdc_cv/{conv}_{vout}V_{load_res_str}.csv",
        user_metadata={
            "description": "DCDC converter voltage attack"
        },

    )
    await experiment.run()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Closing app")
