<p align=center><img src="https://github.com/OcelotWalrus/Cromha-Expansion-plugin/assets/87318892/0210316e-92d1-4d32-ae96-b95cf7466fea" alt="https://github.com/OcelotWalrus/Cromha-Expansion-plugin/assets/87318892/0210316e-92d1-4d32-ae96-b95cf7466fea" /></p>

<h1><p align=center>Endless Sky Plugin:<br />Cromha-Expansion</p></h1>

[![CD](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/actions/workflows/cd.yaml/badge.svg?branch=main)](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/actions/workflows/cd.yaml)
[![Submodule Updates](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/actions/workflows/sub-modules-update.yaml/badge.svg?branch=main)](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/actions/workflows/sub-modules-update.yaml)
[![Codespaces Prebuilds](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/actions/workflows/codespaces/create_codespaces_prebuilds/badge.svg)](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/actions/workflows/codespaces/create_codespaces_prebuilds)

## 

This is a plugin for the free, open-source game [Endless Sky][es]. This plugin
is developed and tested against the [Endless Sky continuous][continuous] build.
Learn more [about Endless Sky][esweb].
**You can join the discord server [here](https://discord.gg/tafa8dVH5Q)** if you want to discuss about the plugin or ask more in depth questions to me.


<details>

  <summary>Summary</summary>

* [About plugin](#about-plugin)
    * [This plugin](#this-plugin)
* [Contributing](#contributing)
* [Development status](#development-status)
* [System Requirements](#system-requirements)
  * [Known Issues](#known-issues)
* [Installation](#installation)
    * [Install steps](#install-steps)
    * [Keeping the plugin updated](#keeping-the-plugin-updated)
* [Special Thanks](#special-thanks)

</details>

# About Plugin:

Adds a new civilization to the Korath Space (now named the '[Empire Space](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Regions-of-the-galaxy#the-empire-space)': [The Cromha Empire](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Cromha-Empire). Also known as 'The Empire', it is a government that dirige a huge part of the north of the Milky Way. It also a very high advanced government. They are human but don't directly have contact with human Merchants, they have contact with the Syndicate, the Republic but they don't allow them to enter their territory. Know more about the plugin in the [wiki](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki)! (or test the game yourself) Also, there is another empire that is set up next to the Paradise Planets. It is called the [Lumbarian Empire](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Lumbarian-Empire).
**Please do not use this plugin with your existing saves! This plugin is highly beta and it could corrupt your saves or make them unusable!**

## This plugin:

* Adds governments that are related to the vanilla storyline (kind of).
* Expand various civilizations:
  * Quarg
  * Drak
  * Pug
  * Remnant
  * Ka'Het
  * Kor Automatons (Kor Mereti and Kor Sestor)
  * Korath
* The Lumbarian Empire that wants to replace the Republic and the Free Worlds and the Syndicate
* The storyline that the plugin adds is made so it is the most similar possible to the vanilla one.
* Add new outfits and ships from different governments.
* Expands upon the existing map for exploration (New Systems in the north of the galaxy and near the Deep Space).
* Adds a new galaxy where there is Sheragi is but it is still in work.

# Contributing

All Contributions are welcome!

_Check the [Contributing Guide](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Contributor-Guide) before creating any issue or pull request._

To contribute to the plugin, you can create [issues](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/issues) to describe an error from spelling errors to mission bug or anything else.
You can also create an [issue](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/issues) or a [pull request](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/pulls) to request specific feature.

# Development Status
It is currently a Beta plugin.

* A medium WIP (work in progress) plugin
* Story is not fully implemented but for most of the part, it is
* Spaceport and planets descriptions are not fully done
* Quarg-Pug Expansion not finished
* Ember Watse/Remnant/Dark Expansion not finished
* Many more civilizations expansions to do
* Outfits and ships descriptions are not fully done.
* The whole 'Empire Rebels' part is not started very yet. (check [wiki](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Governments-&-Major-Factions))
* The [wiki](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/) still in work and most of the Gameplay section is outdated
* The Lumbarian Empire is currently in a very early stage. Help create the storyline [here](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/discussions/117)

# System requirements
Endless Sky has very minimal system requirements, meaning most systems should be able to run the game. But this plugin is kind of heavy.
It is also important that you play using the **latest unstable beta version of Endless Sky**, the main branch of the official [Endless Sky repository](https://github.com/endless-sky/endless-sky).

|| Minimum | Recommended |
|---|----:|----:|
|RAM | 4 MB | 8 GB |
|Graphics | OpenGL 3.0 | OpenGL 3.3 |
|Storage Free | 900 MB | 3 GB |

## Known issues
  * Game sometimes crash when loading resources (don't have enough RAM)
  * Some outfits or ships don't have texture: it's because we're currently revamping them (the textures to be revamped are in [images/_TEMP/](https://github.com/Cromha-Plugins/Cromha-Expansion-plugin/tree/main/images/_TEMP))

# Installation
If you're new in the Endless Sky community, check the [User Guide](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/User-Guide) to learn the basics!

## Install steps

To install the plugin you just have to clone this repository into your [endless sky plugin directory](https://github.com/endless-sky/endless-sky/wiki/CreatingPlugins).
You can use the following command if you're used to command line.

```
git clone https://github.com/OcelotWalrus/Cromha-Expansion-plugin.git
```

If you want the `sources/` directory (a directory for the plugin assets like `.blend` files or `.xcf` for contributor), run the following command to enable sub-modules:

```
git clone https://github.com/OcelotWalrus/Cromha-Expansion-plugin.git --recursive
```

 If not, you can download the [continuous build](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/releases/tag/9.9.9-continuous) and put the folder into your [endless sky plugin directory](https://github.com/endless-sky/endless-sky/wiki/CreatingPlugins).

## Keeping the plugin updated
If you're not familiar with git, you just have to run that command into the installed plugin.

```
git pull
```

If it don't work, you can just re-download the plugin at [releases](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/releases) and put it in your [endless sky plugin directory](https://github.com/endless-sky/endless-sky/wiki/CreatingPlugins). And make sure you deleted the old Cromha Expansion plugin folder.

## Special thanks

Check [copyright.txt](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/blob/main/copyright.txt) for full credits.
I have several people that really needs credits for my work here, first because some of them helped me but also some of them did great work on the endless sky community:

  * [`@lumbar527`](https://github.com/lumbar527)
    * He helped me by a lot on the plugin and had a lot of great ideas.
  * [`@1010todd`](https://github.com/1010todd)
    * This guys is an insane plugin creator who made tons of great assets, plugins and also have insane ideas. Lot of ideas from this project originally come from some of his work. You can check his plugins [here](https://github.com/endless-sky/endless-sky/discussions/7928). Respect to this guy.
  * [`@MidnightPlugins`](https://github.com/MidnightPlugins)
    * He made great plugins with great ideas that have have to me other great ideas.


[es]: https://github.com/endless-sky/endless-sky
[continuous]: https://github.com/endless-sky/endless-sky/releases/tag/continuous
[esweb]: https://endless-sky.github.io/
