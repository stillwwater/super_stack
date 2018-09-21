.main:
	push 0
	push "Hello World!"
.print:
	copy
	jz .end
	putchar
	jmp .print
.end:
	pop
	halt
