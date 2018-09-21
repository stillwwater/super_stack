.main:
	push 100
.loop:
	; Print number of bottles
	copy
	puts

	push 0
	push " bottles of beer on the wall,"
	call .print

	copy
	puts
	push 0
	push 10
	push " bottles of beer"
	call .print

	; Subtract 1 bottle
	copy
	push 1
	swap
	sub

	push 0
	push "Take one down and pass it around"
	call .print

	copy
	puts
	push 0
	push 10
	copy
	push " bottles of beer on the wall."
	call .print

	; Check for end of loop
	copy
	jz .end
	jmp .loop
.print:
	copy
	putchar
	jnz .print
	ret
.end:
	pop
	halt
