# you need to have bc installed in your system!
import commands
from api import *

class Calculator( Plugin_API ):

    def trigger( self ):

        if self.command("math") or self.command("calc") or self.command("c"):

            args    = self.args()
            problem = "".join(args)

            # strip illegal characters for security
            strips   = ["\"", "'", ";", "=", "&", "|"]
            for s in strips:
                problem = problem.replace(s, "")

            problem = problem.replace("\"", "")

            cmd = "echo \"scale=6; " + problem + "\" | bc" # command to calculate
            ans = commands.getoutput(cmd)

            # overflow or something...
            if len(ans) > 32:
                ans = "error"

            elif ans.count("error") > 0:
                ans = "error"

            self.irc.msg( self.reply, "= " + ans )


