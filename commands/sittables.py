from evennia import Command, CmdSet
from evennia import InterruptCommand

class CmdSit(Command):

    """
    Sit down.

    Usage:
        sit <sittable>

    """
    key = "sit"

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.caller.msg("Sit on what?")
            raise InterruptCommand

    def func(self):

        # self.search handles all error messages etc.
        sittable = self.caller.search(self.args)
        if not sittable:
            return
        try:
            sittable.do_sit(self.caller)
        except AttributeError:
            self.caller.msg("You can't sit on that!")

class CmdStand(Command):
    """
    Stand up.

    Usage:
        stand

    """
    key = "stand" 

    def func(self):

        caller = self.caller
        # if we are sitting, this should be set on us
        sittable = caller.db.is_sitting
        if not sittable:
            caller.msg("You are not sitting down.")
        else:
            sittable.do_stand(caller)

class CmdSetSit(CmdSet):
    priority = 1
    def at_cmdset_creation(self):
        self.add(CmdSit)
        self.add(CmdStand)