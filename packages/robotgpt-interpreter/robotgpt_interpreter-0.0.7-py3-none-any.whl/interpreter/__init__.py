import sys
from .core.core import Interpreter

sys.modules["interpreter"] = Interpreter()

# ^ This is done so when users `import interpreter`,
# they get an instance.

# **This is a controversial thing to do,**
# because perhaps modules ought to behave like modules.

# But I think it saves a step, removes friction, and looks good.

#    ____      __                            __
#   /  _/___  / /____  _________  ________  / /____  _____
#   / // __ \/ __/ _ \/ ___/ __ \/ ___/ _ \/ __/ _ \/ ___/
# _/ // / / / /_/  __/ /  / /_/ / /  /  __/ /_/  __/ /
#  /___/_/ /_/\__/\___/_/  / .___/_/   \___/\__/\___/_/
#                       /_/
