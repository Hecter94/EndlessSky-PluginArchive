# Main Plot Plus
[![Check Files](https://github.com/ziproot/endless-sky-main-plot-plus/actions/workflows/check-files.yml/badge.svg)](https://github.com/ziproot/endless-sky-main-plot-plus/actions/workflows/check-files.yml)

A plugin for the video game “endless sky” mostly centered around improving the main plot.

## Guided Start
This is an optional feature that can be enabled or disabled upon creating a new save or loading an existing one with this plugin installed for the first time. If you haven't chosen sides in the human civil war by July 3017, Guided Start will allow you to join the Free Worlds, and also the Syndicate if you have the Crisis in Management plugin installed. It will additionally allow you to remain neutral (see below). Any conditions blocking the campaigns from starting will be cleared. If you enter the spaceport, a map indicator will lead you to the planet to get started and remind you to enter the spaceport if necessary.

## Fast Forward
This is a start two years later than the present. To unlock it, you must have made it to the point where Fast Forward begins. It automatically reveals all of human space and puts you in Wayfarer with no loan and enough credits to buy an Osprey. Since it is two years later, you can immediately start doing the free worlds prologue missions, but you are also unable to do pact recon.

## Neutrality
You can choose to remain neutral in the human civil war. To do this, just play the game normally without choosing sides, then when asked what side you are on, say that you are neutral. When pressed, continue to remain neutral. Shortly after, land on any world one jump away from a Pug planet and tell the Pug that you are neutral, and you will be able to skip the main plot. However, there's a catch: a different pilot will do the free worlds campaign instead, and they will choose checkmate. If you want the reconciliation ending, join the Syndicate with the Crisis in Management plugin or join the Free Worlds and choose reconciliation. The missions are designed so that you will be relocated to Ruin and time will advance by several years, but this is waiting on several pull requests to be merged, so at the moment you will have to use your imagination. Your reward for completing Neutrality is a subsidurial pet.

### Compatibility
Neutrality should be compatible with most major missions in the base game. You are told about the Pug war, the Free Worlds having nuclear weapons, and some of the new outfits produced by humanity: the plasma turret, flamethrower, s-970 regenerator, s-270 regenerator, ionic afterburner, typhoon torpedo launcher, electron beam, and catalytic ramscoop. This isn't everything, as it excludes the stack core due to it not being sold by Kraz Cybernetics, but it is enough to cover everything in the Coalition intros. You also learn about the Oathkeepers, and you assist Danforth by taking out a pirate fleet, unlocking the Wanderers campaign. From there, you can start Hai Reveal through Fiona and Rain, as the pirate fleet happened to have Hai weapons. I have additionally patched a mission that assumes you know Alondo.

## Road to Hai Reveal
Hai Reveal is still in a work in progress state. Additionally, it at the moment requires you to specifically join the Free Worlds, or none of the missions after the leak will offer. As a result, I have a series of missions called “Road to Hai Reveal” that will allow you to do the intro of Hai Reveal if you have done Neutrality. I have also patched all the post-war reactions, see below. I have set it up so that you meet Alondo, which should allow the rest of Hai Reveal to work without issue if it gets merged as-is. If it gets changed to be more campaign agnostic, that still works and you can go down the free worlds path.

### Post War Reactions
The post-war reactions by default all assume you have directly fought with the Pug, which isn't necessarily true in Crisis in Management and definitely isn't true in the Neutrality option. I have replaced all three of these with patch missions which vary depending on how you interacted with the Pug, based on this plugin, the vanilla Free Worlds Reconciliation branch, and Crisis in Management. It also tries to test if you have done the vanilla version of Free Worlds Checkmate instead, if needed. I also removed a stupid section about the Free Worlds and Navy captains joking about almost killing each other, and I have reverted the gender of a character in War Reactions: Syndicate Orphan because MasterofGrey says that the change was not justified. Other than that, doing Free Worlds should result in the same post-war reactions as vanilla, but doing Crisis in Management or the Neutrality option will give you different outcomes that make sense for what you've done.

## Syndicate
The Syndicate will now use their new technology on their ships if you complete the main plot, though they still won't sell it to you if you did reconciliation. The weights of the variants are based on the ones for the republic Mark II ships. A few of the Mark II variants are used in vanilla for a few missions in the reconciliation branch, but I added a bunch more so that all the Syndicate ships used in their main fleets have Mark II variants. The Syndicate rarely uses nuclear missiles before the war in the eastern parts of the Core, where they get raided by the Korath. They stop in 3014 because of the impending war.

### Test Dummies
Do you know those test dummy missions that you have to do? Well, there's a reason for them. Amazinite's Checkmate improvements include “automatic” ships. I have added these ships to occasionally show up in the Syndicate fleets after the main plot. They are essentially the same as the normal “mark II” ships, except that they have a special government that can change hails to use the test dummy ones, they cannot be bribed, they have the same confusion as the target practice jobs, they have the “automaton” and “self-destruct” attributes from the jobs, they are always called “Syndicate Test Vessel,” and, being expensive, try to avoid battle and run away if threatened. Speaking of the test dummies, you can no longer fight them after the main plot, as the Syndicate has moved to the next phase of their testing and has started to incorporate them in their fleet.

## Improved Checkmate
Amazinite had, a long time ago, added changes that improved the Checkmate branch, that ultimately didn't go anywhere, other than some changes in the first part of the campaign rework. These changes will likely be added as part of the next parts of the campaign rework. However, as I am a fan of the Checkmate branch already, I think more people should be doing it, so I am incorporating these changes now, along with some minor fixes. Mostly, these allow you to ask about progress made by the Syndicate in finding the terrorists, and eventually allow you to “fight” them with automatic ships after the Pug invasion. This updated plot is referenced in the Neutrality option, mentioning the Syndicate finding the “terrorists” and the automatic vessels being used as cannon fodder.

### Nuclear Missile (Mark II)
I am also changing one major thing: the nuke launcher is three times smaller, but it now launches “mark II nuclear missiles,” which are essentially the buffed nuclear missiles proposed by Azure3141, but with ionization damage. When these begin being sold, the Syndicate also begin using them instead of regular nukes in a new “Mark II Nuclear” loadout in the systems raided by the Korath. This Manta loadout has two nuclear launch bays holding four mark II missiles, and two sidewinder missile launchers holding 90 sidewinder missiles, the latter of which ensure that the Mantas use the “missile boat” AI, making them less likely to blow themselves up. The old nuclear missiles are 10x cheaper than the nuclear missiles in vanilla are, i.e. they cost 100,000 credits each instead of a million credits each. The nuclear launch bay costs 1 million credits, but each mark II nuke only costs 80,000 credits and can load two nukes, and you can restock from any outfitter via 0.10.13’s system. There is not a storage container for nukes as each one takes up weapon and outfit space directly, which is the main reason why the nuclear launch bay takes up so little outfit space on its own. However, you can still add one ton nuclear installation chips to *load* additional nukes. This is required mainly so that the game can let you refill to whatever target you want without you having to manually rebuy the nukes yourself.

## Other Changes

### Other Free Worlds Changes
The FW Albatross 2A mission requires you to fight Ryk Bartlett, essentially like a bounty mission, however, instead of using the Bounty government, Ryk Bartlett uses the Pirate government, allowing you to just wait for friendly ships to take the ship out. This replaces the government for Ryk Bartlett in that mission with the Bounty government. Additionally, the longest Han Sizer Month job now gives a brief paragraph of flavor text, made by Zitchas, once you land on the final planet before heading to your destination.

### Deep Science Drones
0.10.5 added the sunder and mining drones, so I decided that it was time to allow you to get your own science drones! Some time after you do project hawking, Valhalla and Asgard will begin selling a drone variant of the aerie along with science drones, and a fleets consisting of an aerie with two science drones will begin to travel around the Deep. You will know this happens when you see an advertisement for a science drone upon entering a shipyard that sells it. A few months later, miners will begin using the drone variant with mining drones to mine. The aerie drone variant is also occasionally used by the pirate fleet in road to hai reveal.

### Author Ships
Author ships no longer fine you, because they aren’t canon, with the exception of Captain Pester because she’s Captain Pester.

### Security Analyses and Blueberry1vom1t’s Discount Paint Plugin
I have included Blueberry1vom1t’s “Discount Paint Plugin,” which you can toggle on or off, allowing you to change the swizzle of your ship via the job board. I have also included jobs in nearly every populated planet that allow to see your armament deterrance, cargo attraction, and local reputation, which changes based on what I think makes the most sense, but is usually the planetary government or is mentioned in the job description. The main exceptions are the Avgi systems, which are dependent on hidden planet attributes that determine which faction the planet is likely to be aligned with, however, landing on a non tangled shroud planet will get you the generic Avgi reputation, while landing on a twilight guard or dissonance planet will get you twilight guard or angry dissonance reputation. Landing on Weledos will give you the Avgi consonance reputation, and landing on any other Consonance planet in the tangled shroud will get you the Avgi dissonance reputation.

## Bugs
I have playtested this plugin and fixed any bugs, edge cases, and warnings I could find. There may still be bugs, and bug reports and pull requests fixing bugs are welcome.

## Uninstalling
Most changes made by this plugin should be automatically reverted when the plugin is uninstalled or disabled. One exception is the Neutrality plotline, where if you uninstall or disable the plugin while in the middle of that plotline, you will be unable to finish the main plot, Hai Reveal, or Wanderers. If you have not finished Neutrality and Road to Hai Reveal, you will probably have to revert your save, as Hai Reveal normally requires you to complete Free Worlds. I do not recommend uninstalling or disabling Main Plot Plus if you are in the middle of the Neutrality or Road to Hai Reveal plotlines.

## Other Plugins and Forks
My plugin takes the Crisis in Management plugin into account as much as possible, with the exception of Road to Hai Reveal. This means you still cannot do Hai Reveal if you did Crisis in Management. It also used to contain a patch to prevent the Constellations plugin from softlocking the game, but recent versions of this plugin no longer have the issue, so the patch has been removed, and loading this plugin should result in the patch also being reverted. This is because the patch would remove the wormhole if the plugin gets disabled/uninstalled, which I think is worse than old versions of one plugin breaking.

### Mega Freight Battles
Mega Freight Battles conflicts with Main Plot Plus. This was something I was initially working around, however, Saugia has nerfed the Free Worlds battles and especially made the fleets in those battles smaller. Therefore, I have nerfed my versions of the battles, and opted not to support Mega Freight Battles. This is because Mega Freight Battles makes the fleets even bigger, which is contrary to Saugia’s goal of reducing fleet size, and therefore is not something I will be supporting any longer. If you have Mega Freight Battles, you CAN use this plugin, however, the following missions may be one or the other due to conflicts and race conditions:

Conflicting missions:
```
FW Defend New Tibet (patched)
FW Liberate Delta Sagitarii (patched)
FWC Attack Kaus Borealis (patched)
```

## Copyright
This was originally donated to the public domain, however, I am not sure if I am allowed to do that given that I have copied text from a work licensed under the GPL v3 or later. I have relicensed it under the GPL to make sure that I am not violating any rules. I would therefore recommend following the GPL v3 anyways.

## Note on Breaking Changes
I have made a full release, which means that there will be no more “breaking” changes. For those who just downloaded the beta or full release, I still make no guarantees, but I will try to prevent save issues from now on. Note that I still may rename missions, for instance, but I will provide patch missions, whereas before this wasn't the case. However, those playing before the release will likely have to go through breaking changes when updating to a release branch, including, but not limited to, renaming the plugin, renaming files, removing files, reorganizing files, splitting files, merging files, and modifying data files without providing patch missions or other backwards compatibility features. For those who tested out my plugin before release, thank you, but treat this like you would the “continuous” branch of Endless Sky, except for updates after the release, and do not be surprised if you end up with broken saves. Remember, there is no warranty.
