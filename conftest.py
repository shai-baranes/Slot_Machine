import pytest
from slot_machine import SlotMachine
import random # TBD needed?

# Fixtures
@pytest.fixture
def machine():
    return SlotMachine()

@pytest.fixture
def initialized_machine(machine):
    machine.balance = 1000
    machine.lines = 2
    return machine