# EvenLowerDamage

This plugin is a more extreme version of [LowerDamage](https://github.com/Arachi-Lover/LowerDamage), which rescales the damage of weapons throughout Endless Sky in order to make the game's combat slower, and also aid in making ships affected by LinearHPScaling last longer in combat (though this plugin may be used on its own just as well).

The idea was to multiply the damage of every weapon in the game by a decimal factor, in order to make combat feel slower, with ships lasting longer and regeneration mattering more.

These multipliers would apply only to damage values that affect shields and hull, be that per shot/hit or over time, as a means to also give more value to the status effect damage types. Thus, the affected damage types are:

- shield
- hull
- discharge
- corrosion

Spacefaring creatures such as the Void Sprite and Subsidurial were not affected.

Below are the multiplier values across Tiers, and some notes specific to some outfits/groups.

```
T1 and below
	* 0.7 damage
	(The Nuclear Missile remains unchanged, as it should continue to pose a very credible threat to human ships over the campaign, and by consequence of all other weapons being weaker, would also become a more considerable reward for picking the Checkmate branch)
	(Of the Sheragi, only the Dragonflame Cannon was altered, as the turrets aren't particularly great as is, and also owing to the unique nature of the reward-ship and its Fighters)
T1.5
	* 0.75 damage
T2
	* 0.8 damage
T2.5
	* 0.85 damage
	(The MCS Extractor was spared for it already is terrible at dealing damage)
T3
	* 0.9 damage
T4
	* 0.6 damage
	(Only the Drak Augmented weapons were affected)
```

**EvenLowerDamage** then goes a step further, and slices all of those damage values by 2, so in practice:

```
T1 and below
	* 0.35 damage
T1.5
	* 0.375 damage
T2
	* 0.4 damage
T2.5
	* 0.425 damage
T3
	* 0.45 damage
T4
	* 0.3 damage
```

#### Arachi's Plugins

[LinearHPScaling](https://github.com/Arachi-Lover/LinearHPScaling)
[LowerDamage](https://github.com/Arachi-Lover/LowerDamage)
[EvenLowerDamage](https://github.com/Arachi-Lover/EvenLowerDamage)
[RacingFlivverModifications](https://github.com/Arachi-Lover/RacingFlivverModifications)
[SmolEngines](https://github.com/Arachi-Lover/SmolEngines)
[PirateVariantsHPFix](https://github.com/Arachi-Lover/PirateVariantsHPFix)
[Glory to the CCOR](https://github.com/Arachi-Lover/Glory-to-the-CCOR)
