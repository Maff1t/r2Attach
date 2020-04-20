from r2Attach import *
from pwn import *

p = process ('./example_bin')
'''
r2script = """
r2.cmd('db sym.imp.puts')
r2.cmd ('dc')
"""
'''
r2script=None
# your exploit
print (p.clean())

r2pwn = r2Attach(p)
r2pwn.attach(r2script)

p.sendline ("5")
print (p.clean())
p.sendline ("A"*10 + "MYSUPEREXPLOIT")
print (p.clean())

p.interactive()
