my_arr = [
            ['A', 'B', 'C'],  # Line 1: Winning with 'A'
            ['D', 'E', 'F'],  # Line 2: Winning with 'B'
            ['G', 'H', 'I']   # No win on line 3
        ]



for arr in my_arr:
	for i, element in enumerate(arr):
		if i == len(arr)-1:
			print(element)
		else:
			print(element, end = " | ")

# A | B | C
# D | E | F
# G | H | I


print()


# this results in the transposed way
for row in range(len(my_arr[0])):
    print(" | ".join(col[row] for col in my_arr))

# A | D | G
# B | E | H
# C | F | I



symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}




symbols = [s for s, count in symbol_count.items() for _ in range(count)]
# ['A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']