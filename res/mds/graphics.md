
All Plugins (604)

[Cheats](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/cheats.md) (38) | [Gameplay](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/gameplay.md) (55) | [Graphics](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/graphics.md) (29) | [Outfits](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/outfits.md) (52)<br>
[Overhauls](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/overhauls.md) (46) | [Overwrites](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/overwrites.md) (4) | [Patches](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/patches.md) (3) | [Races](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/races.md) (70)<br>
[Ships](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/ships.md) (143) | [Starts](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/md/starts.md) (17) | [Story](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/story.md) (80) | [Weapons](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/weapons.md) (42)<br>
[Uncategorized](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/uncategorized.md) (25)<br>

---

## Graphics

<p>29 plugins in this category.<p>


 

---

### additional.command.buttons
<img src='../../Working/additional.command.buttons/icon.png' height='100'></img><br>


[additional.command.buttons.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/additional.command.buttons.zip) | 17.65 kb | 2024-06-07 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/additional.command.buttons/) <br>
Author: zuckung | Category: Graphics <br>
[https://github.com/zuckung/endless-sky-plugins](https://github.com/zuckung/endless-sky-plugins) (last commit 2024-06-07) <br>

>Made for the mobile version and adds several new buttons to the lower right corner. See the readme for details.
>(inspired by theweirednut)
>
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote>### additional.command.buttons <br>
<br>
Made for the mobile version and changes the interface by adding the following 10 buttons: <br> 
<ul>
<li>full stop</li>
<li>board ship</li>
<li>land on planet</li>
<li>fleet: harvest flotsam</li>
<li>fleet: hold position</li>
<li>fleet: gather around me</li>
<li>fleet: attack my target</li>
<li>fleet: toggle ammo usage</li>
<li>view player info</li>
<li>fast forward</li>
</ul>
and
<ul>
<li>adjusts the message box to not overlap</li>
<li>moved the hidden ammo box to a visible place</li>
</ul>
<br>
(inspired by theweirednut) <br>
<br>
<img src='https://raw.githubusercontent.com/zuckung/endless-sky-plugins/master/screenshots/additional.command.buttons01.jpg' width='400'>
<br>
Allthough most of these commands are now implemented in other parts to the original mobile user interface or can be accessed by gestures, I personally prefer these buttons on the lower right corner.<br>
<br>
Additional there are some functions in this plugin that the original mobile ui can't do at the moment:<br>
- board button cycles through the possibilities <br>
- fleet commands can be used for single ships when selected <br>
<br>
This plugin overwrites `interface "main buttons"` and `interface "hud"`, so it isn't compatible with other plugins modifying these.<br>
<br>
<br>
Changelog:<br>
<br>
2024-06-07<br>
text corrections (thx to TheGiraffe3)<br>
<br>
2024-02-20<br>
re-added the ammo box to main buttons (latest mobile game version needed)<br>
<br>
2023-10-17<br>
added plugin.txt<br>
<br>
2023-08-24<br>
fixed non-firing attack button<br>
<br>
2023-08-05<br>
moved the hidden ammo box to a visible place<br>
<br>
2023-08-02<br>
added new icon and reworked readme<br>
<br>
2023-07-26<br>
added 3 more buttons to a total of 10<br>
added descriptions inside script to exchange buttons functions<br>
<br>
2023-07-06<br>
changed 'fire afterburner' to new 'fleet: harvest flotsam', because afterburner can easily toggled by double tapping<br>

</blockquote>
</details>

Status: DEPRECATED, continued in plugin "additional.command.buttons.radial" <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### additional.command.buttons.radial
<img src='../../Working/additional.command.buttons.radial/icon.png' height='100'></img><br>


[additional.command.buttons.radial.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/additional.command.buttons.radial.zip) | 404.67 kb | 2025-07-29 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/additional.command.buttons.radial/) <br>
Author: zuckung | Category: Graphics <br>
[https://github.com/zuckung/endless-sky-plugins](https://github.com/zuckung/endless-sky-plugins) (last commit 2025-07-28) <br>

>Made for the MOBILE ANDROID version. Adds several new buttons to the lower right corner. See the README for details.
>
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote>### additional.command.buttons <br>
<br>
Reworks the main buttons ui on the lower right side. Made for the ANDROID version of ES.<br> 
<br>
<br>
This plugin<br>
- rearranges and resizes some of the buttons<br>
- changes most icons (making a ring around as a standard)
- adds more permanent buttons from the radial menus to make them easy accessible<br>
- removes the radial menus<br>
- adds a new button row to the top right for the fleet commands<br>
- adds zoom buttons<br>
- adds more targeting buttons<br>
- greyes out inactive buttons<br>
- puts images behind the buttons, to grey out unavailable.<br>
- changes the ship hud<br>
<br>
merged the plugin landing.images.android:
Moves the landing image above the textbox, instead of behind the textbox.<br>
<br>
In case parts of the UI/the buttons are outside the screen, try rescaling your UI in the ES options<br>
If that doesn't help, open the zip, edit 'additional.command.buttons.radial/data/planet.txt' and change line 2 to 7 to:<br>
	image "land"
		center -60 -150
		dimensions 250 135
	sprite "ui/frame"
		center -60 -150
		dimensions 265 150
That resizes the landing image and the frame to their half.<br>
<br>
<br>
Changelog:<br>
<br>
2025-07-28<br>
made bottom right invisible buttons rectangle to fill out whole box<br>
<br>
2025-06-06<br>
merged with plugin landing.images.android<br>
added new line of buttons to top left<br>
added more greyed out buttons<br>
<br>
2025-04-26<br>
added greyed-out attack button if you can't attack<br>
fixed non-working recall button (thx to VelvetKrow)<br>
<br>
2025-04-21<br>
added 2xicon<br>
moved zoom+- to top left<br>
added round thrust / afterburner to bottom right<br>
removed thrust/afterburner from bottom left<br>
added more space between bottom right buttons<br>
<br>
2025-03-14<br>
added reverse thrust/afterburner button to bottom left<br>
<br>
2025-02-28<br>
moved the fleet box below the text box<br>
adjusted onscreen joystick size<br>
<br>
2025-02-23<br>
added new fleet jump button<br>
moved targeting buttons to the lower right<br>
removed fleet attack from normal attack button<br>
removed targeting button from target display<br>
<br>
2025-02-06<br>
the targeting buttons blocked the new scanner attribute display, so i moved it up<br>
hollowed and colorized the targeting buttons<br>
<br>
2025-02-04<br>
increased the size of the fuel, energy and heat bar to handle fuel up to 4400<br>
resized message box to not overlap with 2 rows of escorts<br>
restored the somehow missing tactical information display<br>
added "target nearest enemy" and "target nearest asteroid" buttons<br>
removed the color folders, white is enough<br>
<br>
2024-12-28<br>
moved the ammo box to the left side if the lower buttons<br>
added ship hud (inspired by Upmost Bsc | https://github.com/tobersj/Central-HUD)<br>
<br>
2024-11-20<br>
added small main menu button to the top left corner (requested by tarminu)<br>
<br>
2024-11-02<br>
removed hold fire button, because it's unsure when/if it comes back<br>
changed fast forward button back to small again, because it messed up the mission overview<br>
added 5 colour schemes(red, green, blue, purple, orange)
<br>
2024-10-29<br>
deactivated hold fire button, because it got removed in 0.10.10<br>
<br>
2024-10-11<br>
added fleet formations button<br>
<br>
2024-10-07<br>
added fleet hold fire button<br>
<br>
2024-09-06<br>
fine tuning for the graphics<br>
<br>
2024-09-02<br>
fixed button radius typo on fleet gather<br>
moved the fleet commands to the right side, so the jump systems are better seen<br>
<br>
2024-08-31<br>
changed button background to look more natural<br>
<br>
2024-08-30<br>
fixed an error<br>
adjusted positions<br>
added zoom buttons<br>
all buttons are visible now, but greyed out if you can't use them<br>
reworked all buttons to display a ring around them<br>
resized the fast forward button in the upper left corner, and added a greyed out version<br>
<br>
2024-08-25<br>
added a new panel for the fleet commands to the top center<br>
reworked the toggle ammo button<br>
removed the expandable radial menus, because all buttons are on the screen now<br>
exchanged some of the button positions<br>
<br>
2024-05-09<br>
initial release<br>
</blockquote>
</details>

Status: complete <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### Animated Ships


[Animated.Ships.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Animated.Ships.zip) | 30.3 mb | 2022-10-06 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Animated%20Ships/) <br>
Author: beccabunny | Category: Graphics <br>
[https://github.com/beccabunny/Animated-ships](https://github.com/beccabunny/Animated-ships) (last commit 2020-06-04) <br>

>Adds animations to many ships.
>



Status: N/A <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### Animated Stars


[Animated.Stars.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Animated.Stars.zip) | 1.54 mb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Animated%20Stars/) <br>
Author: Cat-Lady | Category: Graphics <br>
[https://github.com/Cat-Lady/animated-stars-nova](https://github.com/Cat-Lady/animated-stars-nova) (last commit 2019-11-17) <br>

>Replaces many stars with animated stars.
>



Status: N/A <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### Colorful Void Sprites


[Colorful.Void.Sprites.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Colorful.Void.Sprites.zip) | 4.28 kb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Colorful%20Void%20Sprites/) <br>
Author: Rob59er | Category: Graphics <br>
[https://github.com/Rob59er/Colorful-Void-Sprites](https://github.com/Rob59er/Colorful-Void-Sprites) (last commit 2021-02-21) <br>

>Makes Void Sprites colorful.
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote># Colorful-Void-Sprites
Adds colorful void sprites to Endless Sky

</blockquote>
</details>

Status: Playable on 0.9.14, 0.9.15 Continuous. <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### Dark Ships
<img src='../../Working/Dark Ships/icon.png' height='100'></img><br>


[Dark.Ships.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Dark.Ships.zip) | 8.73 mb | 2022-10-06 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Dark%20Ships/) <br>
Author: N/A | Category: Graphics <br>
N/A[]()  <br>

>This plugin contains ships rendered with a sharper illumination angle to get more dramatic shadows and less "flat" appearances.
>



Status: Should work <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### Different Galaxy Plugin


[Different.Galaxy.Plugin.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Different.Galaxy.Plugin.zip) | 12.36 mb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Different%20Galaxy%20Plugin/) <br>
Author: FranchuFranchu | Category: Graphics <br>
[https://github.com/FranchuFranchu/endless-sky-different-galaxy-plugin](https://github.com/FranchuFranchu/endless-sky-different-galaxy-plugin) (last commit 2021-03-02) <br>

>Changes the background galaxy image of Endless Sky to a nicer one.

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote>This Endless Sky plugin changes the galaxy image to an image of NGC 2336, which I think looks nicer.

Image by Judy Schmidt - NGC 2336, CC BY 2.0, https://commons.wikimedia.org/w/index.php?curid=93254431
</blockquote>
</details>

Status: N/A <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### easier harvesting


[easier.harvesting.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/easier.harvesting.zip) | 92.25 kb | 2022-10-06 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/easier%20harvesting/) <br>
Author: Endros Gunderberg | Category: Graphics <br>
[https://github.com/EndrosG/ES-Plugins](https://github.com/EndrosG/ES-Plugins) (last commit 2017-05-28) <br>

>This plugin provides easy to identify images which help you identifying minable asteroids.
>



Status: N/A <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### EndlessSky_ARUI
<img src='../../Working/EndlessSky_ARUI/icon.png' height='100'></img><br>


[EndlessSky_ARUI.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/EndlessSky_ARUI.zip) | 325.62 kb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/EndlessSky_ARUI/) <br>
Author: DrZingo | Category: Graphics <br>
[https://github.com/DrZingo/EndlessSky_ARUI](https://github.com/DrZingo/EndlessSky_ARUI) (last commit 2021-05-09) <br>

>A Reorganized User Interface for Endless Sky.
>
>This is a changed user interface when in space.
>
>Most important stuff (bars, weapons, hull/shield, target) is organized in top left corner by the radar.
>
>Destination is now to the right under world / date / money.
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote># A Reorganized User Interface for Endless Sky

This is a changed user interface when in space.

* Most important stuff (bars, weapons, hull/shield, target) is organized in top left corner by the radar.

* Destination is now to the right under world / date / money.

![screenshot](screenshot.png)

## Installation

Unpack or git clone repo into:

/.local/share/endless-sky/plugins/

</blockquote>
</details>

Status: N/A <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### ES Ships


[ES.Ships.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/ES.Ships.zip) | 8.06 mb | 2022-10-06 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/ES%20Ships/) <br>
Author: Yann | Category: Graphics <br>
N/A[]()  <br>

>Sprites with modified cockpit/bridge.
>



Status: Playable on 0.9.15 Continuous. <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### es-ui-upgrades
<img src='../../Working/es-ui-upgrades/icon.png' height='100'></img><br>


[es-ui-upgrades.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/es-ui-upgrades.zip) | 810.53 kb | 2024-11-01 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/es-ui-upgrades/) <br>
Author: lumbar527 | Category: Graphics <br>
[https://github.com/Cromha-Plugins/es-ui-upgrades](https://github.com/Cromha-Plugins/es-ui-upgrades) (last commit 2024-07-08) <br>

>Transforms the user interface by making it blue.
>



Status: Complete <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### High DPI
<img src='../../Working/High DPI/icon.png' height='100'></img><br>


[High.DPI.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/High.DPI.zip) | 749.12 mb | 2025-08-05 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/High%20DPI/) <br>
Author: Michael Zahniser (Maintained by the ES Community) | Category: Graphics <br>
[https://github.com/endless-sky/endless-sky-high-dpi](https://github.com/endless-sky/endless-sky-high-dpi) (last commit 2025-08-05) <br>

>Official High-DPI graphics for Endless Sky.
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote># endless-sky-high-dpi

This is a collection of double-resolution sprites for [Endless Sky](https://github.com/endless-sky/endless-sky). To make use of these sprites, copy this folder into one of the two [plugins folders](https://github.com/endless-sky/endless-sky/wiki/CreatingPlugins). These sprites will only be used if:

  * you have set the "zoom factor" to higher than 100% in the preferences, or
  * you have a high-DPI monitor.

High-DPI mode has only been tested on Mac OS X.

</blockquote>
</details>

Status: Playable on 0.9.14, 0.9.15 Continuous. <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### Human Steering Flares


[Human.Steering.Flares.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Human.Steering.Flares.zip) | 2.6 kb | 2022-10-06 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Human%20Steering%20Flares/) <br>
Author: Ferociousfeind | Category: Graphics <br>
N/A[]()  <br>

>Add steering flare to human ships.
>



Status: Playable on 0.9.14, 0.9.15 Continuous. <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### human.labels
<img src='../../Working/human.labels/icon.png' height='100'></img><br>


[human.labels.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/human.labels.zip) | 1.99 mb | 2025-06-21 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/human.labels/) <br>
Author: zuckung | Category: Graphics <br>
[https://github.com/zuckung/endless-sky-plugins](https://github.com/zuckung/endless-sky-plugins) (last commit 2025-06-21) <br>

>Reworks the Human area labels and adds area borders. See the README for details.
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote>### human.labels
<br>
<br>
Reworks the map labels and adds area borders. See the readme for details.<br>
<br>
The area labels are now smaller and better to see. Also there is a border drawn around each human area.<br>
On Earth's job board you can find a mission to change the color of the labels (light blue, light gray, yellow, dark red, green, dark gray, orange, purple).<br>
<br>
<br>
Changelog:<br>
<br>
2025-06-21<br>
added control.station support<br>
<br>
2025-06-05<br>
colored job<br>
<br>
2025-05-19<br>
icon@2x, plugintxt changes<br>
<br>
2025-02-13<br>
added @2x images<br>
added non-human labels<br>
<br>
2024-07-13<br>
corrected script error<br>
<br>
2024-07-09<br>
text correction<br>
<br>
2024-07-08<br>
added 4 more label colors to choose of (green, dark gray, orange, purple)<br>
<br>
2024-07-07<br>
added 3 more label colors to choose of (light blue, light gray, dark red)<br>
added job on Earth to change the label colors<br>
<br>
2024-06-26<br>
initial release<br>


</blockquote>
</details>

Status: complete <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### landing.images
<img src='../../Working/landing.images/icon.png' height='100'></img><br>


[landing.images.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/landing.images.zip) | 15.3 mb | 2024-10-06 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/landing.images/) <br>
Author: zuckung | Category: Graphics <br>
[https://github.com/zuckung/endless-sky-plugins](https://github.com/zuckung/endless-sky-plugins) (last commit 2024-10-06) <br>

>Replaces all planet landing images with better fitting ones. See the README for details.
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote>### landing.images
<br>
<br>
Replaces all planet landing images with better fitting ones.<br>
<br>
These images replace the boring vanilla images you see when you've landed on a planet with new, AI generated, better fitting ones. The old ones look like photos from earth or taken from public NASA archives(which they are). According to the description of the planets I tried to generate better fitting, more futuristic, more alien-looking images. And I think that went well :) <br>
0.10.8 with 472 planets<br>
See all images <a href='https://github.com/zuckung/endless-sky-plugins-graphics/blob/main/res/md/landing.images.md'>here</a>.<br>
<br>
<br>
Changelog:<br>
<br>
2024-10-06<br>
added 53 landing images for 0.10.9 update<br>
<br>
2024-07-31<br>
initial release<br>


</blockquote>
</details>

Status: complete <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### landing.images.android
<img src='../../Working/landing.images.android/icon.png' height='100'></img><br>


[landing.images.android.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/landing.images.android.zip) | 31.51 kb | 2024-08-17 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/landing.images.android/) <br>
Author: zuckung | Category: Graphics <br>
[https://github.com/zuckung/endless-sky-plugins](https://github.com/zuckung/endless-sky-plugins) (last commit 2024-08-09) <br>

>Moves the landing image above the textbox, instead of behind the textbox (for ES mobile). See the README for details.
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote>### landing.images.android 
<br>
<br>
Moves the landing image above the textbox, instead of behind the textbox (for ES mobile).<br>
<br>
In case parts of the UI/the buttons are outside the screen, try rescaling your UI in the ES options<br>
If that doesn't help, open the zip, edit 'landing.images.android/data/interface.txt' and change line 2 to 7 to:<br>
	image "land"
		center -60 -150
		dimensions 250 135
	sprite "ui/frame"
		center -60 -150
		dimensions 265 150
That resizes the landing image and the frame to their half.<br>
<br>
Before:<br>
<img src='https://raw.githubusercontent.com/zuckung/endless-sky-plugins/master/screenshots/landing.images.android01.jpg' width='400'>
<br>
After:<br>
<img src='https://raw.githubusercontent.com/zuckung/endless-sky-plugins/master/screenshots/landing.images.android02.jpg' width='400'>
<br>
<br>
Changelog:<br>
<br>
2024-08-09<br>
minor text changes (thx to TheGiraffe3)<br>
<br>
2024-08-07<br>
added a frame for the image<br>
finetuned position<br>
<br>
2024-08-03<br>
added hire all/fire all buttons which were missing (thx timeout.fu)<br>
added guide to resize the image (thx Pyrrha of simpleplanes)
<br>
2024-08-02<br>
initial release<br>


</blockquote>
</details>

Status: complete <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### landing.images.highres
<img src='../../Working/landing.images.highres/icon.png' height='100'></img><br>


[landing.images.highres.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/landing.images.highres.zip) | 67.11 mb | 2024-10-06 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/landing.images.highres/) <br>
Author: zuckung | Category: Graphics <br>
[https://github.com/zuckung/endless-sky-plugins](https://github.com/zuckung/endless-sky-plugins) (last commit 2024-10-06) <br>

>High resolution files for landing.images plugin. See the README for details.
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote>### landing.images.highres
<br>
<br>
High resolution files for landing.images plugin.<br>
<br>
Adds images with 1440x720 resolution. The landing.images plugin is still needed.<br>
<br>
<br>
Changelog:<br>
<br>
2024-10-06<br>
added 53 landing images for 0.10.9 update<br>
<br>
2024-08-09<br>
minor text changes (thx to TheGiraffe3)<br>
<br>
2024-08-02<br>
initial release<br>


</blockquote>
</details>

Status: complete <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### Low Quality


[Low.Quality.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Low.Quality.zip) | 359.6 kb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Low%20Quality/) <br>
Author: N/A | Category: Graphics <br>
N/A[]()  <br>

>replaces ship images with lows quality versions
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote>this is just a meme plugin for ESS to be used as a workshop example upon launch, however as so many people are excited to begin developing on it now, i guess i will allow it. 

</blockquote>
</details>

Status: N/A <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### New Galaxy
<img src='../../Working/New Galaxy/icon.png' height='100'></img><br>


[New.Galaxy.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/New.Galaxy.zip) | 7.28 mb | 2022-10-06 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/New%20Galaxy/) <br>
Author: Lia Gerty | Category: Graphics <br>
N/A[]()  <br>

>This is just a demonstration of the map image that would be used with an expanded core region.  Since it does not include the new systems that would be between Sagittarius A* and human space, Sagittarius A* will appear off centre.
>
>



Status: N/A <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### Outfit Highlighter
<img src='../../Working/Outfit Highlighter/icon.png' height='100'></img><br>


[Outfit.Highlighter.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Outfit.Highlighter.zip) | 445.75 kb | 2023-10-28 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Outfit%20Highlighter/) <br>
Author: MidnightPlugins | Category: Graphics <br>
[https://github.com/MidnightPlugins/Outfit-Highlighter](https://github.com/MidnightPlugins/Outfit-Highlighter) (last commit 2023-10-28) <br>

>Makes the selected outfit stand out more in the outfitter screen. Recommended for those who prefer to navigate the outfitter using the keyboard instead of the mouse.
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote># Outfit-Highlighter

Makes the selected outfit stand out more in the outfitter screen. Recommended for those who prefer to navigate the outfitter using the keyboard instead of the mouse.

![image][image]

[image]: icon.png

https://github.com/MidnightPlugins/Outfit-Highlighter

Now includes alternate themed highlighters! To change highlighters, copy the image file in the subfolder for your chosen theme and paste it into the ui folder of the Outfit Highlighter plugin. (Not the Endless Sky ui folder!)

Description of available themes:

- Alert (color): Four exclamation corner brackets and the grid in the chosen color
- Arrows (color): Four arrows in the corner set to the chosen color
- Cargo Pods: Frame made of Syndicate cargo pods
- Classic Highlighter: The original Outfit Highlighter
- Endless Sky Frames: Frame resembling Endless Sky's menu frames
- Fade to Black: A gray box that fades to black near the top
- Fade to (color): A box of the chosen color that fades to black near the top
- Fluffy Sales Clerks: Two Subsidurials help you shop for outfits
- Hai: Frame made of Hai ship parts
- Mereti: Frame made of Mereti ship parts
- Ringworld: Frame made of Ringworld parts
- Sheragi: Frame made of Sheragi ship parts
- Vanilla Enhanced: Just a slightly bigger vanilla highlighter
- Wanderer: Frame made of Wanderer ship parts

</blockquote>
</details>

Status: N/A <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### Pi game mods


[Pi.game.mods.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Pi.game.mods.zip) | 158.06 kb | 2022-11-09 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Pi%20game%20mods/) <br>
Author: Pilover100 | Category: Graphics <br>
N/A[]()  <br>

>Pilover100's personal modifications. (Change UI colors to make things more visible. Alternate Wanderer Reactor graphic.)
>



Status: Playable on 0.9.15/0.9.16. <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### Pug-Hud
<img src='../../Working/Pug-Hud/icon.png' height='100'></img><br>


[Pug-Hud.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Pug-Hud.zip) | 458.21 kb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Pug-Hud/) <br>
Author: comnom | Category: Graphics <br>
N/A[]()  <br>

>adds a HUD
>



Status: N/A <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### Rainbow Pleiades


[Rainbow.Pleiades.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Rainbow.Pleiades.zip) | 139.64 kb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Rainbow%20Pleiades/) <br>
Author: RestingImmortal | Category: Graphics <br>
[https://github.com/RestingImmortal/misc-plugins](https://github.com/RestingImmortal/misc-plugins) (last commit 2019-09-03) <br>

>Turns the galaxy sprite for the pug empty galaxy into a rainbow.

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote>### Rainbow Pleiades
Turns the galaxy sprite for the pug empty galaxy into a rainbow.

</blockquote>
</details>

Status: Abandoned <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### Realistic Solar System


[Realistic.Solar.System.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Realistic.Solar.System.zip) | 9.06 mb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Realistic%20Solar%20System/) <br>
Author: beccabunny | Category: Graphics <br>
[https://github.com/beccabunny/Realistic-Solar-System](https://github.com/beccabunny/Realistic-Solar-System) (last commit 2020-08-11) <br>

>This plugin modifies the Sol system adding every planet, large moon (over 20!) and two dwarf planets (Ceres and Pluto with its moon, Charon), each with unique sprites modified from NASA pictures taken during various missions. Everything in Sol has also been resized to a much bigger and realistic size, including the Sun itself.
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote># Realistic-Solar-System
This plugin modifies the Sol system adding every planet, large moon (over 20!) and two dwarf planets (Ceres and Pluto with its moon, Charon), each with unique sprites modified from NASA pictures taken during various missions. Everything in Sol has also been resized to a much bigger and realistic size, including the Sun itself.

In vanilla, the solar system has:
 - 5 planets
 - 5 moons
 - a 90x90 star

With this plugin, it gets:
- 8 planets
- 20 moons
- 2 dwarf planets
- a 450x450 star

And all of this with 31 unique sprites, plus other 30 high DPI ones included in the package!

</blockquote>
</details>

Status: N/A <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### Resized Endless Sky


[Resized.Endless.Sky.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Resized.Endless.Sky.zip) | 3.26 mb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Resized%20Endless%20Sky/) <br>
Author: FranchuFranchu | Category: Graphics <br>
[https://github.com/FranchuFranchu/resized-endless-sky](https://github.com/FranchuFranchu/resized-endless-sky) (last commit 2021-03-02) <br>

>Resizes the Endless Sky galaxy. 



Status: WIP <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### Restock


[Restock.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Restock.zip) | 9.68 mb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Restock/) <br>
Author: beccabunny | Category: Graphics <br>
[https://github.com/beccabunny/ES-Restock](https://github.com/beccabunny/ES-Restock) (last commit 2020-12-29) <br>

>A visual mod that improves the look of many vanilla human outfits, either greatly detailing the original model or using a completely new one. Currently including 109 new sprites!
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote># ES-Restock
A visual mod that improves the look of many vanilla human outfits, either greatly detailing the original model or using a completely new one. Currently including 109 new sprites!


</blockquote>
</details>

Status: N/A <br>
Daily update check: <img src='../img/check.png' width='15' ></img><br>


---

### swiftclaws.additional.command.buttons
<img src='../../Working/swiftclaws.additional.command.buttons/icon.png' height='100'></img><br>


[swiftclaws.additional.command.buttons.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/swiftclaws.additional.command.buttons.zip) | 389.02 kb | 2023-09-25 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/swiftclaws.additional.command.buttons/) <br>
Author: swiftclaw | Category: Graphics <br>
[https://drive.google.com/file/d/17RstjG7nxM0KzhfwpVh50NrgCO9cQ375/view](https://drive.google.com/file/d/17RstjG7nxM0KzhfwpVh50NrgCO9cQ375/view)  <br>

>Modified version of additional.command.buttons plugin
>
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote>### swiftclaws.additional.command.buttons <br>
<br>
<img src='https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/swiftclaws.additional.command.buttons/screenshot.jpg' width='400'>

</blockquote>
</details>

Status: tested with 0.10.2 <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### Swizzle Player


[Swizzle.Player.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Swizzle.Player.zip) | 48.53 kb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Swizzle%20Player/) <br>
Author: Cat-Lady | Category: Graphics <br>
[https://github.com/Cat-Lady/swizzle-player/releases](https://github.com/Cat-Lady/swizzle-player/releases) (last commit 2019-11-02) <br>

>This is a small plugin that allow to change player's swizzle in "Endless Sky" - and keep the colour after ES get updates that change goverments.txt data file.
>
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote>This is a small plugin that allow to change player's swizzle in "Endless Sky" - and keep the colour after ES get updates that change goverments.txt data file.


[h1]Installing[/h1]

Check:
https://github.com/Cat-Lady/swizzle-player/releases

...for latest, pre-packaged version.


[b]1.[/b] Unpack [i]swizzle-player[/i] to your ES plugins folder. Be sure that you have single [i]swizzle-player[/i] directory inside your plugins folder, containing [i]data[/i] folder. Directory structure should look like:

[code](...)/plugins/swizzle-player/(.../data/, /images/ and other stuff)[/code]

It [b]won't[/b] work if the directory structure will be anything like:

[code](...)/plugins/swizzle-player/swizzle-player/(...)[/code]



[h1]Author[/h1]

[list][*][b]Cat Lady[/b][/list]



[h1]License[/h1]

This project is licensed under the GPL3 License - see the LICENSE.md file for details.



[h1]Acknowledgments[/h1]

"Endless Sky" Development Team and Michael Zahniser; For maintaining and creating the game

[url=https://github.com/EndlessSkyCommunity/EndlessSky-Discord-Bot]James the Bot[/url] from "endless Sky" discord forum; For easy way to check swizzle numbers, the bazzilion times I needed to do it in the past.

Iggy Pop for singing "She want's to be your James Bot" (and don't even try to convince me that he meant something else).
</blockquote>
</details>

Status: N/A <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>


---

### Wanderer Suns
<img src='../../Working/Wanderer Suns/icon.png' height='100'></img><br>


[Wanderer.Suns.zip](https://github.com/Hecter94/EndlessSky-PluginArchive/releases/download/Latest/Wanderer.Suns.zip) | 285.29 kb | 2023-07-27 | [view files](https://github.com/Hecter94/EndlessSky-PluginArchive/tree/main/Working/Wanderer%20Suns/) <br>
Author: Gefüllte Taubenbrust | Category: Graphics <br>
[https://github.com/GefullteTaubenbrust2/Wanderer-Suns](https://github.com/GefullteTaubenbrust2/Wanderer-Suns) (last commit 2022-05-15) <br>

>This plugin changes the models of the Wanderer "Sun" reactors so that a sort of "sun" can actually be seen in them.
>

<details>
<summary>:blue_book: Plugin readme</summary>
<blockquote># Wanderer-Suns
This is a plugin for Endless Sky that changes to Wanderer reactors so they actually show small "suns" within them.

</blockquote>
</details>

Status: N/A <br>
Daily update check: <img src='../img/cross.png' width='15' ></img><br>



[back to top](https://github.com/Hecter94/EndlessSky-PluginArchive/blob/main/res/mds/graphics.md#graphics)


