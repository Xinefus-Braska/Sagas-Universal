"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent
from evennia.utils import lazy_property
from evennia.contrib.rpg.traits import TraitHandler

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
    """
    This is also the generic Playable character class. Everyone that creates a 
    player will have these attributes.
    """
    
    @lazy_property
    def traits(self):
        # this adds the handler as .traits
        return TraitHandler(self, db_attribute_key="traits")
    
    @lazy_property
    def stats(self):
        # this adds the handler as .stats
        return TraitHandler(self, db_attribute_key="stats")

    @lazy_property
    def skills(self):
        # this adds the handler as .skills
        return TraitHandler(self, db_attribute_key="skills")

    def at_object_creation(self):

        self.traits.add( "hp", "Health", trait_type="counter", base=0, mod=0 )
        self.traits.add( "hp_base", "HealthBase", trait_type="static", base=100, mod=0 )
        self.traits.add( "lf_base", "LifeforceBase", trait_type="static", base=1000, mod=0 )
        self.traits.add( "lf", "Lifeforce", trait_type="counter", base=0, max=1000000000000, mod=0 )
        self.stats.add( "str", "Strength", trait_type="static", base=10, max=100, mod=0 )
        self.stats.add( "str_base", "StrengthBase", trait_type="static", base=10, max=100, mod=0 )
        self.stats.add( "dex", "Dexterity", trait_type="static", base=10, max=100, mod=0 )
        self.stats.add( "dex_base", "DexterityBase", trait_type="static", base=10, max=100, mod=0 )
        self.stats.add( "int", "Intelligence", trait_type="static", base=10, max=100, mod=0 )
        self.stats.add( "int_base", "IntelligenceBase", trait_type="static", base=10, max=100, mod=0 )
        self.traits.add( "level", "Level", trait_type="static", base=1, max=100, mod=0 )
        self.stats.add( "limit", "Limit", trait_type="static", base=0, max=1000, mod=0 )

    def at_pre_move(self, destination, **kwargs):
       """
       Called by self.move_to when trying to move somewhere. If this returns
       False, the move is immediately cancelled.
       """
       if self.db.is_sitting:
           self.msg( "You need to stand up first." )
           return False
       return True

    pass

class NonPlayerCharacter(DefaultCharacter):
    """
    The generic NPC, such as shopkeepers, trainers, etc.
    Inherits the DefaultCharacter class, without any of the Character attributes.
    """

class MobCharacter(Character):
    """
    Everything you can grind and kill to level up!
    Inherits the Character class so that we can use all of their attributes. 
    """
