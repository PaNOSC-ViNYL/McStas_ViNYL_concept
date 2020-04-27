import os

from mcstasscript.interface import instr

from AbstractCalculatorParameters import AbstractCalculatorParameters
from EntityChecks import checkAndSetInstance

class McStasParameters(AbstractCalculatorParameters):

    def __init__(self,
                 instrument=None,
                 pars=None,
                 **kwargs
                 ):

        # Check all parameters.
        self.instrument = instrument
        if not isinstance(self.instrument, instr.McStas_instr):
            raise ValueError("Instrument has to be a McStasScript McStas_instr.")

        self.pars = pars
        if not isinstance(self.pars, dict):
            raise ValueError("Instrument pars has to be a dict.")

        super(McStasParameters, self).__init__(**kwargs)

        self.mpi = 1
        if "mpi" in kwargs:
            self.mpi = kwargs["mpi"]
            if not isinstance(self.mpi, int):
                raise ValueError("Number of cores to use, mpi, must be an integer.")

        self.ncount = 1E6
        if "ncount" in kwargs:
            self.ncount = kwargs["ncount"]
            if not isinstance(self.ncount, int) and not isinstance(self.ncount, float):
                raise ValueError("Number of rays to use, ncount, must be an integer.")

        self.increment_folder_name = False
        if "increment_folder_name" in kwargs:
            self.increment_folder_name = kwargs["increment_folder_name"]
            if not isinstance(self.increment_folder_name, bool):
                raise ValueError("Increment foldername mode, must be an bool.")

        self.custom_flags = ""
        if "custom_flags" in kwargs:
            self.custom_flags = kwargs["custom_flags"]
            if not isinstance(self.custom_flags, str):
                raise ValueError("custom_flags for McStas, must be a string.")


    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

    ### New setters and queries
    @property
    def instrument(self):
        """ Query the 'sample' parameter. """
        return self.__instrument

    @instrument.setter
    def instrument(self, val):
        """ Set the 'sample' parameter to val."""
        if val is None:
            raise ValueError("A instrument must be defined with instr attribute.")
        if isinstance(val, instr.McStas_instr):
            self.__instrument = val
        else:
            raise ValueError("instrument must be of type McStas_instr.")

    @property
    def pars(self):
        """ Query the 'sample' parameter. """
        return self.__pars

    @pars.setter
    def pars(self, val):
        """ Set the 'sample' parameter to val."""
        if val is None:
            raise ValueError("pars must be defined with pars attribute.")
        if isinstance(val, dict):
            self.__pars = val
        else:
            raise ValueError("pars must be a dict.")

