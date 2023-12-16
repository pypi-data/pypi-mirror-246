import time
import inspect
from typing import List, Callable


class State:
    def __init__(self, id: int) -> None:
        """
        Initialize a State object.
        All routines and transitions must be added manually through the class methods

        Parameters:
        - id (int): The state number. Each state should only have one ID.

        Raises:
        - TypeError: If the provided ID is not of type 'int'.

        Usage:
        - state_instance = State(0)
        """
        # A boolean to track if the state is apart of a state machine yet
        self.__apartOfStateMachine = False

        # A dictionary containing the routines registered to run
        self.__routines = {}

        # A list of all valid states to transition to
        self.__transitions = []

        # The state number, each state should only have one ID
        try:
            # Check if the provided ID is an integer
            self.id = int(id)
            # Add itself as a valid transition to its transition list
            self.set_transition(self.id)
        except (TypeError, ValueError) as e:
            # Raise a TypeError if the ID is not of type 'int' or if it can't be converted
            raise TypeError(
                f"Id should be an integer, but the supplied id is of type {type(id)}"
            ) from e

    def set_routine(self, routineName: str, routine: Callable):
        """
        Set a routine with a given name in the object's routines dictionary.
        The order in which the routines are added determines the order in which they will be executed.
        If a routine name is already present in the states dictionary of routines, the routine will be updated, not added.
        Thus, routine names must be unique within a state object.
        It is required that all routines accept kwargs by default, such that on call the routines can be passed information.

        Parameters:
        - routineName (str): The name of the routine.
        - routine (Callable): The callable object representing the routine.

        Raises:
        - TypeError: If routineName is not of type 'str' or routine is not of type 'Callable'.
        - Exception: If an unexpected exception occurs during the process.
        - Exception: If state is already a part of the state machine, raises an exception.

        Usage:
        - obj.set_routine("my_routine", my_callable_routine)
        """
        if self.__apartOfStateMachine == False:
            try:
                # Check if routineName is a string and routine is a callable object
                if isinstance(routineName, str) and isinstance(routine, Callable):
                    if self.__accepts_kwargs(routine) == True:
                        # Assign the provided routine to the specified routineName in the routines dictionary
                        self.__routines[routineName] = routine
                    else: 
                        raise Exception(f"Supplied routine must accept kwargs as a parameter")
                else:
                    raise TypeError(
                        f"routineName must be of type 'str' and routine must be of type 'Callable', supplied routineName is of type {type(routineName)} and supplied routine is of type {type(routine)}"
                    )
            except (TypeError, ValueError) as e:
                # If an unexpected exception occurs, raise a more informative exception
                raise TypeError(f"Unexpected {type(e)}: {e}")

        else:
            raise Exception(
                f"Once state object is apart of StateMachine object, it may no longer be modified"
            )

    def get_routines(self) -> dict:
        """
        Get the dictionary containing the routines registered in the state.

        Returns:
        - dict: The dictionary of routines.

        Usage:
        - routines_dict = obj.get_routines()
        """
        return self.__routines

    def set_transition(self, transitionId: int):
        """
        Set a transition ID in the object's transitions list.

        Parameters:
        - transitionId (int): The ID of the transition.

        Raises:
        - TypeError: If transitionId is not of type 'int'.
        - Exception: If an unexpected exception occurs during the process.
        - Exception: If state is already apart of state machine, raises exception.

        Usage:
        - obj.set_transition(123)
        """
        if self.__apartOfStateMachine == False:
            try:
                # Append the provided transitionId to the transitions list
                self.__transitions.append(int(transitionId))
            except (TypeError, ValueError) as e:
                # Raise a TypeError if transitionId is not of type 'int'
                raise TypeError(
                    f"Error {type(e)}: transitionId must be of type 'int', supplied transitionId is of type: {type(transitionId)}"
                )
        else:
            raise Exception(
                f"Once state object is apart of StateMachine object, it may no longer be modified"
            )

    def get_transitions(self) -> List[int]:
        """
        Get the list of valid state transitions from the current state.

        Returns:
        - List[int]: The list of transition IDs.

        Usage:
        - transitions_list = obj.get_transitions()
        """
        return self.__transitions

    def __set_apartOfStateMachine(self):
        """
        Set the apartOfStateMachine variable. Do not reccomend users accessing this directly.
        A State may only be added to a State Machine object once

        Raises:
        - Exception: If state is already apart of state machine, raises exception.

        Usage:
        - Designed to be used by the StateMachine object, not by user
        """
        if self.__apartOfStateMachine == False:
            self.__apartOfStateMachine = True
        else:
            raise Exception(
                f"Once state object is apart of StateMachine object, it may no longer be modified"
            )

    def get_apartOfStateMachine(self) -> bool:
        """
        Check if the state is apart of a state machine

        Returns:
        - bool: if the state is apart of a StateMachine object.

        Usage:
        - isApartOfStateMachine = obj.get_state_machine()
        """
        return self.__apartOfStateMachine

    def get_id(self) -> int:
        """
        Get the ID of the state.

        Returns:
        - int: The state ID.

        Usage:
        - state_id = obj.get_id()
        """
        return self.id
    
    def __accepts_kwargs(self, func):
        """
        Check if a function accepts keyword arguments.

        Parameters:
        - func: The function to check.

        Returns:
        - bool: True if the function accepts **kwargs, False otherwise.
        """
        signature = inspect.signature(func)
        for parameter in signature.parameters.values():
            if parameter.kind == inspect.Parameter.VAR_KEYWORD:
                return True
        return False