import pytest
import io

from slot_machine import SlotMachine


# Test Classes
class TestDepositValidation:
    @pytest.mark.parametrize("inputs, expected", [
        (["0", "100"], 101),  # Invalid then valid
        (["abc", "50"], 50),  # Invalid then valid
        (["-5", "a", "20"], 20),  # Multiple invalid then valid
        (["invalid", "invalid", "invalid"], ValueError)  # All invalid inputs
    ])
    def test_deposit_validation(self, machine, inputs, expected, monkeypatch): # 'machine' from conftest.py
        def mock_input(_):
            return inputs.pop(0) if inputs else "invalid" # extract and provides the 1st item upon each call

        monkeypatch.setattr('builtins.input', mock_input) # part of the PyTest FW
        # 'monkeypatch' allows you to temporarily modify or replace attributes, methods, or functions during a test. (auto-reverted after the test)

        if isinstance(expected, type) and issubclass(expected, Exception): # ensures that expected is a class and not an instance of a class (and this class {ValueError} is a subsype of 'Exception')
            with pytest.raises(expected):
                machine.deposit(max_attempts=3)
        else:
            machine.deposit(max_attempts=3) # machine.deposit method is running the input() upto 3 times
            assert machine.balance == expected


class TestLineSelection:
    @pytest.mark.parametrize("inputs, expected_lines, expected_error", [
        (["0", "2"], 2, None),  # Invalid then valid
        (["4", "3"], 3, None),  # Invalid then valid
        (["abc", "1"], 1, None),  # Invalid then valid
        (["0", "4", "invalid"], None, ValueError)  # All invalid inputs
    ])
    def test_line_validation(self, machine, inputs, expected_lines, expected_error, monkeypatch):
        def mock_input(_):
            return inputs.pop(0) if inputs else "invalid"

        monkeypatch.setattr('builtins.input', mock_input)

        if expected_error:
            with pytest.raises(expected_error):
                machine.select_lines()
        else:
            machine.select_lines()
            assert machine.lines == expected_lines



class TestBettingMechanics:
    @pytest.mark.parametrize("balance, lines, bet, expected_error", [
        (100, 2, 50, None),       # Valid bet
        (100, 2, 0, ValueError),  # Below minimum
        (100, 2, 101, ValueError),# Above maximum
        (50, 2, 26, ValueError),  # Exceeds balance (in 2 lines)
        (100, 3, 33, None),       # Exact balance with valid total bet
        (100, 3, 34, ValueError)  # Exceeds balance (in 3 lines)
    ])
    def test_bet_validation(self, machine, balance, lines, bet, expected_error):
        machine.balance = balance
        machine.lines = lines
        machine.bet = bet

        print(f"DEBUG: balance={machine.balance}, lines={machine.lines}, bet={machine.bet}, total_bet={machine.total_bet}")

        if expected_error:
            with pytest.raises(expected_error):
                machine._validate_bet(bet)
        else:
            machine._validate_bet(bet)
            assert machine.total_bet == bet * lines






import pytest

class TestGameLogic:
    @pytest.mark.parametrize("slots_config, lines, bet, expected_winnings, expected_winning_lines", [
        # Winning configurations
        (
            [['D', 'C', 'B'],  # Row 1: Winning with 'D'
             ['D', 'C', 'B'],  # Row 2: Winning with 'C'
             ['D', 'C', 'B']],  # Row 3: Winning with 'B'            

            3,  # Number of lines
            10,  # Bet per line
            (10 * 2) + (10 * 3) + (10 * 4),  # Winnings: Line 1 ('D'), Line 2 ('C'), Line 3 ('B')
            [1, 2, 3]  # Winning lines
        ),
        (
            [['A', 'B', 'C'],  # Row 1: Winning with 'A'
             ['A', 'B', 'C'],  # Row 2: Winning with 'B'
             ['A', 'B', 'C']],  # Row 3: Winning with 'C'            
            3,
            10,
            (10 * 5) + (10 * 4) + (10 * 3),  # Winnings: Line 1 ('A'), Line 2 ('B'), Line 3 ('C')
            [1, 2, 3]  # Winning lines
        ),

        # --- I was hadding here another winning permutation w/ 2 lines winnig
        (
            [['A', 'B', 'A'],  # Row 1: Winning with 'A'
             ['A', 'B', 'B'],  # Row 2: Winning with 'B'
             ['A', 'B', 'C']],  # Row 3: Winning with 'C'            
            3,
            20,
            (20 * 5) + (20 * 4),  # Winnings: Line 1 ('A'), Line 2 ('B'), Line 3 ('C')
            [1, 2]  # Winning lines
        ),

        # ---

        # Non-winning configurations
        (
            [['A', 'D', 'A'],  # Row 1: No win
             ['B', 'C', 'D'],  # Row 2: No win
             ['C', 'B', 'C']],  # Row 3: No win
            3,
            5,
            0,  # No winnings
            []  # No winning lines
        )
    ])


    def test_win_calculations(self, initialized_machine, slots_config, lines, bet, expected_winnings, expected_winning_lines):
        # Set up the slot machine with the test parameters
        initialized_machine.slots = slots_config
        initialized_machine.lines = lines
        initialized_machine.bet = bet

        # Calculate winnings and winning lines
        winnings, winning_lines = initialized_machine.calculate_winnings()

        # Debug output for verification during testing
        print(f"Slots: {initialized_machine.slots}")
        print(f"Winnings: {winnings}")
        print(f"Winning Lines: {winning_lines}")

        # Assertions to verify correctness of winnings and winning lines
        assert winnings == expected_winnings, f"Expected winnings: {expected_winnings}, got: {winnings}"
        assert winning_lines == expected_winning_lines, f"Expected winning lines: {expected_winning_lines}, got: {winning_lines}"






    def test_symbol_distribution(self, initialized_machine):
        # Run multiple spins to reduce randomness impact
        total_spins = 1000
        all_symbols = []

        for _ in range(total_spins):
            initialized_machine.spin()
            symbols = [symbol for col in initialized_machine.slots for symbol in col]
            all_symbols.extend(symbols)

        counts = {sym: all_symbols.count(sym) for sym in ['A', 'B', 'C', 'D']}

        # Expected proportions based on symbol_count weights
        total_symbols = sum(initialized_machine._symbol_count.values())
        expected_proportions = {
            sym: count / total_symbols
            for sym, count in initialized_machine._symbol_count.items()
        }

        # Verify that actual proportions are close to expected proportions
        actual_proportions = {sym: counts[sym] / len(all_symbols) for sym in counts}
        for sym in expected_proportions:
            assert abs(actual_proportions[sym] - expected_proportions[sym]) < 0.05, (
                f"Symbol {sym} distribution deviates significantly: "
                f"Expected ~{expected_proportions[sym]:.2f}, Got ~{actual_proportions[sym]:.2f}"
            )


    # def test_win_calculations(self, initialized_machine, slots_config, expected_winnings, monkeypatch):
    #     initialized_machine.bet = 2
    #     monkeypatch.setattr(random, 'choice', lambda x: slots_config.pop(0).pop(0))
        
    #     initialized_machine.spin()
    #     winnings, _ = initialized_machine.calculate_winnings()
        
    #     assert winnings == expected_winnings
    #     assert initialized_machine.balance == 1000 - (2 * 2) + winnings

# ---
# @pytest.fixture
# def initialized_machine(machine):
#     machine.balance = 1000
#     machine.lines = 2
#     return machine
# ----

    @pytest.mark.xfail  # it now appeares as 'XPASS' in report after was fixing the issues/bugs
    def test_balance_adjustments(self, initialized_machine):
        # Set initial balance, lines, and bet
        initialized_machine.balance = 900 # TBD now disabled
        # initialized_machine.balance = 1000 # TBD now disabled
        initialized_machine.lines = 2 # TBD now disabled
        initialized_machine.bet = 50 # TBD now disabled

        # Predefine a winning slot configuration (winning on lines 1 and 2)

        initialized_machine.slots = [
            ['A', 'B', 'C'],  # Line 1: Winning with 'A'
            ['A', 'B', 'D'],  # Line 2: Winning with 'B'
            ['A', 'B', 'C']   # No win on line 3
        ]
        # initialized_machine.slots = [
        #     ['A', 'A', 'A'],  # Line 1: Winning with 'A'
        #     ['B', 'B', 'B'],  # Line 2: Winning with 'B'
        #     ['C', 'D', 'C']   # No win on line 3
        # ]

        # Calculate winnings based on predefined slots
        winnings, winning_lines = initialized_machine.calculate_winnings()

        # Verify winnings and balance adjustments
        assert winnings == (initialized_machine.bet * initialized_machine._symbol_value['A'] +
                            initialized_machine.bet * initialized_machine._symbol_value['B'])
        assert winning_lines == [1, 2]  # Winning on lines 1 and 2
        assert initialized_machine.balance == 1000 - (50 * 2) + winnings
        # assert initialized_machine.balance == 1000 - (50 * 2) + winnings

        # print(f"Slots: {initialized_machine.slots}")
        print(f"Winnings: {winnings}")
        print(f"Winning Lines: {winning_lines}")
        print(f"Balance: {initialized_machine.balance}")



class TestEdgeCases:
    def test_zero_balance(self, machine):
        # Set balance to zero
        machine.balance = 0
        
        # Attempt to place a bet and expect ValueError
        with pytest.raises(ValueError, match="Cannot place a bet with zero or negative balance."):
            machine.place_bet()


    def test_max_win_scenario(self, initialized_machine):
        initialized_machine.bet = SlotMachine.MAX_BET # calling  globals without instance...
        initialized_machine.lines = SlotMachine.MAX_LINES
        initialized_machine.spin()
        # Force all lines to win with symbol 'A'
        initialized_machine.slots = [['A']*3 for _ in range(3)]
        winnings, lines = initialized_machine.calculate_winnings()
        
        expected = SlotMachine._symbol_value['A'] * SlotMachine.MAX_BET * SlotMachine.MAX_LINES
        assert winnings == expected
        assert len(lines) == SlotMachine.MAX_LINES