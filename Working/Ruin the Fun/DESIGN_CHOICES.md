Design Choices
==============

This document explains choices made in the design of this plugin.

I may also use it as a reference for other plugins.



## Placing assets in `rtf/` folders

Resources from different plugins may collide.
To prevent this, all resources are located within a `rtf` subfolder.

There is already a standard hierarchy for assets folders.
In the case of ship sprites, images must be within `images/ship/` for their hitbox to be generated.

For this reason, the `rtf/` folder is located after the standard path but before the resources.
For instance:
- `images/ship/rtf/ship-sprite.jpg`
- `images/outfit/rtf/outfit-sprite.jpg`
- `images/outfit/rtf/cube/outfit-sprite.jpg`
- `sounds/rtf/sound-file.mp3`
- `sounds/ambient/rtf/sound-file.mp3`



## Using a plugin prefix, without colons

The plugin prefix lowers the chances of collision with content from other plugins.
I used to separate the plugin prefix and the object name with a colon, but this had the following inconveniences:
- Some object types does not have a "display name" property yet. In this case, the colon causes additional issues:
  - Takes more space over the UI... And the colon is ugly.
  - Harder to do searches in the UI (using the in-game CTRL+F shortcut on the map, ship list, or outfit list).
- Not standardized across the plugin, causing confusion with some names.

This is why there is no colon after the namespace.

In `es-ruin-the-fun`, the prefix is `Ruin-The-Fun` to be more explicit, but also sometimes `RTF` when it's more convenient, so that some object types without a "display name" are still decently rendered. It would look like this:
- `Ruin-The-Fun Object Name: Subobject Name`
- `RTF Object Name: Subobject Name`
