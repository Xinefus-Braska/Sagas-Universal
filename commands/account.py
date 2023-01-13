from evennia import default_cmds

class CmdLogOut(default_cmds.CmdOOC):

    """
    stop puppeting and go ooc

    Usage:
        <logout> or <relog>

    Go out-of-character (OOC).

    This will leave your current character and put you in a incorporeal OOC state.

    <quit> to disconnect completely while playing.
    """

    key = "logout"
    aliases = "relog"
    locks = "cmd:not is_ooc()"

class CmdPlay(default_cmds.CmdIC):

    """
    control an object you have permission to puppet

    Usage:
      play or login <character>

    Go in-character (IC) as a given Character.

    This will attempt to "become" a different object assuming you have
    the right to do so. Note that it's the ACCOUNT character that puppets
    characters/objects and which needs to have the correct permission!

    You cannot become an object that is already controlled by another
    account. In principle <character> can be any in-game object as long
    as you the account have access right to puppet it.
    """

    key = "play"
    aliases = "login"

class MyAccountCmdSet(default_cmds.AccountCmdSet):
    
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.remove("ic")
        self.remove("ooc")
        self.add(CmdLogOut)
        self.add(CmdPlay)

