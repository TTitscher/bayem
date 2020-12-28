from bayes.parameters import *
import numpy as np

class MultiModelError:
    """
    Purpose:

        * Join a different individual model errors (each with a __call__ routine
          to determine the individual model error) in a joint interfaces via a __call__
          method that can e.g. be provided to an optimization procedure such as scipy-optimize
        * Enable the usage of shared variables that are identical and multiple model errors
          and are thus only once in the global optimization.

    Example:
        * Join multiple data sets (and individual model errors) of a tensile test and potentially
          other tests such as a three point bending test to determine joint material parameters
          such as the Youngs modulus.

    Idea:

        * Idea: The individual model errors as well as the paramter lists are stored a dictionary
          with a unique key to indentify the indivual model errors. The same key is used in the
          joint_parameter_list to store the complete parameter list required as input
          to compute the model error. This joint_parameter_list that provides the functionality
          to update identical variables (labeled shared) in multiple parameter lists.
    """

    def __init__(self):
        self.prms = {}
        self.mes = {}
        self.n = 0
        self.joint_parameter_list = None
        pass

    def add(self, model_error, parameters, key=None):
        """
        Add an individual model error.
        model_error:
            local model error that provides an __call__ method to
            compute the model error

        parameters:
            local list of parameters (see ModelParameter in parameters.py)
            required to compute the model error (in the model error, this list
            is usually passed to the forward model)
        key:
            the key used in the dictionary to access the local model_error and local
            parameter_list. If not provided an integer key is used.
        """
        key = key or self.n
        assert key not in self.prms.keys()
        self.n += 1

        self.mes[key] = model_error
        self.prms[key] = parameters
        return key


    def __call__(self, parameter_vector):
        """
        Updates all latent parameters in the joint_parameter_list
        based on the parameter_vector and evaluates each individual model error
        and concatenates the result into a long vector
        parameter_vector:
            "global" parameter vector exposed to the joint optimization.
            The dimension must be identical to the number of latent variables
            (shared variables are only a single latent variable)
        """
        if self.joint_parameter_list is None:
            self.join()

        self.joint_parameter_list.update(parameter_vector)
        result = []
        for key, me in self.mes.items():
            prm = self.prms[key]
            result.append(me(prm))
        return np.concatenate(result)

    def join(self, shared=None):
        """
        Sets a specific parameter latent such that it is updated
        before evaluating the model error in the __call__ method

        shared:
            dictionary of variables to be shared (only used once in the global problem)

        """
        self.joint_parameter_list = JointParameterList(self.prms, shared)

    def set_latent(self, name, key=None):
        """
        Sets a specific parameter latent such that it is updated
        before evaluating the model error in the __call__ method

        name:
            parameter name that must match one in global parameters

        key:
            The key indicates to which the parameter group the "name" belongs
            to. If key is None, this assumes a _shared_ parameter.
        """
        if self.joint_parameter_list is None:
            raise RuntimeError(
                "Error, you should first join all model errors to a joint list by calling join."
            )
        self.joint_parameter_list.set_latent(name, key)

    def uncorrelated_normal_prior(self, shared=None):
        """
        Joins all individual parameter lists and creates a normal prior for all latent variables

        shared:
            dictionary of variables to be shared (only used once in the global problem)
        """
        self.joint_parameter_list = JointParameterList(self.prms, shared)
        return UncorrelatedNormalPrior(self.joint_parameter_list)