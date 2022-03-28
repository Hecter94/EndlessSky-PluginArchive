# Endless Sky Plugin Archive

## Introduction
A comprehensive library of ~350 ancient and new plugins for the open-source game Endless Sky. 

## Downloading: 
 
Third party tool such as [this](https://download-directory.github.io/) can download a single folder/plugin. 
Paste the url to the folder url into that tool and you will be given a .zip for that folder. 
- For example, for the "50 cal" plugin, enter: https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/All%20Plugins/50%20cal

Github by default only allows the entire library to be downloaded as a single .zip. **Github may have issues with downloading very large file sizes**, a possible workaround is using Github Desktop or Git Bash to clone the repository.

## Notes

"Working" directory – plugins updated to work with the continous build of Endless Sky

"Originals" directory – archived copies of original plugins 

"Nonfunctional" directory – plugins with serious conflict with continuous build

[Here](Plugin%20Manifest.md) for plugin list and descriptions.
## Known Plugin Issues

	
***A Galaxy Far Far Away, Businessman Mod, Endless Depth, Normandy***
- Title screen missing/corrupted.
 override the title screen, using one or more of these can cause issues with it looking corrupted or "missing". Recommend to use one of these at a time, OR delete title.png from \images to restore the vanilla title screen

***Civil War, Edge of Endless, Jump to Lightspeed and Star Wars***
- all edit the vanilla interface, this can also cause issues and can only be fixed by editing/removing the interfaces.txt file in the plugin.

***A Wonderful Worldship*** 
- Random sprites replaced by worldships
	Culprit: Intended Behavior of "A wonderful worldship mod"
	
***Bare Ships*** 
- clears all ships from shipyards, meaning only bare versions of ships will be available, any plugins adding other ships not to custom shipyards will likely be incompatible

***Elite Sky*** 
- creates an Interceptor "bay type" which seems to make any interceptor escort jump around randomly.

***Final Frontier*** 
- sets every government swizzle to 0, also has an image named raider which conflicts with vanilla korath raider.

***Star Wars***
- includes a copy of vanilla data files and will likely conflict with any missions added/changed since it was created. Specifically known to conflict with changes to the Remnant storyline.
- Star Wars has an image named fury which conflicts with vanilla fury.

***Recovery Ships***
- NPC Ships unable to assist with fuel or repairs
	Culprit: Likely an old version of Recovery Ship, updated 2/8/2022. Please let me know if you still see the issue. 
	
- Escorts from missions not spawning correctly
	Culprit: use the “safe” variant of this plugin to fix this behavior, “safe” version ships can only carry "Fighter" from vanilla  and "Heavy Fighter" and "Gunship"

***The Station of Dr. Rousseau***
- "Bounty" Arfecta is spawned directly outside starting location. 
	Culprit: , Mission: "Puzzle 3". No location is defined so Arfecta is spawned on first "landing".

