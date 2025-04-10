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
 
	- pytest -v test_slot_machine.py


## Benefits:

	- This test suite provides:

	- 100% method coverage

	- Input validation testing

	- Game logic verification

	- Edge case handling

	- Balance management checks

	- Symbol distribution validation

	- The tests use pytest's powerful features to ensure comprehensive validation while maintaining readability and reducing code duplication through parametrization