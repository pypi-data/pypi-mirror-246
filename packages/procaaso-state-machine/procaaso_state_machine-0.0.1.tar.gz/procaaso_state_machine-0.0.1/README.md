# procaaso-state-machine
The ProCaaSo based state machine is an ENS centric implementaion of a finite state machine. It's goal is to provide users a state machine that works well within the ProCaaSo App loop, its handlers, classes, methods and other such details will be outlined below. 


# StateMachine Class

The `StateMachine` class is a deterministic finite acceptor state machine designed for use within the ProCaaSo framework. It works in conjunction with the `State` object from the `procaaso_state` module. State objects should be defined and complete before addition to the `StateMachine`. It is recommended to handle `StateMachine` logic with try-except statements to catch any errors.

## Initialization

```python
from procaaso_state_machine.procaaso_state import State

state_machine_instance = StateMachine()
```

## Attributes

- `instruments` (dict): A dictionary containing each instrument object added to the machine.
- `__states` (dict): A dictionary of `State` objects that the state machine keeps track of.
- `__currentStateId` (int): Tracks identification for the current state.
- `__currentTransitions` (list): A list of current transitions based on the current state.
- `__isConfigured` (bool): Tracks whether the machine is able to enter its initial state.

## Methods

### `add_state(state: State)`

Add a `State` object to the `StateMachine`.

```python
state_machine_instance.add_state(my_state_object)
```

Raises:
- `KeyError`: If the state ID is already present in the `StateMachine`.
- `Exception`: If an unexpected exception occurs during the process.

### `get_states() -> dict`

Get the dictionary containing the `State` objects in the `StateMachine`.

```python
states_dict = state_machine_instance.get_states()
```

Raises:
- `Exception`: If an unexpected exception occurs during the process.

### `get_current_state_id() -> int`

Get the ID of the current state.

```python
current_state_id = state_machine_instance.get_current_state_id()
```

Raises:
- `Exception`: If an unexpected exception occurs during the process.

### `get_current_transitions() -> list`

Get the list of current transitions.

```python
current_transitions_list = state_machine_instance.get_current_transitions()
```

Raises:
- `Exception`: If an unexpected exception occurs during the process.

### `transition_state(newStateId: int)`

Transition to a new state.

```python
state_machine_instance.transition_state(2)
```

Raises:
- `Exception`: If an unexpected exception occurs during the process.

### `start_state_machine(initialStateId: int)`

Start the `StateMachine`.

```python
state_machine_instance.start_state_machine(1)
```

Raises:
- `Exception`: If the `StateMachine` is already configured and/or running.

### `add_instrument(instruments: dict)`

Add instruments to the `StateMachine`.

```python
state_machine_instance.add_instrument({"instrument1": data1, "instrument2": data2})
```

Raises:
- `TypeError`: If the provided instruments are not of type 'dict'.
- `Exception`: If an unexpected exception occurs during the process.

### `get_instruments() -> dict`

Get the instruments dictionary from the `StateMachine`.

```python
instruments_dict = state_machine_instance.get_instruments()
```

Raises:
- `Exception`: If an unexpected exception occurs during the process.

### `get_state_start_time() -> float`

Get the start time of the state.

```python
start_time = state_machine_instance.get_state_start_time()
```

Raises:
- `Exception`: If retrieving the start time fails.

### `get_time_elapsed_in_state() -> float`

Get the elapsed time since the state started.

```python
elapsed_time = state_machine_instance.get_time_elapsed_in_state()
```

Raises:
- `Exception`: If retrieving the elapsed time fails.

# State Class

The `State` class represents a state object within the ProCaaSo framework. Each state must have a unique ID, and routines and transitions are added manually through the class methods.

## Initialization

```python
from typing import Callable
from procaaso_state import State

state_instance = State(0)
```

### Attributes

- `__apartOfStateMachine` (bool): A boolean to track if the state is part of a state machine.
- `__routines` (dict): A dictionary containing the routines registered to run.
- `__transitions` (list): A list of all valid states to transition to.
- `id` (int): The state number, each state should only have one ID.

## Methods

### `set_routine(routineName: str, routine: Callable)`

Set a routine with a given name in the object's routines dictionary.

```python
state_instance.set_routine("my_routine", my_callable_routine)
```

Raises:
- `TypeError`: If routineName is not of type 'str' or routine is not of type 'Callable'.
- `Exception`: If an unexpected exception occurs during the process.
- `Exception`: If the state is already part of a state machine.

### `get_routines() -> dict`

Get the dictionary containing the routines registered in the state.

```python
routines_dict = state_instance.get_routines()
```

### `set_transition(transitionId: int)`

Set a transition ID in the object's transitions list.

```python
state_instance.set_transition(123)
```

Raises:
- `TypeError`: If transitionId is not of type 'int'.
- `Exception`: If an unexpected exception occurs during the process.
- `Exception`: If the state is already part of a state machine.

### `get_transitions() -> List[int]`

Get the list of valid state transitions from the current state.

```python
transitions_list = state_instance.get_transitions()
```

### `set_state_machine()`

Set the `__apart_of_state_machine` variable. Do not recommend users accessing this directly. A State may only be added to a State Machine object once.

Raises:
- `Exception`: If the state is already part of a state machine.

### `get_state_machine() -> bool`

Get the `__apart_of_state_machine` of the state object.

```python
isApartOfStateMachine = state_instance.get_state_machine()
```

### `get_id() -> int`

Get the ID of the state.

```python
state_id = state_instance.get_id()
```

**Note**: Methods prefixed with double underscores (e.g., `__set_routine`, `__set_current_state_id`) are intended for internal use and should not be accessed directly by users.