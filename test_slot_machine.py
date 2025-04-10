import pytest

# Test Classes
class TestDepositValidation:
    @pytest.mark.parametrize("input_val, expected", [
        (100, 100), 
        ("500", 500),
        (0, ValueError),
        (-50, ValueError),
        ("abc", ValueError)
    ])
    def test_deposit_validation(self, machine, input_val, expected, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: str(input_val))
        if isinstance(expected, type) and issubclass(expected, Exception):
            with pytest.raises(expected):
                machine.deposit()
        else:
            machine.deposit()
            assert machine.balance == expected

class TestLineSelection:
    @pytest.mark.parametrize("lines, expected_error", [
        (0, ValueError),
        (4, ValueError),
        ("2", None),
        (3, None),
        ("abc", ValueError)
    ])
    def test_line_validation(self, machine, lines, expected_error, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: str(lines))
        if expected_error:
            with pytest.raises(expected_error):
                machine.select_lines()
        else:
            machine.select_lines()
            assert machine.lines == int(lines)

class TestBettingMechanics:
    @pytest.mark.parametrize("balance, lines, bet, expected_error", [
        (100, 2, 50, None),       # Valid bet
        (100, 2, 0, ValueError),  # Below minimum
        (100, 2, 101, ValueError),# Above maximum
        (50, 2, 26, ValueError),  # Exceeds balance
        (100, 3, 34, None)        # Exact balance
    ])
    def test_bet_validation(self, machine, balance, lines, bet, expected_error):
        machine.balance = balance
        machine.lines = lines
        machine.bet = 0  # Reset previous bet
        
        if expected_error:
            with pytest.raises(expected_error):
                machine._validate_bet(bet)
        else:
            machine._validate_bet(bet)
            assert machine.total_bet == bet * lines

class TestGameLogic:
    def test_symbol_distribution(self, initialized_machine):
        initialized_machine.spin()
        symbols = [symbol for col in initialized_machine.slots for symbol in col]
        counts = {sym: symbols.count(sym) for sym in ['A', 'B', 'C', 'D']}
        
        assert counts['A'] == 2
        assert counts['B'] == 4
        assert counts['C'] == 6
        assert counts['D'] == 8

    @pytest.mark.parametrize("slots_config, expected_winnings", [
        # Winning configurations
        ([[['A', 'A', 'A'], ['B', 'B', 'B'], ['C', 'C', 'C']]], 10),  # 2 lines of A
        ([[['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']]], 16),  # All lines B
        # Non-winning configurations
        ([[['A', 'B', 'C'], ['D', 'D', 'D'], ['A', 'B', 'C']]], 4),   # One line D
        ([[['A', 'B', 'C'], ['D', 'C', 'B'], ['A', 'D', 'C']]], 0)    # No wins
    ])
    def test_win_calculations(self, initialized_machine, slots_config, expected_winnings, monkeypatch):
        initialized_machine.bet = 2
        monkeypatch.setattr(random, 'choice', lambda x: slots_config.pop(0).pop(0))
        
        initialized_machine.spin()
        winnings, _ = initialized_machine.calculate_winnings()
        
        assert winnings == expected_winnings
        assert initialized_machine.balance == 1000 - (2 * 2) + winnings

    def test_balance_adjustments(self, initialized_machine):
        initialized_machine.place_bet()  # Default bet setup
        initial_balance = initialized_machine.balance
        initialized_machine.spin()
        winnings, _ = initialized_machine.calculate_winnings()
        
        assert initialized_machine.balance == initial_balance + winnings

class TestEdgeCases:
    def test_zero_balance(self, machine):
        machine.balance = 0
        with pytest.raises(ValueError):
            machine.place_bet()

    def test_max_win_scenario(self, initialized_machine):
        initialized_machine.bet = SlotMachine.MAX_BET
        initialized_machine.lines = SlotMachine.MAX_LINES
        initialized_machine.spin()
        # Force all lines to win with symbol 'A'
        initialized_machine.slots = [['A']*3 for _ in range(3)]
        winnings, lines = initialized_machine.calculate_winnings()
        
        expected = SlotMachine._symbol_value['A'] * SlotMachine.MAX_BET * SlotMachine.MAX_LINES
        assert winnings == expected
        assert len(lines) == SlotMachine.MAX_LINES