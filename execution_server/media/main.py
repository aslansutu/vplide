
# ██╗░░░██╗██████╗░██╗░░░░░██╗██████╗░███████╗
# ██║░░░██║██╔══██╗██║░░░░░██║██╔══██╗██╔════╝
# ╚██╗░██╔╝██████╔╝██║░░░░░██║██║░░██║█████╗░░
# ░╚████╔╝░██╔═══╝░██║░░░░░██║██║░░██║██╔══╝░░
# ░░╚██╔╝░░██║░░░░░███████╗██║██████╔╝███████╗
# ░░░╚═╝░░░╚═╝░░░░░╚══════╝╚═╝╚═════╝░╚══════╝


def fibonacci_sequence(n):
    sequence = [0, 1]  # Initialize the sequence with the first two numbers

    while len(sequence) < n:
        next_num = sequence[-1] + sequence[-2]  # Calculate the next number
        sequence.append(next_num)  # Add the next number to the sequence

    return sequence




# Example usage:
n = 14
fib_sequence = fibonacci_sequence(n)
print(fib_sequence)


def main():
	print('<-- Hello World! -->')
	return 0

if __name__=="__main__":
	main()

