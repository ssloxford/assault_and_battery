from exp_lib.experiment_base import ExperimentLogger

from exp_lib.generator_smc100a import Generator_SMC100A

from exp_lib.detector_ds2302a import DetectorDS2302A
from exp_lib.detector_dl3021a import DetectorDL3021A
from exp_lib.detector_multiplex import DetectorMultiplex
from exp_lib.detector_simpleserial import DetectorSimpleSerial

from exp_lib.sweep_utils import generate_all_combinations, generate_freqs, generate_sequence
from exp_lib.utils import VariableData, format_freq

import asyncio
import time

async def main():
    #Sensor and location of antenna
    conv = "cs3_above"
    
    iload = 2
    
    tmp = (str(iload) + ".").split(".")
    if(len(tmp[1]) > 0 and float(tmp[1]) == 0):
        tmp[1] = ""
    iload_str = tmp[0] + "A" + tmp[1]

    #generator = GeneratorDemo()
    generator = Generator_SMC100A(None)
    
    #detector = DetectorDemo(),
    detector_scope = DetectorDS2302A(None, [1])

    #V sense channel (connected to analog output of sensor)
    detector_scope.instr.setDefaults(1)
    detector_scope.instr.setBW(1, "20M")
    detector_scope.instr.setScale(1, 0.5)
    detector_scope.instr.setOffset(1, -2.5)

    #I sense channel
    #detector_scope.instr.setDefaults(2)
    #detector_scope.instr.setBW(2, "20M")
    #detector_scope.instr.setScale(2, 0.1)
    #detector_scope.instr.setOffset(2, -0.4)

    #2ms/div, to safely cover the ripple
    detector_scope.instr.setTimebase(0.002)

    detector_load = DetectorDL3021A(None)

    detector_load.instr.setLoadOn(False)
    detector_load.instr.setLoadMode("CURR", iload)
    detector_load.instr.setLoadOn(True)

    #Serial data from TLI4971 devboard microcontroller, sending current over serial
    #detector_tli4971 = DetectorSimpleSerial("COM12", id_test = "JLink CDC UART Port")
    #Serial data from INA260 microcontroller, sending voltage and current over serial
    #detector_ina260 = DetectorSimpleSerial("COM8", baud=115200, id_test = "Silicon Labs CP210x USB to UART Bridge", count = 2, separator="\t")

    # Wait for scope to settle
    time.sleep(4)
    input("Press enter when ready")

    experiment = ExperimentLogger(
        0.25,
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
        savefile=f"cs/{conv}_{iload_str}.csv",
        user_metadata={
            "description": "Current sensor measurements"
        },
    )
    await experiment.run()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Closing app")
