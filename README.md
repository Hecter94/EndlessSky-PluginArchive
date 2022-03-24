# Endless Sky Plugin Archive

Some plugins have been updated to work with continous, any plugins which have been updated will be in the "Working" directory, originals of those plugins will be available in the "originals" directory for compatability and for archival

Note, by default GitHub does not allow for downloading a single folder, you will need to download or clone the repository and then pick the plugins you want. Alternatively, you can use a third party tool such as [this](https://download-directory.github.io/) to download a single folder. Simply paste the url to the folder you want in that tool and you will be given a link to download just that folder.

Please see [here](Plugin%20Manifest.md) for a list of plugins and their descriptions and please see below for a list of known issues.

Known Issues

"Bounty" Arfecta is spawned directly outside starting location. 
	Culprit: The Station of Dr. Rousseau, Mission: "Puzzle 3". No location is defined so Arfecta is spawned on first "landing".

NPC Ships unable to assist with fuel or repairs
	Culprit: Likely an old version of Recovery Ship, updated 2/8/2022. Please let me know if you still see the issue. 
	
Escorts from missions not spawning correctly
	Culprit: Caused by Recovery Ships(not safemode), use the “safe” variant of this plugin to fix this behavior, “safe” version ships can only carry "Fighter" from vanilla  and "Heavy Fighter" and "Gunship"
		
Random sprites replaced by worldships
	Culprit: Intended Behavior of "A wonderful worldship mod"
	
Title screen missing/corrupted.
Normandy, A Galaxy Far Far Away, Endless Depth, plugin and Businessman Mod all override the title screen, using one or more of these can cause issues with it 	looking corrupted or "missing". Recommend to use one of these at a time, OR delete title.png from \images to restore the vanilla title screen
Edge of Endless, Civil War, Jump to Lightspeed and Star Wars all edit the vanilla interface, this can also cause issues and can only be fixed by editing the interfaces.txt file in the plugin

"Star Wars" includes a copy of vanilla data files and will likely conflict with any missions added/changed since it was created. Specifically known to conflict with changes to the Remnant storyline.
Star Wars has an image named fury which conflicts with vanilla fury.

Bare Ships clears all ships from shipyards, meaning only bare versions of ships will be available, any plugins adding other ships not to custom shipyards will likely be incompatible

Final Frontier sets every government swizzle to 0, also has an image named raider which conflicts with vanilla korath raider.

Elite Sky make Interceptor "bay type" which seems to make any interceptor escort jump around randomly.
