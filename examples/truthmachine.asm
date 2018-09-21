.main:
	push 63
	putchar
	push 100
	readchar
	push 100
	access
.loop:
	copy
	push 48
	sub
	jnz .loop
	halt
