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
from evennia.utils.logger import log_file
from evennia.contrib.rpg.traits import TraitHandler
from world.combat.dice_roller import return_a_roll as roll, return_a_roll_sans_crits as rarsc
from evennia import gametime, create_script

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

        self.traits.clear()
        self.skills.clear()
        self.stats.clear()

        self.traits.add( "lf_base", "LifeforceBase", trait_type="static", base=1000, mod=0 )
        self.traits.add( "lf", "Lifeforce", trait_type="gauge", base=0, max=1000000000000, mod=0 )
        self.stats.add( "str", "Strength", trait_type="static", base=10, max=100, mod=0 )
        self.stats.add( "str_base", "StrengthBase", trait_type="static", base=10, max=100, mod=0 )
        self.stats.add( "dex", "Dexterity", trait_type="static", base=10, max=100, mod=0 )
        self.stats.add( "dex_base", "DexterityBase", trait_type="static", base=10, max=100, mod=0 )
        self.stats.add( "int", "Intelligence", trait_type="static", base=10, max=100, mod=0 )
        self.stats.add( "int_base", "IntelligenceBase", trait_type="static", base=10, max=100, mod=0 )
        self.traits.add( "level", "Level", trait_type="static", base=1, max=100, mod=0 )
        self.stats.add( "limit", "Limit", trait_type="static", base=0, max=1000, mod=0 )

        # set up intial equipment slots for the character. Since the character
        # is new and has no mutations, there won't be slots like tail or extra
        # arms
        self.db.limbs = ( ('head', ('head', 'face', 'ears', 'neck')),
                          ('torso', ('chest', 'back', 'waist')),
                          ('arms', ('shoulders', 'arms', 'hands', 'ring')),
                          ('legs', ('legs', 'feet')),
                          ('weapon', ('main hand', 'off hand')) )
        
        # define slots that go with the limbs.
        # TODO: Write a function for changing slots if/when mutations cause
        # new limbs to be grown or damage causes them to be lost
        self.db.slots = {
            'head': None,
            'face': None,
            'ears': None,
            'neck': None,
            'chest': None,
            'back': None,
            'waist': None,
            'shoulders': None,
            'arms': None,
            'hands': None,
            'ring': None,
            'legs': None,
            'feet': None,
            'main hand': None,
            'off hand': None
        }

        # Add in info db to store other useful tidbits we'll need
        self.db.info = {'Target': None, 'Mercy': True, 'Default Attack': 'unarmed_strike',
                        'In Combat': False, 'Position': 'standing', 'Sneaking' : False,
                        'Wimpy': 100, 'Yield': 200, 'Title': None}

    def populate_num_combat_actions(self):
        """
        Rolls to determine the number of actions the character can perform during
        this round of combat.
        """
        log_file(f"start of num of combat actions function for {self.name}.", \
                 filename='combat_step.log')
        # listing out modifiers for readbility
        actions_roll = ((self.stats.dex.value + self.stats.int.value))
        log_file(f"{self.name} rolling {actions_roll} for actions. This \
                 will be divided by 100 and then rounded.", filename='combat_step.log')
        self.ndb.num_of_actions = round((roll(actions_roll, 'very flat', \
                                       self.stats.dex.value, self.stats.int.value)) / 100)
        log_file(f"{self.name} gets {self.ndb.num_of_actions} actions.", \
                 filename='combat.log')

    def at_heartbeat_tick_regen_me(self):
        """
        This function will be fired off at the heartbeat tick of the global
        MovingSpotlightTick script. It will determine randomly how much health,
        stamina, and conviction to regen at that tick. Being in combat will
        reduce regen. Other factors that influence regen are ability scores,
        mutations, and the phases of the three moons.
        """
        log_file(f"start of regen tick function for {self.name}.", \
                 filename='time_tick.log')
        # first, check if we're in combat
        if self.db.info['In Combat']:
            combat_mod = .25
        else:
            combat_mod = 1
        # next, check position
        pos_mod = 1
        if self.db.info['Position'] == "resting":
            pos_mod = 1.1
        elif self.db.info['Position'] == "sitting":
            pos_mod = 1.1
        elif self.db.info['Position'] == "supine":
            pos_mod = 1.2
        elif self.db.info['Position'] == "prone":
            pos_mod = 1.2
        elif self.db.info['Position'] == "sleeping":
            pos_mod = 1.5
        # TODO: implement moon phase modifier when we have that
        # TODO: Add a multiplier for wounds once we implment those
        # define regen dice and roll for amount to regen
        lf_regen_dice = (self.stats.str.value + self.stats.int.value + \
                         self.stats.dex.value ) * combat_mod * pos_mod * 2
        lf_regen_roll = round(roll(lf_regen_dice, 'normal', \
                        self.ability_scores.Vit, self.traits.hp))
        log_file(f"{self.name} regen tick - LF: {lf_regen_roll}", \
                 filename='time_tick.log')
        self.traits.lf.current += lf_regen_roll

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
