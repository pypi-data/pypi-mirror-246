import time
import inspect
from typing import List, Any
from procaaso_state_machine.procaaso_state import State
from procaaso_state_machine.procaaso_event import Event


class StateMachine:
    """
    A deterministic finite acceptor state machine designed for use within the ProCaaSo framework.

    This machine works in conjunction with the 'State' object from procaaso_state.
    State objects are not modifiable after they are added to the state machine instance.
    The state object should be defined and complete before addition to the StateMachine.
    Recommended practice is to place StateMachine logic with try-except statements to catch any errors.

    """

    def __init__(self) -> None:
        """
        Initialize a StateMachine object.

        Attributes:
        - instruments (dict): Dictionary containing each instrument object added to a machine.
        - __states (dict): A dictionary of state class objects that the state machine will keep track of.
        - __currentStateId (int): Tracks identification for the current state.
        - __currentTransitions (list): A dictionary of lists, where the key is state, each sublist containing the state's possible transitions.
        - __isConfigured (bool): Tracks whether the machine is able to enter its initial state.
        - __stateStartTime (float): Timestamp indicating the start time of the current state.
        - __currentEvent (Event): The current event associated with the state machine.

        Usage:
        - state_machine_instance = StateMachine()
        """
        self.instruments = {}
        self.__states = {}
        self.__currentStateId = None
        self.__currentTransitions = []
        self.__isConfigured = False
        self.__stateStartTime = None
        self.__currentEvent = None

    def run_routine(self, routineName: str = None, **kwargs):
        """
        Run a routine or all routines associated with the current state.
        Amend the 'stateMachine' object into the kwargs of the routines for easy access.
        
        If no routine name is supplied, all routines housed in a state will be executed in the order they are provided.
        If a routine name is specified, it will run that routine only.
        
        If kwargs are provided and a routine name is supplied, the specified routine will receive the kwargs. 
        If kwargs are provided and no routine name is supplied, all routines will receive the same kwargs.
        
        Args:
        - routineName (str, optional): The name of the routine to run. Defaults to None.
        - **kwargs: Additional keyword arguments to pass to the routines.

        Raises:
        - Exception: If there is an issue running the routine(s).

        Usage:
        - state_machine_instance.run_routine()
        - state_machine_instance.run_routine("Main Routine")
        - state_machine_instance.run_routine("Main Routine", returnKwarg="I'm a Keyword Function", anotherVariable="I'm another KWARG")
        """
        try:
            # Run all routines in order
            if routineName == None: 
                states: dict = self.get_states()
                routines = states[self.get_current_state_id()].get_routines()
                if kwargs:
                    for routine in routines.values():
                        kwargs.update({"stateMachine": self})
                        # Check to see if the function takes itself as a parameter
                        if self.__has_self_argument(routine):
                            # Call the function with itself
                            routine(routine, **kwargs)
                        else:
                            # Call routine without itself
                            routine(**kwargs)
                else: 
                    for routine in routines.values():
                        kwargs.update({"stateMachine": self})
                        # Check to see if the function takes itself as a parameter
                        if self.__has_self_argument(routine):
                            # Call the function with itself
                            routine(routine, **kwargs)
                        else:
                            # Call routine without itself
                            routine(**kwargs)

            # Run the specified routine
            else:
                states: dict = self.get_states()
                routines = states[self.get_current_state_id()].get_routines()
                if kwargs:
                    kwargs.update({"stateMachine": self})
                    # Check to see if the function takes itself as a parameter
                    if self.__has_self_argument(routines[routineName]):
                        # Call the function with itself
                        routines[routineName](routines[routineName], **kwargs)
                    else:
                        # Call routine without itself
                        routines[routineName](**kwargs)
                else: 
                    # Check to see if the function takes itself as a parameter
                    if self.__has_self_argument(routines[routineName]):
                        # Call the function with itself
                        routines[routineName](routines[routineName], stateMachine=self)
                    else:
                        # Call routine without itself
                        routines[routineName](stateMachine=self)
        except Exception as e:
            raise Exception(f"Failed to run routine(s) due to: {e}")

    def set_currentEvent(self, event: Event):
        """
        Set the current event object.

        Parameters:
        - event (Event): The event object to set as the current event.

        Raises:
        - Exception: If the provided event is not of type 'Event'.

        Usage:
        - obj.set_currentEvent(my_event)
        """
        if type(event) == Event:
            self.__currentEvent = event
        else:
            raise Exception(f"Event object must be of type 'event', but is of type '{event}'")

    def get_currentEvent(self):
        """
        Retrieve the current event object.

        Raises:
        - Exception: If there is no current event set.

        Returns:
        - Event: The current event object.

        Usage:
        - current_event = obj.get_currentEvent()
        """
        return self.__currentEvent

    def clear_currentEvent(self) -> None: 
        """
        Clear the current event in the StateMachine object.

        Usage:
        - state_machine_instance.clear_current_event()
        """
        self.__currentEvent = None

    def add_state(self, state: State):
        """
        Add a State object to the StateMachine.

        Parameters:
        - state (State): The State object to be added.

        Raises:
        - KeyError: If the state ID is already present in the StateMachine.
        - Exception: If an unexpected exception occurs during the process.

        Usage:
        - state_machine_instance.add_state(my_state_object)
        """
        try:
            if self.__states.get(state.get_id()) is None:
                self.__states[state.get_id()] = state
                # This is a 'managled' name, it allows access to guarded methods,
                # it allows access to the guarded methods of the state machine
                state._State__set_apartOfStateMachine()
            else:
                raise KeyError("State ID already present in State Machine")
        except Exception as e:
            raise Exception(f"Failed to add state due to the following error: {e}")

    def get_states(self):
        """
        Get the dictionary containing the State objects in the StateMachine.

        Returns:
        - dict: The dictionary of State objects.

        Raises:
        - Exception: If an unexpected exception occurs during the process.

        Usage:
        - states_dict = state_machine_instance.get_states()
        """
        try:
            return self.__states
        except Exception as e:
            raise Exception(f"Failed to get state dictionary: {e}")

    def __set_current_state_id(self, newStateId: int):
        """
        Set the ID of the current state.

        Parameters:
        - newStateId (int): The ID of the new state.

        Raises:
        - Exception: If an unexpected exception occurs during the process.

        Usage:
        - state_machine_instance._StateMachine__set_current_state_id(2)
        """
        try:
            self.__currentStateId = newStateId
        except Exception as e:
            raise Exception(
                f"Failed to set __currentStateId due to the following error: {e}"
            )

    def get_current_state_id(self):
        """
        Get the ID of the current state.

        Returns:
        - int: The ID of the current state.

        Raises:
        - Exception: If an unexpected exception occurs during the process.

        Usage:
        - current_state_id = state_machine_instance.get_current_state_id()
        """
        try:
            return self.__currentStateId
        except Exception as e:
            raise Exception(f"Failed to get id of current state: {e}")

    def __set_current_transitions(self, newStateId: int):
        """
        Set the current transitions based on the new state ID.

        Parameters:
        - newStateId (int): The ID of the new state.

        Raises:
        - Exception: If an unexpected exception occurs during the process.

        Usage:
        - state_machine_instance._StateMachine__set_current_transitions(2)
        """
        try:
            self.__currentTransitions = self.__states[newStateId].get_transitions()
        except Exception as e:
            raise Exception(
                f"Failed to set __currentTransitions due to the following error: {e}"
            )

    def get_current_transitions(self):
        """
        Get the list of current transitions.

        Returns:
        - list: The list of current transitions.

        Raises:
        - Exception: If an unexpected exception occurs during the process.

        Usage:
        - current_transitions_list = state_machine_instance.get_current_transitions()
        """
        try:
            return self.__currentTransitions
        except Exception as e:
            raise Exception(
                f"Failed to get __currentTransitions due to the following error: {e}"
            )

    def transition_state(self, newStateId: int):
        """
        Transition to a new state.

        Parameters:
        - newStateId (int): The ID of the new state.

        Raises:
        - Exception: If an unexpected exception occurs during the process.

        Usage:
        - state_machine_instance.transition_state(2)
        """
        try:
            self.__validate_transition(newStateId)
            self.__set_current_state_id(newStateId)
            self.__set_current_transitions(newStateId)
            self.__set_state_start_time()
        except Exception as e:
            raise Exception(
                f"Failed to transition from current state {self.get_current_state_id()} to new state {newStateId}: {e}"
            )

    def __validate_transition(self, newStateId: int):
        """
        Validate if the transition to a new state is allowed.

        Parameters:
        - newStateId (int): The ID of the new state.

        Raises:
        - Exception: If the new state ID is not present in the State object's transition list.
            Or if an unexpected exception occurs during the process.

        Usage:
        - state_machine_instance._StateMachine__validate_transition(2)
        """
        try:
            if newStateId in self.__currentTransitions:
                return
            else:
                raise Exception(
                    f"State ID {newStateId} not present in current State object's transition list"
                )
        except Exception as e:
            raise Exception(f"Failed to validate transition to new state: {e}")

    def start_state_machine(self, initialStateId: int):
        """
        Start the StateMachine.

        Parameters:
        - initialStateId (int): The ID of the initial state.

        Raises:
        - Exception: If the StateMachine is already configured and/or running.

        Usage:
        - state_machine_instance.start_state_machine(1)
        """
        if self.__isConfigured is False:
            self.__set_current_state_id(initialStateId)
            self.__set_current_transitions(initialStateId)
            self.__set_state_start_time()
            self.__set_is_configured(True)
        else:
            raise Exception("State machine is already configured and/or running")

    def __set_is_configured(self, configureValue):
        """
        Set the isConfigured attribute.

        Parameters:
        - configureValue: The value to set for the isConfigured attribute.

        Raises:
        - Exception: If an unexpected exception occurs during the process.

        Usage:
        - state_machine_instance._StateMachine__set_is_configured(True)
        """
        try:
            self.__isConfigured = configureValue
        except Exception as e:
            raise Exception(f"Failed to set __isConfigured: {e}")

    def get_is_configured(self):
        """
        Get the value of the isConfigured attribute.

        Returns:
        - bool: The value of the isConfigured attribute.

        Raises:
        - Exception: If an unexpected exception occurs during the process.

        Usage:
        - is_configured_value = state_machine_instance.get_is_configured()
        """
        try:
            return self.__isConfigured
        except Exception as e:
            raise Exception(f"Failed to get isConfigured: {e}")

    def add_instrument(self, instruments: dict[str, Any]):
        """
        Add instruments to the StateMachine.

        Parameters:
        - instruments (dict): An open-ended function so the user can define the data structure they wish to use for their instruments.
                            If the instrument dictionary is already present in the StateMachine dictionary, it will simply update the first entry.

        Raises:
        - TypeError: If the provided instruments are not of type 'dict'.
        - Exception: If an unexpected exception occurs during the process.

        Usage:
        - state_machine_instance.add_instrument({"instrument1": data1, "instrument2": data2})
        """
        try:
            if type(instruments) is dict:
                self.instruments.update(instruments)
            else:
                raise TypeError(
                    f"Expected type of dict, but got type of {type(instruments)}"
                )
        except [Exception, TypeError] as e:
            raise TypeError(f"Failed to add instrument due to the following error: {e}")

    def get_instruments(self):
        """
        Get the instruments dictionary from the StateMachine.

        Returns:
        - dict: The dictionary containing instruments.

        Raises:
        - Exception: If an unexpected exception occurs during the process.

        Usage:
        - instruments_dict = state_machine_instance.get_instruments()
        """
        try:
            return self.instruments
        except Exception as e:
            raise Exception(f"Failed to get_instruments: {e}")

    def __set_state_start_time(self):
        """
        Set the start time for the state.

        Raises:
        - Exception: If setting the start time fails.

        Usage:
        - self.__set_state_start_time()
        """
        try:
            self.__stateStartTime = time.time()
        except Exception as e:
            raise Exception(f"Failed to set state start time: {e}")

    def get_state_start_time(self):
        """
        Get the start time of the state.

        Raises:
        - Exception: If retrieving the start time fails.

        Returns:
        - float: The start time of the state.

        Usage:
        - start_time = self.get_state_start_time()
        """
        try:
            return self.__stateStartTime
        except Exception as e:
            raise Exception(f"Failed to retrieve the start time: {e}")

    def get_time_elapsed_in_state(self):
        """
        Get the elapsed time since the state started.

        Raises:
        - Exception: If retrieving the elapsed time fails.

        Returns:
        - float: The elapsed time since the state started.

        Usage:
        - elapsed_time = self.get_time_elapsed_in_state()
        """
        try:
            return time.time() - self.__stateStartTime
        except Exception as e:
            raise Exception(f"Failed to retrieve the time elapsed: {e}")
        
    def __has_self_argument(slef, func):
        """
        Check if a function has "self" as a positional argument.

        Parameters:
        - func: The function to check.

        Returns:
        - bool: True if "self" is a positional argument, False otherwise.
        """
        signature = inspect.signature(func)
        parameters = signature.parameters

        # Check if "self" is a positional argument
        return 'self' in parameters and parameters['self'].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD

