.main:
	# Start with ans = fact(0) = 1
	push 200
	push 1
	store

	push 0
	push "n = "
.print:
	copy
	jz .read_input
	putchar
	jmp .print
.read_input:
	# Read value of n
	pop
	push 100
	read
	push 0

	# Check for fact(0)
	copy
	push 100
	access
	sub
	jz .fact0
.fact:
	# Increment counter
	push 1
	add

	# Mul current ans by the counter
	copy
	push 200
	access
	mul

	# Print ans
	copy
	puts

	# Store ans
	push 200
	swap
	store

	# Print new line
	push 10
	putchar

	# End loop if counter == n
	copy
	push 100
	access
	sub
	jz .end
	jmp .fact
.fact0:
	push 1
	puts
.end:
	pop
	halt
