# YouTube URL: https://www.youtube.com/watch?v=th4OBktqK1I
# TBD maybe have this functions in a single Class
# TBD maybe adopt the verification methods from the decoration scripts?
# TBD need unit-test (PyTest) on class levent methods having the logic upon balance exceeding
# TBD before massive changes, need to commit the basic working revision and learn deeply about branch naming and tree view
# TBD currently the prmopt says lines (plural) on a single line
# TBD since we're working with int values, we should allow only 1 lines for 1$ deposit and only 2 lines for 2$ deposit (all can be also part of the unit-testing)
# maybe can be enhaced w/ AI


import random

# Const Values
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3


symbol_count = {
	"A": 2, # less chance to get Ace (looks like we'll never get a column/row of 3 'A' ??? )
	"B": 4,
	"C": 6,
	"D": 8, # more change to get 'D'
}

symbol_value = {
	"A": 5, # the rarer symbol is, the higher the myltiply on your money is
	"B": 4,
	"C": 3,
	"D": 2,
}



def check_winnings(columns, lines, bet, symb_val): # bet per line and not the total bet
	winnings = 0
	winning_lines = []
	for line in range(lines):
		symbol = columns[0][line] # all symbols must be same
		for column in columns:  # (for|Else, like we have if|else)
			symbol_to_check = column[line]
			if symbol_to_check != symbol:
				break # break out of the for loop
		else: # else without the if ... (do it only if we didn't break out of the inner for loop ) - TBD without the 'else' it shall be done regardless of the breakout from loop
			winnings += symb_val[symbol] * bet
			winning_lines.append(line+1)

	return winnings, winning_lines





def get_slot_machine_spin(rows, cols, symbols):
	all_symbols = []
	for symbol, count in symbols.items():
		for _ in range(count):
			all_symbols.append(symbol)



	columns = [] # columns = [[], [], []]
	for col in range(cols): # can replace col w/ '_'
		column = []
		current_symbols = all_symbols[:] # [:] to create a copy instead of reference
		for row in range(rows): # can replace row w/ '_'
			value = random.choice(current_symbols)
			current_symbols.remove(value)
			column.append(value)

		columns.append(column)

	return columns



def print_slot_machine(columns):
	for row in range(len(columns[0])):
		for i, column in enumerate(columns):
			if i != len(columns)-1:	# as we don't want the "|" for the last column			
				print(column[row], end=" | ")
			else:
				print(column[row], end="")

		print()



def get_deposit():
	while True:
		amount = input("What would you like to deposit? $ ")
		if amount.isdigit():# to be valid number 
			amount = int(amount)
			if amount > 0: # and positive number
				break # break out of the while loop
			else:
				print("Amount must be greater than 0.")
		else:
			print("Pls. enter a number.")
	return amount


def get_number_of_lines():
	while True:
		lines = input("Enter the number of lines to bet on (1 -" + str(MAX_LINES) + ")? ")
		if lines.isdigit():# to be valid number 
			lines = int(lines)
			if lines >= 1 and lines <=MAX_LINES: # and positive number
			# if MAX_LINES >= lines >= 1: # check that this also works TBD
			# if 1 <= lines <= MAX_LINES: # check that this also works TBD (actual format from vid)
				break
			else:
				print("number of lines must be between 1 and 3")
		else:
			print("Pls. enter a number.")
	return lines


def get_bet():
	while True:
		amount = input("How much would you like to bet on each line? $ ")
		if amount.isdigit():# to be valid number 
			amount = int(amount)
			if MAX_BET >= amount >= MIN_BET : # and positive number
				break
			else:
				print(f"Ammout must be between ${MIN_BET} and ${MAX_BET}.")
		else:
			print("Pls. enter a number.")
	return amount



def main():
	balance = get_deposit()
	lines = get_number_of_lines()
	while True:
		bet = get_bet()
		if bet * lines > balance:
			print(f"Exceeding balance! (Balance = ${balance})")
		else:
			break

	print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: {bet * lines}$ ") # TBD also need to adjust for one line to be non-plural

	slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
	print_slot_machine(slots)
	winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
	print(f"You won ${winnings}.")
	if len(winning_lines) != 0:
		print(f"You won on lines", *winning_lines) # because we return array and we unpack it



main() # funcs are embedded in main() so we could re-run the program after asking: "Do you want to play again?"




