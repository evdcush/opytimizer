"""Optimizer.
"""

import copy

import opytimizer.utils.exception as e
import opytimizer.utils.logging as l

logger = l.get_logger(__name__)


class Optimizer:
    """An Optimizer class that holds meta-heuristics-related properties
    and methods.

    """

    def __init__(self):
        """Initialization method.

        """

        # Algorithm's name
        self.algorithm = self.__class__.__name__

        # Key-value parameters
        self.params = {}

        # Key-value arguments
        self.args = {}

        # Key-value additional variables
        self.add_vars = {}

        # Indicates whether the optimizer is built or not
        self.built = False

    @property
    def algorithm(self):
        """str: Algorithm's name.

        """

        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm):
        if not isinstance(algorithm, str):
            raise e.TypeError('`algorithm` should be a string')

        self._algorithm = algorithm

    @property
    def built(self):
        """bool: Indicates whether the optimizer is built.

        """

        return self._built

    @built.setter
    def built(self, built):
        if not isinstance(built, bool):
            raise e.TypeError('`built` should be a boolean')

        self._built = built

    @property
    def params(self):
        """dict: Key-value parameters.

        """

        return self._params

    @params.setter
    def params(self, params):
        if not isinstance(params, dict):
            raise e.TypeError('`params` should be a dictionary')

        self._params = params

    @property
    def args(self):
        """dict: Key-value arguments.

        """

        return self._args

    @args.setter
    def args(self, args):
        if not isinstance(args, dict):
            raise e.TypeError('`args` should be a dictionary')

        self._args = args

    @property
    def add_vars(self):
        """dict: Key-value additional variables.

        """

        return self._add_vars

    @add_vars.setter
    def add_vars(self, add_vars):
        if not isinstance(add_vars, dict):
            raise e.TypeError('`add_vars` should be a dictionary')

        self._add_vars = add_vars

    def build(self, params, args, add_vars=None):
        """Builds the object by creating its parameters.

        Args:
            params (dict): Key-value parameters to the meta-heuristic.
            args (dict): Key-value arguments to the meta-heuristic.
            add_vars (dict): Key-value additional variables to the meta-heurisitc.

        """

        # Checks if `params` are really provided
        if params:
            # Saves the `params` for faster looking up
            self.params = params
        
            # Iterates through all parameters
            for k, v in params.items():
                # Sets its key-value pair
                setattr(self, k, v)

        # Registers the arguments
        self.args = args

        # Register the additional variables
        if add_vars:
            self.add_vars = add_vars

        # Sets the `built` variable to true
        self.built = True

        # Logs the properties
        logger.debug('Algorithm: %s | Custom Parameters: %s | Built: %s.',
                     self.algorithm, str(params), self.built)

    def evaluate(self, space, function):
        """Evaluates the search space according to the objective function.

        If you need a specific evaluate method, please re-implement it on child's class.

        Args:
            space (Space): A Space object that will be evaluated.
            function (Function): A Function object serving as an objective function.

        """

        # Iterates through all agents
        for agent in space.agents:
            # Calculates the fitness value of current agent
            agent.fit = function(agent.position)

            # If agent's fitness is better than global fitness
            if agent.fit < space.best_agent.fit:
                # Makes a deep copy of agent's position and fitness
                space.best_agent.position = copy.deepcopy(agent.position)
                space.best_agent.fit = copy.deepcopy(agent.fit)

    def update(self):
        """Updates the agents' position array.

        As each child has a different procedure of update,
        you will need to implement it directly on its class.

        Raises:
            NotImplementedError.

        """

        pass
