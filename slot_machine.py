# TBD ask it to deposit more money for each new round

import random

class SlotMachine:
    ## Game Constants
    MAX_LINES = 3
    MAX_BET = 100 # bet per line
    MIN_BET = 1 # bet per line
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
        self.lines = 0 # Lines to bet on
        self.bet = 0 # bet per line
        self.slots = [] # the 2D matrix, injected by the spin() method

    ## Input Validation Methods
    def _validate_deposit(self, amount):
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Amount must be a positive integer")

    def _validate_lines(self, lines):
        if not 1 <= lines <= self.MAX_LINES:
            raise ValueError(f"Lines must be between 1-{self.MAX_LINES}")


    def _validate_bet(self, bet):
        if not self.MIN_BET <= bet <= self.MAX_BET:
            raise ValueError(f"Bet must be between ${self.MIN_BET} and ${self.MAX_BET}")
        if bet * self.lines > self.balance:  # Allow bets equal to or less than the balance
            raise ValueError("Total bet exceeds current balance")



    ## Core Game Methods
    def deposit(self, max_attempts=3): # maybe we can use this max attempts only for the testing phase
        attempts = 0
        while attempts < max_attempts:
            try:
                amount = int(input("Deposit amount: $"))
                self._validate_deposit(amount)
                self.balance = amount
                return
            except ValueError as e:
                print(f"Invalid deposit: {e}")
                attempts+=1
        raise ValueError("Too many invalid deposit attempts")   



    def select_lines(self, max_attempts=3):
        attempts = 0
        while attempts < max_attempts:
            try:
                lines = int(input(f"Lines to bet (1-{self.MAX_LINES}): "))
                self._validate_lines(lines)
                self.lines = lines
                return
            except ValueError as e:
                print(f"Invalid input: {e}")
                attempts += 1
        raise ValueError("Too many invalid line selection attempts")




    def place_bet(self):
        if self.balance <= 0:
            raise ValueError("Cannot place a bet with zero or negative balance.")

        while True:
            try:
                bet = int(input("Bet per line: $"))
                self._validate_bet(bet)
                self.bet = bet
                self.balance -= self.bet * self.lines  # Deduct when valid
                # self.balance -= self.total_bet  # Deduct when valid
                return
            except ValueError as e:
                print(f"Invalid bet: {e}")


    ## Game Logic
    @property # this property enabling features such as data validation... (purpose here is be instead of class property that is calculated dependency)
    def total_bet(self):
        return self.bet * self.lines



    def spin(self):
        symbols = [s for s, count in self._symbol_count.items() for _ in range(count)] # ['A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']
        self.slots = []
        
        for _ in range(self.COLS):
            column = []
            current_symbols = symbols.copy() # instead of symbols[:]
            for _ in range(self.ROWS):
                symbol = random.choice(current_symbols)
                current_symbols.remove(symbol)
                column.append(symbol)
            self.slots.append(column)



    def display_result(self):
        print("\nSlot Results:")
        for row in range(len(self.slots[0])):
            print(" | ".join(col[row] for col in self.slots))



    # def calculate_winnings(self):
    #     winnings = 0
    #     winning_lines = []
        
    #     # Iterate over each row (assuming a 3x3 grid)
    #     for i, row_index in enumerate(range(3)):  # Check rows 0, 1, 2  # TBD maybe call row_index -> col_index instead?
    #         # Get symbols from each column in this row
    #         symbols = [
    #             self.slots[0][row_index],  # Column 0, current row
    #             self.slots[1][row_index],  # Column 1, current row
    #             self.slots[2][row_index]   # Column 2, current row
    #         ]
            
    #         # Check if all symbols in this row are identical
    #         if symbols[0] == symbols[1] == symbols[2]:
    #             symbol = symbols[0]
    #             if symbol in self._symbol_value:
    #                 line_winnings = self.bet * self._symbol_value[symbol]
    #                 winnings += line_winnings
    #                 winning_lines.append(i + 1)  # 1-based index
    #                 print(f"DEBUG: Row {i + 1} wins with symbol {symbol}, winnings: {line_winnings}")
        
    #     print(f"DEBUG: Total winnings: {winnings}, Winning rows: {winning_lines}")
    #     self.balance += winnings
    #     return winnings, winning_lines


    def calculate_winnings(self):
        winnings = 0
        winning_lines = []
        
        # Iterate over each row (assuming a 3x3 grid)
        for row_index in range(3):  # Check rows 0, 1, 2  # TBD maybe call row_index -> col_index instead?
            # Get symbols from each column in this row
            symbols = [
                self.slots[0][row_index],  # Column 0, current row
                self.slots[1][row_index],  # Column 1, current row
                self.slots[2][row_index]   # Column 2, current row
            ]
            
            # Check if all symbols in this row are identical
            if symbols[0] == symbols[1] == symbols[2]:
                symbol = symbols[0]
                if symbol in self._symbol_value:
                    line_winnings = self.bet * self._symbol_value[symbol]
                    winnings += line_winnings
                    winning_lines.append(row_index + 1)  # 1-based index
                    print(f"DEBUG: Row {row_index + 1} wins with symbol {symbol}, winnings: {line_winnings}")
        
        print(f"DEBUG: Total winnings: {winnings}, Winning rows: {winning_lines}")
        self.balance += winnings # my new addition (TBD see that without it, the --runxfail is faling)
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
