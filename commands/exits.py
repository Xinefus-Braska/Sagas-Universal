from evennia.objects.objects import ExitCommand as BaseExitCommand

class CmdExit(BaseExitCommand):
    def at_pre_cmd(self):
        if super().at_pre_cmd():
            # this makes sure to cancel the command if it would've failed for other reasons
            return True
        # this is the part where you check movement status
        # e.g.if the is_sitting attribute is "truthy" i.e. an object, it'll cancel
        if self.caller.db.is_sitting:
            self.caller.msg(f"You need to stand up first")
            return True