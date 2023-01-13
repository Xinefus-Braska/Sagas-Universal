# Parent of this new class is objects.Object. So we need to import it
# to inherit everything.
from typeclasses.objects import Object
# New Class called Monster - child of Object
class Monster(Object):
    """
    This is a base class for Monster.
    """
    # When the monster moves around, it will do the below
    def move_around(self):
        print(f"{self.key} is moving!")

# Sub-class Dragon - child of Monster(Object)
class Dragon(Monster):
    """
    This is a dragon monster.
    """
    # When the monster moves around, it will do the below
    def move_around(self):
        # Inherit the def from parent
        super().move_around()
        # Add a new thing.
        print("The world trembles.")
    # For this to happen you need to actually call it in-game
    # with py smaug = me.search("Smaug") ; smaug.firebreath()
    def firebreath(self):
        """
        Let our dragon breathe fire.
        """
        print(f"{self.key} breathes fire!")