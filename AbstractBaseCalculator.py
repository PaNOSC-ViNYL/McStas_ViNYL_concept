""":module AbstractBaseCalculator: Hosting the base class of all Calculators."""
##########################################################################
#                                                                        #
# Copyright (C) 2015-2018 Carsten Fortmann-Grote                         #
#               2016-2017 Sergey Yakubov                                 #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################
from abc import ABCMeta, abstractmethod

from AbstractBaseClass import AbstractBaseClass
from AbstractCalculatorParameters import AbstractCalculatorParameters
#from Utilities import ParallelUtilities
from EntityChecks import checkAndSetInstance
import dill
import os
import sys

class AbstractBaseCalculator(AbstractBaseClass, metaclass=ABCMeta):
    """
    :class AbstractBaseCalculator: Abstract class for all simulation calculators.
    """
    @abstractmethod
    def __init__(self, parameters=None, input_path=None, output_path=None):
        """
        :param parameters: Parameters of the calculation (not data).
        :type parameters: dict || AbstractCalculatorParameters
        :param input_path: Path to hdf5 file holding the input data.
        :type input_path: str
        :param output_path: Path to hdf5 file for output.
        :type output_path: str
        """

        # Check parameters.
        self.__parameters = checkAndSetParameters(parameters)

        self.__input_path, self.__output_path = checkAndSetIO((input_path, output_path))


    @classmethod
    def runFromCLI(cls):
        """
        Method to start calculator computations from command line.
        :return: exit with status code
        """
        if len(sys.argv) == 2:
            fname = sys.argv[1]
            calculator=cls.dumpLoader(fname)
            status = calculator._run()
            sys.exit(status)

    @classmethod
    def dumpLoader(cls,fname):
        """
        Creates calculator object from a dump file
        :param fname: path to the dump file.
        :return: Created calculator object.
        :raises RuntimeError: if cannot create object.
        """

        try:
            with open(fname,'rb') as file_handle:
                calculator = dill.load(file_handle)

        except:
            raise IOError("Cannot read  from file "+fname)
        if not issubclass(type(calculator),AbstractBaseCalculator):
            raise TypeError( "The argument to the script should be a path to a file "
                             "with object of subclass of AbstractBaseCalculator")
        return calculator

    @abstractmethod
    def backengine(self):
        """
        Method to call the backengine for the calculator.
        To be implemented on the derived classes.
        """
        pass

    @abstractmethod
    def expectedData(self):
        """
        Query for the data fields expected by this calculator.
        """
        # To be implemented in specialized calculators.
        pass

    @abstractmethod
    def providedData(self):
        """
        Query for the data fields provided by this calculator.
        """
        # To be implemented by specialized calculator.
        pass

#    @abstractmethod
    def _run(self):
        """
        Method to do computations. By default starts backengine.
        :return: status code.
        """
        result=self.backengine()

        if result is None:
            result=0

        return result
        # Can be reimplemented by specialized calculator.

    def dumpToFile(self, fname):
        """
        dump class instance to file.
        :param fname: Path to file to dump.
        """

        try:
            with open(fname, "wb") as file_handle:
                dill.dump(self, file_handle)
        except:
            raise IOError("Cannot dump to file "+fname)


    @abstractmethod
    def _readH5(self):
        pass

    @abstractmethod
    def saveH5(self):
        pass

    #######################################################################
    # Queries and setters
    #######################################################################
    # control_parameters

    @property
    def parameters(self):
        """ Query for the control parameters of the calculator."""
        return self.__parameters
    @parameters.setter
    def parameters(self, value):
        """ Set the control parameters for the calculation. """
        if isinstance( value, AbstractCalculatorParameters):
            self.__parameters = value
            return
        self.__parameters = checkAndSetInstance(dict, value, None)
    @parameters.deleter
    def parameters(self):
        """ Delete the control parameters.  """
        del self.__parameters

    # input
    @property
    def input_path(self):
        """ Query for the input file path(s). """
        return self.__input_path
    @input_path.setter
    def input_path(self, value):
        """ Set the io path(s) to a value. """
        self.__input_path = checkAndSetInstance( (str, list), value, None   )
    @input_path.deleter
    def input_path(self):
        """ Delete the input_path path(s). """
        del self.__input_path

    # output
    @property
    def output_path(self):
        """ Query for the output file path(s). """
        return self.__output_path
    @output_path.setter
    def output_path(self, value):
        """ Set the io path(s) to a value. """
        self.__output_path = checkAndSetInstance( (str, list), value, None   )
    @output_path.deleter
    def output_path(self):
        """ Delete the output_path path(s). """
        del self.__output_path

def checkAndSetIO(io):
    """ Check the passed io path/filenames and set appropriately. """

    # Check we have a tuple.
    io = checkAndSetInstance(tuple, io)
    if len(io) != 2:
        raise RuntimeError("The parameter 'io' can only be a tuple of two strings.")

    # Check if input exists, if not, raise.
    i = checkAndSetInstance(str, io[0])
    if i is None:
        raise IOError("The parameter 'input_path' must be a valid filename.")
    i = os.path.abspath(i)
#
    # Check if output file exists, otherwise attempt to create it.
    o = checkAndSetInstance(str, io[1])
    if o is None:
        raise IOError("The parameter 'output_path' must be a valid filename.")
    o = os.path.abspath(o)

    return (i, o)

def checkAndSetBaseCalculator(var=None, default=None):
    """
    Check if passed object is an AbstractBaseCalculator instance. If non is given, set to given default.
    :param var: The object to check.
    :param default: The default to use.
    :return: Te checked photon source object.
    :raises RuntimeError: if no valid BaseCalculator was given.
    """

    return checkAndSetInstance(AbstractBaseCalculator, var, default)

def checkAndSetParameters(parameters):
    """ Utility to check if the 'parameters' argument is valid input.
    :param parameters: The parameters object to check.
    :type parameters: dict or AbstractCalculatorParameters
    :return: The checked parameters object.
    """
    if parameters is None:
        parameters = {}
    if not (isinstance( parameters, dict ) or isinstance( parameters, AbstractCalculatorParameters) ):
        raise TypeError( "The 'parameters' argument to the constructor must be of type dict or AbstractCalculatorParameters.")

    # Return.
    return parameters
