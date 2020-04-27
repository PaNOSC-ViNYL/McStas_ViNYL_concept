from abc import ABCMeta, abstractmethod
import copy

class AbstractBaseClass(object, metaclass=ABCMeta):
#class AbstractBaseClass:
    """
    :class AbstractBaseClass: The SimEx abstract base class from which all SimEx classes derive.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        """
        :param **kwargs:  key=value pairs for calculator specific parameters.
        """

    def __call__(self, **kwargs):
        """
        Copy constructor of the class. Returns an identical or mutated copy of self.
        :param kwargs: List of key-value arguments supported by the class constructor.
        """
        clone = copy.deepcopy(self)

        if kwargs is not None:
            for key,value in kwargs.items():
                setattr(clone, key, value)

        return clone

    def __eq__(self, comp):
        """ Test equality of this and another ABC instance. """
        eq = True
        for key, val in self.__dict__.items():
            if not ( val == comp.__dict__[key] ):
                #print key, val, comp.__dict__[key]
                return not eq

        return eq
