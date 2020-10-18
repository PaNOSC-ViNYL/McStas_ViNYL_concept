"""
Using BaseCalculator from libpyvinyl package as base for McStasCalculator
"""
from libpyvinyl.BaseCalculator import BaseCalculator
import mcstasscript

class McStasCalculator(BaseCalculator):
    def __init__(self, parameters=None, dumpfile=None, input_path=None, output_path=None):
        """
        :param parameters : Parameters for McStas run
        :type parameters : McStasParameters

        :param input_path: The path to the input data for the photon source.
        :type input_path:  str

        :param output_path: The path where to save output data.
        :type output: str
        """

        # Overwrites input path with the one used for the McStas instrument
        input_path = parameters.instrument.input_path

        super(McStasCalculator, self).__init__(parameters=parameters, dumpfile=dumpfile,
                                               input_path=input_path, output_path=output_path)

    def backengine(self):
        instr = self.parameters.instrument
        pars = self.parameters.pars

        ncount = self.parameters.ncount
        mpi = self.parameters.mpi
        increment_folder_name = self.parameters.increment_folder_name

        data = instr.run_full_instrument(parameters=pars, foldername=self.output_path,
                                         mpi=mpi, increment_folder_name=increment_folder_name,
                                         ncount=ncount)

        return data

    def expectedData(self):
        pass

    def providedData(self):
        pass

    def _run(self):
        pass

    def _readH5(self):
        pass

    def saveH5(self):
        pass


"""
Using Parameters from libpyvinyl package as base for McStasCalculator
"""

import os
from mcstasscript.interface import instr
from libpyvinyl.BaseCalculator import Parameters

class McStasParameters(Parameters):

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

