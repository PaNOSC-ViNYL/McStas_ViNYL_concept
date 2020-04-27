"""
Using some simplified AbstractBase classes for Calculator and Parameter from SimEx
"""

import AbstractBaseClass
import AbstractBaseCalculator
import mcstasscript

class McStasCalculator(AbstractBaseCalculator.AbstractBaseCalculator):
    def __init__(self, parameters=None, input_path=None, output_path=None):
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

        super(McStasCalculator, self).__init__(parameters, input_path, output_path)

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
