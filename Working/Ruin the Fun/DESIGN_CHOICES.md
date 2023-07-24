Design Choices
==============

This document explains choices made in the design of this plugin.



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
