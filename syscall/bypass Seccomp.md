# 通过切换模式来绕过PWN题中对系统调用的拦截

## 简介
CTF比赛中有时会出现一些使用prctl函数或者seccomp安全机制来禁止部分系统调用的pwn题，如果只是禁用了execve，那么还能使用open、read、write系统调用来读flag，如果禁止了open，那么就既不能用execve调用也没法直接打开flag文件来读。这些安全机制都是通过拦截指定的系统调用号来实现安全保护的的目，所以如果我们能够改变想要执行的系统调用的调用号，就能够绕过这些保护。常见的方法是使用retf指令修改cs寄存器来切换程序所处的模式(64 or 32)，因为64位模式和32位模式下相同系统调用的调用号是不同的，所以能够绕过基于拦截系统调用号的安全保护。

## retf指令
retf指令是一条远转移指令，等价于pop cs; pop ip，这条指令一般来说可以在libc中找到，但为什么它能修改程序的模式呢，实际上是因为它修改了cs段寄存器。

## cs寄存器
cs寄存器即code segment寄存器，指向存放代码的内存段，在8086的实模式下，指令的寻址为cs:ip->cs *16 + ip。在32位保护模式下，cpu地址总线和通用寄存器都达到了32位，可以直接访问4GB的内存，段寄存器被赋予了新的任务：保存段描述符的索引即段选择符(segment descriptor)，下图是它的结构：
```plain
					+--------------------------------------+
					|         index                 |T|    |
					|                               |I|RPL |
					+--------------------------------^--^--+
					                                 |  |
					   Table indicator+--------------+  |
					     0 GDT                          |
					     1 LDT                          |
					  Request Privilege Level+----------+					
```
段选择符的低两位用来表示特权级0-3，第3位表示对应的描述符是位于GDT or LDT，高15位则是下标。在段描述符里，保存有更多的该段的参数信息，包括段基址、粒度、属性、模式等等，具体请查询intel手册。64位模式与32位模式类似。

### 模式切换
以64为模式切换到32位模式为例，为了实现模式的切换，我们需要找到一个合适的段选择符，它指向GDT中的一个32位的段描述符。通过google可以知道，在linux x86_x64中，0x23是一个32位的代码段选择符（位于GDT），0x33是一个64位长模式的代码段选择符。所以在模式切换时，只需用retf指令将cs寄存器的值由0x33改为0x23即可。另外需要注意的是，由于程序从64位切换到了32位，所以各个通用寄存器的使用发生了变化，从原来的8字节变成了只使用低4字节，特别对于栈寄存器esp来说，它是rsp的低4字节，原先的rsp保存着可以被正常访问的栈地址，但这个地址的低4字节大概率为一个不可访问的地址，所以在执行retf之前，还需要进行栈迁移，只要通过rop控制rbp后进行两次连续的leave指令就可以实现。

在Linux中，除了FS、GS需要设置段基址用于访问TLS之外，其余的段寄存器对应的段描述符中的段基址都被置为了0，也就是直接使用偏移作为内存访问的绝对地址，所以只要控制好指令指针寄存器，模式切换时就不会出现控制流的失控。

### references:
https://stackoverflow.com/questions/24113729/switch-from-32bit-mode-to-64-bit-long-mode-on-64bit-linux/32384358#32384358

https://www.intel.cn/content/www/cn/zh/architecture-and-technology/64-ia-32-architectures-software-developer-manual-325462.html

https://github.com/david942j/seccomp-tools
