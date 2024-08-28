from exp_lib.experiment_base import ExperimentLogger

from exp_lib.generator_n210 import GeneratorN210

from exp_lib.detector_dl3021a import DetectorDL3021A
from exp_lib.detector_powermeter import DetectorPowermeter
from exp_lib.detector_multiplex import DetectorMultiplex


from exp_lib.sweep_utils import generate_all_combinations, generate_freqs, generate_sequence, generate_powers_mW, generate_powers_dBm
from exp_lib.utils import VariableData, format_freq

import asyncio
import time

async def main():
    conv = "dcdc5"

    #USRP, 10W amplifier
    generator = GeneratorN210(1e6, "WBX", "192.168.10.2")

    #detector = DetectorDemo(),
    #detector = DetectorPowermeter("COM4", 30),
    #detector_scope = DetectorDS2302A(None, [1,2], [1, 10])

    #V sense channel
    #detector_scope.instr.setDefaults(1)
    #detector_scope.instr.setBW(1, "20M")
    #detector_scope.instr.setScale(1, 0.5)
    #detector_scope.instr.setOffset(1, -3.5)

    #I sense channel
    #detector_scope.instr.setDefaults(2)
    #detector_scope.instr.setBW(2, "20M")
    #detector_scope.instr.setScale(2, 0.1)
    #detector_scope.instr.setOffset(2, -0.1)

    #2ms/div, to safely cover the ripple
    #detector_scope.instr.setTimebase(0.002)

    #Power meter
    #20dB directional coupler and 30dB attenuator to measure power coming in
    detector_pwm = DetectorPowermeter("COM5", attenuator=50)

    detector_load = DetectorDL3021A(None)
    
    #detector_scope.instr.wait()
    detector_load.instr.wait()

    # Wait for scope to settle
    input("Press enter when ready")

    experiment = ExperimentLogger(
        1,
        generator,
        DetectorMultiplex([detector_pwm, detector_load]),

        variables=[
            VariableData("freq", "%f", "Frequency", format_freq),
            VariableData("power", "%f", "Gain"),
        ],
        data = generate_all_combinations(
            [740e6],
            generate_powers_dBm(0, 0.5, 26),
            order=[0,1]
        ),
        savefile=f"pow2/{conv}",
        user_metadata={
            "description": "Power linearity scan"
        },
    )
    await experiment.run()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Closing app")
