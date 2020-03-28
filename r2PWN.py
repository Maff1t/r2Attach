from pwn import *
import os

class R2PWN:
    def __init__ (self, process, r2script=None, terminal=None, template_file='r2template.conf'):
        if isinstance(process, pwnlib.tubes.process.process):
            self.pid = process.pid
            self.debuggee = process.program
        else:
            raise Exception ("Insert a correct process")
        
        # Terminal preferences
        if terminal != None:
            self.terminal = terminal
        else:
            self.terminal = ["tmux", 'splitw', '-h']

        self.script = r2script
        with (template_file, "r") as f:
            self.r2template = f.read()
    def attach(self):
        if self.script != None:
            script_file = os.path.join ("/tmp/", self.debuggee + ".py")
            print script_file
            with open(script_file,"w+") as f:
                f.write(self.r2template.format(mod_name=os.path.basename(self.debuggee), user_commands=self.script))
            command = ["tmux", "splitw", "-h", "r2", "-i", script_file, "-d", str(self.pid)]
        else:
            print self.pid
            command = self.terminal + ['r2', '-d', str(self.pid)]
        
        subprocess.call (command)
        

