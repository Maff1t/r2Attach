from pwn import *
import os

class r2Attach:
    def __init__ (self, process, terminal=None):
        if isinstance(process, pwnlib.tubes.process.process):
            self.pid = process.pid
            self.debuggee = process.program
        else:
            raise Exception ("Insert a correct pwntools process object")
        
        # Terminal preferences
        if terminal != None:
            self.terminal = terminal
        else:
            self.terminal = ["tmux", 'splitw', '-h']

        self.r2template ="""#!/usr/bin/env python
import os, r2pipe
r2 = r2pipe.open()

def load_modules():
    modules = r2.cmdj("dmmj")
    for module in modules:
        if '{mod_name:s}' == os.path.basename(module['file']):
            command = "oba {{addr:d}} {{file_name:s}}".format(file_name=module['file'], addr=module['address'])
            r2.cmd(command)

load_modules()
r2.cmd('ib') # Reload the buffer info

{user_commands:s}"""
    def attach(self, r2script=None):
        if r2script != None:
            script_file = os.path.join ("/tmp/", self.debuggee + ".py")
            with open(script_file,"w+") as f:
                f.write(self.r2template.format(mod_name=os.path.basename(self.debuggee), user_commands=r2script))
            command = self.terminal + ['r2', "-i", script_file, "-d", str(self.pid)]
        else:
            command = self.terminal + ['r2', '-d', str(self.pid)]
        
        subprocess.call (command)
        

