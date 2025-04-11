# Slot_Machine

> URL: https://www.youtube.com/watch?v=th4OBktqK1I
> by: Tech With Tim
-----------------------------------------------------------------
> note that the first commit with working project had an empty requirements list (no virtual env needed...)
-----------------------------------------------------------------


## AI prompt (Perplexity):
> Hi, the following code implements a slot machine gambling game. can you take this code and apply it using class while the class incorporates the input validation upon initiation or method calls?
> the code:  (TBD get the code from main prior to branch)> 

## PyTest followup prompt:
> using pytest and its functions, such as fixtures parametrize raises and mark, wherever necessary, and test this code.



## added notes by Perplexity:

> Key features used:
> 
	- Fixtures: machine and initialized_machine for test setup

	- Parametrization: Multiple @pytest.mark.parametrize decorators for testing different input combinations

	- Exception Testing: pytest.raises for validating error conditions

	- Monkeypatching: Modifying random choice for controlled slot outcomes

	- Test Classes: Logical grouping of related test cases
 

## Run PyTest:
> To run the tests (bash):
 
	-> pytest -v test_slot_machine.py


## Benefits:

	- This test suite provides:

	- 100% method coverage

	- Input validation testing

	- Game logic verification

	- Edge case handling

	- Balance management checks

	- Symbol distribution validation

	- The tests use pytest's powerful features to ensure comprehensive validation while maintaining readability and reducing code duplication through parametrization



## additional clarifcations by Perplexity:

### 1)
> **if isinstance(ValueError, type) and issubclass(expected, Exception)**:

> is typically used to check whether the variable expected represents an exception class (not an instance of an exception, but the class itself).
> that is also a subclasses of the base Exception class.

### 2)
> the purpose of **monkeypatch.setattr('builtins.input', mock_input)**
 
> is used in Python testing with the pytest framework to mock the behavior of the built-in input() function during a test. Let’s break it down step by step:

> 1. What Does monkeypatch.setattr Do?
> The monkeypatch fixture provided by pytest allows you to temporarily modify or replace attributes, methods, or functions during a test. The changes are > automatically reverted after the test completes, ensuring that the global state is not permanently altered.
> 
> setattr(target, name, value) replaces the attribute name of the object specified by target with the value value.
> 
> 2. Target: 'builtins.input'
> The target 'builtins.input' refers to Python's built-in input() function, which is used to receive user input from the console.
> 
> By specifying 'builtins.input', you are telling monkeypatch to replace the global input() function with a mock implementation for the duration of the test.
> 
> 3. Replacement: mock_input
> The value passed as the replacement (mock_input) is typically a mock function or object that simulates user input. This allows you to control what input() > will return during the test without requiring actual user interaction.

