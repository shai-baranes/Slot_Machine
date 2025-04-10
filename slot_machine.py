# TBD ask it to deposit more money for each new round

import random

class SlotMachine:
    ## Game Constants
    MAX_LINES = 3
    MAX_BET = 100
    MIN_BET = 1
    ROWS = 3
    COLS = 3
    
    _symbol_count = {
        "A": 2,
        "B": 4,
        "C": 6,
        "D": 8
    }
    
    _symbol_value = {
        "A": 5,
        "B": 4,
        "C": 3,
        "D": 2
    }

    def __init__(self):
        self.balance = 0
        self.lines = 0
        self.bet = 0
        self.slots = []

    ## Input Validation Methods
    def _validate_deposit(self, amount):
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Amount must be a positive integer")

    def _validate_lines(self, lines):
        if not 1 <= lines <= self.MAX_LINES:
            raise ValueError(f"Lines must be between 1-{self.MAX_LINES}")

    def _validate_bet(self, bet):
        if not self.MIN_BET <= bet <= self.MAX_BET:
            raise ValueError(f"Bet must be ${self.MIN_BET}-${self.MAX_BET}")
        if bet * self.lines > self.balance:
            raise ValueError("Exceeds current balance")

    ## Core Game Methods
    def deposit(self):
        while True:
            try:
                amount = int(input("Deposit amount: $"))
                self._validate_deposit(amount)
                self.balance = amount
                return
            except ValueError as e:
                print(f"Invalid deposit: {e}")

    def select_lines(self):
        while True:
            try:
                lines = int(input(f"Lines to bet (1-{self.MAX_LINES}): "))
                self._validate_lines(lines)
                self.lines = lines
                return
            except ValueError as e:
                print(f"Invalid lines: {e}")

    def place_bet(self):
        while True:
            try:
                bet = int(input("Bet per line: $"))
                self._validate_bet(bet)
                self.bet = bet
                self.balance -= self.total_bet  # Deduct when valid
                return
            except ValueError as e:
                print(f"Invalid bet: {e}")

    ## Game Logic
    @property
    def total_bet(self):
        return self.bet * self.lines

    def spin(self):
        symbols = [s for s, count in self._symbol_count.items() for _ in range(count)]
        self.slots = []
        
        for _ in range(self.COLS):
            column = []
            current_symbols = symbols.copy()
            for _ in range(self.ROWS):
                symbol = random.choice(current_symbols)
                current_symbols.remove(symbol)
                column.append(symbol)
            self.slots.append(column)

    def display_result(self):
        print("\nSlot Results:")
        for row in range(len(self.slots[0])):
            print(" | ".join(col[row] for col in self.slots))

    def calculate_winnings(self):
        winnings = 0
        winning_lines = []
        
        for line in range(self.lines):
            first_symbol = self.slots[0][line]
            if all(col[line] == first_symbol for col in self.slots):
                multiplier = self._symbol_value[first_symbol]
                winnings += multiplier * self.bet
                winning_lines.append(line + 1)
        
        self.balance += winnings  # Add winnings to balance
        return winnings, winning_lines

## Game Flow
def play_game():
    machine = SlotMachine()
    machine.deposit()
    
    while True:
        machine.select_lines()
        machine.place_bet()
        machine.spin()
        machine.display_result()
        
        winnings, lines = machine.calculate_winnings()
        if winnings > 0:
            print(f"🎉 Won ${winnings} on lines: {', '.join(map(str, lines))}!")
        else:
            print("💸 No wins this round")
        
        print(f"Current balance: ${machine.balance}")
        
        if machine.balance <= 0:
            print("Game over - out of funds!")
            return
            
        if input("Play again? (y/n): ").lower() != 'y':
            print(f"💰 Final balance: ${machine.balance}")
            return

if __name__ == "__main__":
    play_game()
