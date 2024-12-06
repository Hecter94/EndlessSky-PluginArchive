# Main Plot Plus
[![Check Files](https://github.com/ziproot/endless-sky-main-plot-plus/actions/workflows/check-files.yml/badge.svg)](https://github.com/ziproot/endless-sky-main-plot-plus/actions/workflows/check-files.yml)

A plugin for the video game “endless sky” mostly centered around improving the main plot.

## Guided Start
This is an optional feature that can be enabled or disabled upon creating a new save or loading an existing one with this plugin installed for the first time. If you haven't chosen sides in the human civil war by July 3017, Guided Start will allow you to join the Free Worlds, and also the Syndicate if you have the Crisis in Management plugin installed. It will additionally allow you to remain neutral (see below). Any conditions blocking the campaigns from starting will be cleared. If you enter the spaceport, a map indicator will lead you to the planet to get started and remind you to enter the spaceport if necessary.

## Neutrality
You can choose to remain neutral in the human civil war. To do this, just play the game normally without choosing sides, then when asked what side you are on, say that you are neutral. When pressed, continue to remain neutral. Shortly after, land on any world one jump away from a Pug planet and tell the Pug that you are neutral, and you will be able to skip the main plot. However, there's a catch: a different pilot will do the free worlds campaign instead, and they will choose checkmate. If you want the reconciliation ending, join the Syndicate with the Crisis in Management plugin or join the Free Worlds and choose reconciliation. The missions are designed so that you will be relocated to Ruin and time will advance by several years, but this is waiting on several pull requests to be merged, so at the moment you will have to use your imagination.

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
Amazinite had, a long time ago, added changes that improved the Checkmate branch, that ultimately didn't go anywhere, other than some changes in the first part of the campaign rework. These changes will likely be added as part of the next parts of the campaign rework. However, as I am a fan of the Checkmate branch already, I think more people should be doing it, so I am incorporating these changes now, along with some minor fixes. Mostly, these allow you to ask about progress made by the Syndicate in finding the terrorists, and eventually allow you to “fight” them with automatic ships after the Pug invasion. I am also changing one major thing: the nuke launcher has been replaced with “augmented nuclear missiles,” which are essentially the buffed nuclear missiles proposed by Azure3141. When these begin being sold, the Syndicate also begin using them instead of regular nukes in a new “Mark II Nuclear” loadout in the systems raided by the Korath. This Manta loadout has four augmented nuclear missiles and two sidewinder missile launchers, the latter of which ensures that the Mantas use the “missile boat” AI, making them less likely to blow themselves up. This updated plot is referenced in the Neutrality option, mentioning the Syndicate finding the “terrorists” and the automatic vessels being used as cannon fodder. Both the old nuclear missiles and the new augmented nuclear missiles are also 10x cheaper than the nuclear missiles in vanilla are, i.e. they cost 100,000 credits each instead of a million credits each.

## Other Changes

### Free Worlds Albatross Bounty
The FW Albatross 2A mission requires you to fight Ryk Bartlett, essentially like a bounty mission, however, instead of using the Bounty government, Ryk Bartlett uses the Pirate government, allowing you to just wait for friendly ships to take the ship out. This replaces the government for Ryk Bartlett in that mission with the Bounty government.

### Deep Science Drones
0.10.5 added the sunder and mining drones, so I decided that it was time to allow you to get your own science drones! Some time after you do project hawking, Valhalla and Asgard will begin selling a drone variant of the aerie along with science drones, and a fleets consisting of an aerie with two science drones will begin to travel around the Deep. A few months later, miners will begin using the drone variant with mining drones to mine. The aerie drone variant is also occasionally used by the pirate fleet in road to hai reveal.

### Author Ships
Author ships no longer fine you, because they aren’t canon, with the exception of Captain Pester because she’s Captain Pester.

### Hai Reveal Closure and Side Missions
Hai Reveal is *not* unlocked in Main Plot Plus, however, when you finish all there is to Hai Reveal, you now get a pop-up explaining this and are able to once again do any side missions blocked by Hai Reveal. Turner Incorporated is also unlocked until Hai Reveal starts and after the pop-up.

## Bugs
I have playtested this plugin and fixed any bugs, edge cases, and warnings I could find. There may still be bugs, and bug reports and pull requests fixing bugs are welcome.

## Uninstalling
Most changes made by this plugin should be automatically reverted when the plugin is uninstalled or disabled. One exception is the Neutrality plotline, where if you uninstall or disable the plugin while in the middle of that plotline, you will be unable to finish the main plot, Hai Reveal, or Wanderers. If you have not finished Neutrality and Road to Hai Reveal, you will probably have to revert your save, as Hai Reveal normally requires you to complete Free Worlds. I do not recommend uninstalling or disabling Main Plot Plus if you are in the middle of the Neutrality or Road to Hai Reveal plotlines. The other exception is an edge case where you finish the Hai Reveal missions in vanilla, triggering the patch unlocking the other side missions, then uninstall the plugin, then continue Hai Reveal through Delta, the PR, or a plugin. This will result in “hr: secret leaks” not being set. If you are experiencing problems with Hai Reveal after uninstalling this plugin and you finished those missions, make sure “hr: secret leaks” is set.

## Other Plugins and Forks
My plugin takes the Crisis in Management plugin into account as much as possible, with the exception of Road to Hai Reveal. This means you still cannot do Hai Reveal if you did Crisis in Management. It also used to contain a patch to prevent the Constellations plugin from softlocking the game, but recent versions of this plugin no longer have the issue, so the patch has been removed, and loading this plugin should result in the patch also being reverted. This is because the patch would remove the wormhole if the plugin gets disabled/uninstalled, which I think is worse than old versions of one plugin breaking. Furthermore, Endless Sky Delta is a fork of Endless Sky adding in features that are not considered suitable for the base game at the moment, one of which is “engine slots” which breaks plugin ships that do not have slots assigned. As the only ship that would be broken is a person ship, I have given that person ship engine slots, as they won’t be noticed in non-Delta versions of the game anyways.

### Hai Reveal
Additionally, the Hai Reveal closure mission is designed not to offer if Hai Reveal can continue due to the “repair Hai Reveal” plugin or the Delta fork being installed. The patched Turner Incorporated mission will not offer in this case as the secret leaks condition will never be cleared. There should be no other issues with using this plugin in Endless Sky Delta or with the “repair Hai Reveal” plugin, but if there are other issues, feel free to leave a bug report. As for the hai.side.mission.unlocker and Lost in Midnight plugins, clearing the secret leaks tag will not break the plugins, and the old Turner Incorporated mission will not offer if another plugin mission offers, and will block the plugin mission from offering if it offers.

### Mega Freight Battles
Mega Freight Battles by 1010todd contains three missions that conflict with this plugin, so my conflicting missions override the Mega Freight Battles missions and spawn the ships from Mega Freight Battles if the plugin is detected, with permission from 1010todd. This requires the plugin being called “Mega Freight Battles” and requires the plugin to be enabled for those ships to spawn. It additionally requires Endless Sky version 0.10.3 or later, and the version of Mega Freight Battles linked in the Endless Sky Community Discord in the #plugin-releases channel on 2/29/2024 at 14:45 UTC. If these requirements are not met, there is still a conflict and one of the two plugins should be disabled. If the conflict is because of an update to Mega Freight Battles, please report this as a bug and I will try to address the changes as soon as possible. This uses a fail-safe approach, so all Mega Freight Battles NPCs will despawn if the plugin is disabled or the mission is offered without the plugin being enabled, and will not respawn. This does not prevent there from being a conflict, rather, this is an attempt to workaround the conflict. In most normal circumstances, there should not be an issue, however, that doesn’t mean that there isn’t one, so keep this in mind.

Conflicting missions:
```
FW Defend New Tibet (patched)
FW Liberate Delta Sagitarii (patched)
FWC Attack Kaus Borealis (patched)
```

### Mega Freight
Additionally, to prevent breakage if Mega Freight is not installed, the Mega Freight ships and variants used in the conflicting missions are defined to be the same as plugin commit 486f09479c941c51957ef40ed0f0c181500a640a (the latest commit as of 11/25/24 at 16:13 UTC). This means that if you have a later version of Mega Freight, your ships may be downgraded. If this is the case, temporarily uninstall Main Plot Plus and report this as a bug, so I can update the ships.

Conflicting ships and variants:
```
Eleonorae
PF-80 Intrepid
PF-80 Intrepid (Plasma Engine)
PF-80 Intrepid (Swordfish)
CK50T Stahbar (Proton)
PAS-2 Bulwark
PAS-3 Barbette
PCS-4 Castle
PCS-5 Citadel
SWV4 Ravelin
EP-3 Rat
AGT-31 Xencar
CS-24 Garrison
CS-24 Garrison (Parapet)
CSE-6 Steward
Falcon (Parapet)
FUe02y Gebrant Tender
TS-CH0 Kratzbal
Culverin Class (Mark II)
Spetum Class (Mark II)
Spetum Class (Mark II, ShieldRegen)
A-14F Rondel
```


## Copyright
This was originally donated to the public domain, however, I am not sure if I am allowed to do that given that I have copied text from a work licensed under the GPL v3 or later. I have relicensed it under the GPL to make sure that I am not violating any rules. I would therefore recommend following the GPL v3 anyways.

## Note on Breaking Changes
I have made a full release, which means that there will be no more “breaking” changes. For those who just downloaded the beta or full release, I still make no guarantees, but I will try to prevent save issues from now on. Note that I still may rename missions, for instance, but I will provide patch missions, whereas before this wasn't the case. However, those playing before the release will likely have to go through breaking changes when updating to a release branch, including, but not limited to, renaming the plugin, renaming files, removing files, reorganizing files, splitting files, merging files, and modifying data files without providing patch missions or other backwards compatibility features. For those who tested out my plugin before release, thank you, but treat this like you would the “continuous” branch of Endless Sky, except for updates after the release, and do not be surprised if you end up with broken saves. Remember, there is no warranty.
