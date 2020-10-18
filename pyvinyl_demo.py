import pyvinyl
from mcstasscript.interface import instr, plotter

# Create McStas instrument object
instrument = instr.McStas_instr("mcstas_instrument_name")

src = instrument.add_component("Source", "Source_simple")
src.xwidth = 0.1 # Setup source dimensions
src.yheight = 0.1
src.dist = 2.0 # Setup source focusing
src.focus_xw = 0.03
src.focus_yh = 0.03
instrument.add_parameter("energy") # Create instrument parameter for energy
src.E0 = "energy" # Assign energy instrument parameter to the source energy

det = instrument.add_component("Detector", "PSD_monitor") # Setup a detector
det.xwidth = 0.03
det.yheight = 0.03
det.filename = '"psd.dat"'
det.set_AT([0, 0, 2.0], RELATIVE=src)

# Create a parameter object using pyvinyl syntax
pars = pyvinyl.McStasParameters(instrument=instrument, pars={"energy": 10},
                                ncount=1E7, mpi=4, increment_folder_name=True)

# Create calculator object using pyvinyl and the pars object
calculator = pyvinyl.McStasCalculator(parameters=pars, output_path='test_output')

# Perform simulation using McStas as backengine
data = calculator.backengine()

# Use McStasScript to plot the resulting data
plotter.make_sub_plot(data)
