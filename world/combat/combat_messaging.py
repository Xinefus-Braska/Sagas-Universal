"""
This file will contains the functions for controlling messaging to the
characters and NPCs in a room where combat is happening. The messaging will be
divided into three kinds of occupants of the room:
- Attacker - The person that is taking an action like hitting, blocking, etc.
- Victim - The person that is beiong acted upon. They've been hit, dodged, etc
- Observer - Any characters or NPCs that are in the room, but are not the
             attacker or victim. They may or may not be a part of the combat, but
             that is independent of the role determination
The messaging functions will be called by combat_actions script objects or the
combat handler script object. The messaging functions in turn will pull phrasing
for combat action descriptions from a number of sources:
- The combat description file - Contains 90% of the combat descriptions or more.
                                These are stored in dictionaries.
- From item objects - For example, weapons can have their owbn unique attack
                      phrases. As weapons become more powerful, this gets more
                      common
- From character objects - Some characters will have mutations that give them
                           unique attack phrases.
- From room objects - Some rooms will have unique movement phrases. For example,
                      a character may fail to close range because of slipping in
                      mud.
"""
from evennia import utils
from evennia.utils.logger import log_file
from world.combat.combat_desc import return_unarmed_damage_normal_text as rudnt, \
    return_dodge_text as dodgetxt, return_unarmed_block_text as blocktxt, \
    return_grappling_takedown_text as takedowntxt, return_grappling_position_text as grappling_pos_txt, \
    return_grappling_unarmed_damage_normal_text as grudnt, return_grappling_submission_text as rgsat, \
    return_grappling_escape_text as rgeat, return_melee_weapon_strike_text as mwst

## functions for delivering messages
# what characters and NPCs are in the room?
def determine_objects_in_room(location, attacker, victim):
    """
    This function takes in a room object where combat is happening, checks the
    contents of the room, and determines which objects should get a message.
    """
    log_file("start of determine objects in room func", filename='combat_step.log')
    # empty dictionary for use later
    pcs_and_npcs_in_room = {'Attacker': [], 'Victim': [], 'Observers': []}
    # get room contents
    objects_in_room = location.contents
    log_file(f"Room: {location} contents: {location.contents}", \
             filename='combat_step.log')
    # loop through contents and determine if they are the correct typeclasses
    # to be messaged at
    for obj in objects_in_room:
        log_file(f"Testing {obj} to see if they are a char or NPC.", \
                 filename='combat_step.log')
        # TODO: Add NPC typeclasses to this when we create them
        if utils.inherits_from(obj, 'typeclasses.npcs.NPC') or utils.inherits_from(obj, 'typeclasses.characters.Character'):
            log_file(f"Role assignment for {obj.name}", filename='combat_step.log')
            if obj == attacker:
                pcs_and_npcs_in_room['Attacker'] = attacker
                log_file(f"{obj.name} is the attacker.", filename='combat_step.log')
            elif obj == victim:
                pcs_and_npcs_in_room['Victim'] = victim
                log_file(f"{obj.name} is the victim.", filename='combat_step.log')
            else:
                pcs_and_npcs_in_room['Observers'].append(obj)
                log_file(f"{obj.name} is an observer.", filename='combat_step.log')
        else:
            log_file(f"{obj} not a char or NPC. type: {type(obj)}", \
                     filename='combat_step.log')
            pass
    # return dict of player and NPC objects
    return pcs_and_npcs_in_room


def send_msg_to_attacker(attacker, attacker_msg_string):
    """
    This function takes in the object performing an action, like attack or
    dodging plus a message string formatted in the first person tense. It then
    sends them that message.
    """
    log_file("start of send msg to attacker func", filename='combat_step.log')
    attacker.msg(f"{attacker_msg_string}")
    attacker.execute_cmd("rprom")


def send_msg_to_victim(victim, victim_msg_string):
    """
    This function takes in the object that is being acted upon, such as the
    player being attacked. It then sens them a message in the third person,
    with their name replaced by 'you'.
    """
    log_file("start of send msg to victim func", filename='combat_step.log')
    victim.msg(f"{victim_msg_string}")
    victim.execute_cmd("rprom")


def send_msg_to_observer(observer, observer_msg_string):
    """
    This function takes in the attacker object and the message string to be
    sent to the attacker. The function then messeages the attacker.
    """
    log_file("start of send msg to observer func", filename='combat_step.log')
    observer.msg(f"{observer_msg_string}")
    observer.execute_cmd("rprom")


def send_msg_to_objects(pcs_and_npcs_in_room, attacker_msg_string, victim_msg_string, observer_msg_string):
    """
    This function gathers in the info to call all three of the functions above
    and calls them.
    """
    log_file("start of send msg to all objs func", filename='combat_step.log')
    log_file(f"Roles - Attacker: {pcs_and_npcs_in_room['Attacker']} Victim: {pcs_and_npcs_in_room['Victim']} Observers: {pcs_and_npcs_in_room['Observers']}", \
             filename='combat_step.log')
    log_file(f"msg strings: {attacker_msg_string} {victim_msg_string} {observer_msg_string}", \
             filename='combat_step.log')
    for role, character in pcs_and_npcs_in_room.items():
        if role == 'Attacker':
            send_msg_to_attacker(character, attacker_msg_string)
        elif role == 'Victim':
            send_msg_to_victim(character, victim_msg_string)
        elif role == 'Observers':
            for observer in pcs_and_npcs_in_room['Observers']:
                log_file(f"attempting to send msg for {observer.name}", \
                         filename='combat_step.log')
                send_msg_to_observer(observer, observer_msg_string)
