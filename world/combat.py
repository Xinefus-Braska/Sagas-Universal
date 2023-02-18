"""
Combat can be initiated either via 'attack <target>' or through the use of a 
skill on a target, e.g. punch <target> or lunge <target> or blast <target>.

Once combat has begun, combatants cannot leave the current room. Combat persists
in that room until a victory/death, or flee. 

When a PC flees from an NPC, the NPC will retain aggression until zone/area resets. 

Combat based on rounds. Damage or healing to be calculated based on roll of
character attributes. 

NPCs will auto attack every round using basic library of attacks, and 
perhaps have certain special attacks based on certain attributes of the NPC. 

PCs will auto attack every round but with a limited library of basic attacks.
Victory is not guaranteed to the more experienced or strongest. PCs required to
input commands while in combat to add to the fight. These will be special
attacks/skills/spells. 

"""