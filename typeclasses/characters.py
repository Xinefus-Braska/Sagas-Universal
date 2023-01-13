"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent
import random 


class Character(ObjectParent, DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_post_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    # When we create the character, it will randomly give STR, DEX, and INT
    # between 3-18.
    def at_object_creation(self):       
        self.db.strength = random.randint(3, 18)
        self.db.dexterity = random.randint(3, 18)
        self.db.intelligence = random.randint(3, 18)

    # function to check stats... 
    def get_stats(self):
        """
        Get the main stats of characters
        """
        # This returns in the form of a tuple: ( a, b, c, ...)
        return self.db.strength, self.db.dexterity, self.db.intelligence

    def at_pre_move(self, destination, **kwargs):
       """
       Called by self.move_to when trying to move somewhere. If this returns
       False, the move is immediately cancelled.
       """
       if self.db.is_sitting:
           self.msg("You need to stand up first.")
           return False
       return True

    pass
