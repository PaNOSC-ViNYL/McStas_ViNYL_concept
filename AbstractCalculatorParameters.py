from abc import ABCMeta, abstractmethod

from AbstractBaseClass import AbstractBaseClass
from EntityChecks import checkAndSetPositiveInteger
from EntityChecks import checkAndSetInstance
from EntityChecks import checkAndSetNonNegativeInteger


class AbstractCalculatorParameters(AbstractBaseClass, metaclass=ABCMeta):
    """
    Abstract class for all calculator parameters.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        """
        :param **kwargs:  key=value pairs for calculator specific parameters.
        """
        # Set default for parameters that have to be defined on every Parameters class but
        # depend on the specific calculator.
        self._setDefaults()  # Calls the specialized method!

        # Check and set parameters.
        if 'nodes_per_task' in list(kwargs.keys()):
            self.nodes_per_task = kwargs['nodes_per_task']
        else:
            self.nodes_per_task = 1

        if 'gpus_per_task' in list(kwargs.keys()):
            self.gpus_per_task = kwargs['nodes_per_task']
        else:
            self.gpus_per_task = 0

        if 'cpus_per_task' in list(kwargs.keys()):
            self.cpus_per_task = kwargs['cpus_per_task']
        else:
            self.cpus_per_task = self.__cpus_per_task_default

        if 'forced_mpi_command' in list(kwargs.keys()):
            self.forced_mpi_command = kwargs['forced_mpi_command']
        else:
            self.forced_mpi_command = None  # Will set default "".

    # Queries and
    @property
    def gpus_per_task(self):
        """ Query for the number of gpus per task. """
        return self.__gpus_per_task

    @gpus_per_task.setter
    def gpus_per_task(self, value):
        self.__gpus_per_task = _checkAndSetGPUPerTask(value)

    @property
    def nodes_per_task(self):
        """ Query for the number of nodes per task. """
        return self.__nodes_per_task

    @nodes_per_task.setter
    def nodes_per_task(self, value):
        self.__nodes_per_task = _checkAndSetNodesPerTask(value)

    @property
    def cpus_per_task(self):
        """ Query for the number of cpus per task. """
        return self.__cpus_per_task

    @cpus_per_task.setter
    def cpus_per_task(self, value):
        """ Set the number of cpus per task."""
        self.__cpus_per_task = _checkAndSetCPUsPerTask(value)

    @property
    def forced_mpi_command(self):
        """ Query for the number of cpus per task. """
        return self.__forced_mpi_command

    @forced_mpi_command.setter
    def forced_mpi_command(self, value):
        """ Set the number of cpus per task."""
        self.__forced_mpi_command = _checkAndSetForcedMPICommand(value)

    @abstractmethod
    def _setDefaults(self):
        pass


def _checkAndSetGPUPerTask(value=None):
    """ """
    """ Utility function to check validity of input for number of GPUs per
    task.
    :param value: The value to check.
    :type value: int
    :return: The checked value, default 0.
    """

    return checkAndSetNonNegativeInteger(value, 0)


def _checkAndSetNodesPerTask(value=None):
    """ """
    """ Utility function to check validity of input for number of nodes per
    task.
    :param value: The value to check.
    :type value: int
    :return: The checked value, default 1.
    """

    return checkAndSetPositiveInteger(value, 1)


def _checkAndSetCPUsPerTask(value=None):
    """ """
    """ Utility function to check validity of input for number of cpus per task.
    :param value: The value to check.
    :type value: (int | str)
    :return: The checked value, default 1.
    """

    # Check type
    if isinstance(value, str):
        if not value == "MAX":
            raise ValueError(
                'cpus_per_task must be a positive integer or string "MAX".')
        return value

    return checkAndSetPositiveInteger(value, 1)


def _checkAndSetForcedMPICommand(value):
    """ """
    """ Utility function to check validity of input for forced MPI command.
    :param value: The value to check.
    :type value: str
    """

    return checkAndSetInstance(str, value, "")
