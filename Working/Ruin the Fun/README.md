# es-ruin-the-fun

Cheat plugin for [endless-sky](https://github.com/endless-sky/endless-sky), to ruin your fun, or to assist you in making or testing another plugin.

Ruin-The-Fun lets you change your captain's name, choose the color swizzle of your ships, edit your relation with other governments, set your combat rank, hire a powerful escort, gift yourself pre-outfitted ships, give yourself money, and much more. It also makes all ships and outfits available from a few added systems.



# Startup

This assumes you have installed and enabled the plugin. If not, see [Install Instructions](#install-instructions).

**Be advised against using this plugin with your favorite pilot's save**, since it will make your hours of labor nonsensical.
If you want to use this plugin for an existing save anyway, then **MAKE A BACKUP OF YOUR PILOT** (for instance with the `Add snapshot` button).

![new pilot menu](./images/screenshot/add-snapshot.png)

If your intent is rather to use this plugin with a new pilot, you may use one of the starts provided by this plugin to do so:

![new pilot menu](./images/screenshot/rtf-starts.png)
You will spawn in an RTF system, from which cheat features are available.

Cheat features are available from, and only from, the RTF systems. One of them has an hyperlink to `Rutilicus` (the default start system), so that you can reach it with an Hyperdrive:

![new pilot menu](./images/screenshot/rtf0-on-map.png)

There is other RTF systems everywhere on the map, so you do not have to cross it whole.

![new pilot menu](./images/screenshot/rtf-systems-on-map.png)



# Spaceport

![Spaceport](./images/screenshot/spaceport-button.png)

Click the `Spaceport` button to access a number of quick actions.
More actions are available from the `Job Board`.



# Job Board

![Job Board](./images/screenshot/job-board-button.png)

The `Job Board` contains most of this plugin's features.

The following jobs can be used after every landing on an RTF planet:
- `All Useful Things`: Get money, reveal the map, and earn combat rank 14.
- `Escort: * Barges` (3 variants): Get escorted by dreadful Star Barges.
- `Escort: Tek Far 109`: Get escorted by a customized drone transporter.
- `Fight Combat Drones`: Summon an amount of hostile Combat Drones.
- `Fight Kestrels`: Summon a combination of hostile Kestrels.
- `Fight Tek Far 109`: Summon an hostile customized drone transporter.
- `Fleets: Heliarchs vs Quargs`: Adds Heliarch and Quarg fleets to RTF0.
- `Fleets: Meretis vs Sestors`: Adds Mereti and Sestor fleets to RTF0.
- `Fleets: Scin vs Vis`: Adds Scin and Vi fleets to RTF0.
- `Free Money`: Obtain 1B credits.
- `Name`: Change your captain's name.
- `Rank`: Set your combat rank. Optionally spawn a target in space, to get xp from.
- `Reputations`: Change your reputation with other governments.
- `Reputations`: Customize your reputation per government, or turn everyone friendly or hostile, or, reset reputations to default.
- `Reveal Planet Infos`: Reveal all vanilla planets information (upon take of, does not reveal systems).
- `Reveal Systems`: Reveal the whole system map (upon take of).
- `Swizzle`: Change the color of your ships.
- `Vanilla Events And Conditions`: Let you edit a few vanilla conditions.

The following jobs are toggles, their effect is reverted when you abort them:
- `Hide RTF Systems`: Hide the RTF systems, so that they do not interfere.
- `Super Reach`: While in an RTF system, you can jump to any system on the map, even without a God Drive. By default, RTF systems have a lower jump range, to lower their impact on surrounding content.



# Shipyard

![Shipyard](./images/screenshot/shipyard-button.png)

From the RFT shipyards, all ships in the game are available to you.



# Outfitter

![Outfitter](./images/screenshot/outfitter-button.png)

From the RFT outfitters, all outfits in the game are available to you.

RTF also adds a few outfits, all listed under the `Special` category:
- `God Drive`: Jump drive, with no range limit, that does not consume fuel.
- `God Mode`: Makes you immortal.
- `God Turret`: Turret that one-shot most ships.
- `100000 Outfit Space`: Gives you more than enough outfit space.
- `100000 Cargo Space`: Gives you so much cargo space that this will trigger pirate raids.
- (property name): Change individual stats of a ship. They look like this:
![Outfitter](./images/screenshot/wheel-examples.png)



# Assets (placeholders)

You can use those assets as placeholders:
 - [Outfits](./images/outfit/rtf/)
 - [Sounds](./sounds/)

If needed, info about individual assets are available from [./copyright](./copyright).



# Install Instructions

This plugin was last made for endless-sky `v0.10.2`, but is likely to include later content.

To install this plugin, put it as a folder (not an archive/zip file) inside the `plugins` folder.
The `plugins` folder should be located at one of those locations:
- On Windows:
  - `plugins\ (in the same folder as the Endless Sky executable)`
  - or `C:\Users\yourusername\AppData\Roaming\endless-sky\plugins\`
- On Linux:
  - `/usr/share/games/endless-sky/plugins/`
  - or `~/.local/share/endless-sky/plugins/`
- On Mac:
  - `Contents/Resources/plugins/ (within the application bundle)`
  - or `~/Library/Application Support/endless-sky/plugins`

If the `plugins` folder does not exist, create it.

## Plugin Conflicts
All the content added by this plugin is prefixed, to avoid conflicts with other plugins.

## Updating Content
You can **update the plugin's vanilla content** by running the following command inside the plugin's directory:
> make update

You may have to set the path to the Endless Sky `data` folder as instructed.

You can **include content from other plugins** by running the following command inside the plugin's directory:
> make plugin-update

This will only work if all plugins, including RTF, are in the same `plugins` folder.



# Bugs / Suggestions

Please submit bug reports or suggestions using [GitHub issues](https://github.com/Pshy0/es-ruin-the-fun/issues).



# License

 > This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
 > This Source Code Form is “Incompatible With Secondary Licenses”, as defined by the Mozilla Public License, v. 2.0.
