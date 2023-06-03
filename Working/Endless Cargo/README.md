# Endless Cargo

## What is it?

It's a plugin/mod for [Endless Sky](http://endless-sky.github.io) which attempts to add shipping containers and container ships to the game.

## How do I install it?

[Download the ZIP file](https://bitbucket.org/YellowApple/endless-cargo/downloads/) and extract it into your plugins folder.  Alternately, you can just `git clone` directly into the plugins folder (e.g. `git clone https://bitbucket.org/YellowApple/endless-cargo.git ~/.local/share/endless-sky/plugins/endless-cargo`).

## How does it work?

The current plan is to implement a shipping container as a sort of unarmed, ~~unpropelled~~ (HAHA, turns out at least *some* propulsion is needed for them to redock if you release them) drone, and in turn to implement a container ship as a sort of drone carrier.  This means that drones and shipping containers are interchangeable.

At this time, one type of container (a generic "Cargo Container") and two container ships (the Star Barge and Freighter without the welded-in containers and with drone bays for one's own containers) are implemented.  There's also a test mission out of Greenrock to haul an empty container to a nearby factory world (like New Britain or Luna), which I plan to flesh out and turn into more missions for more planets (including with specialized container types).  Most (if not all) factory worlds in human space sell containers, and the Container Barge and Container Freighter are available from any "Syndicate Basics" shipyard (and the former from any "Basic Ships" shipyard, so you can grab a Container Barge as your first ship right out of New Boston).

In the distant future, I might opt to attempt to implement containers as their own ship class, or perhaps as something that's not necessarily a "ship" per se.  This would require submitting this as a part of the vanilla game, though; while I think this idea is pretty cool, I'm also fully aware that's it's a *very* niche mod that probably doesn't belong in the core game, in which case - unless the core game opens up the ability to easily define new ship classes - the drone-container approach is probably the best I can do for the time being.

## What kinds of shipping containers will be implemented?

The average container (that is, the kind you'd actually want to buy at a shipyard) would have very little besides a few tons of cargo space and perhaps a smidge of outfit space.  A container ship would in turn have very little cargo or passenger space on its own, but could instead fill itself with shipping containers.

Once the basic shipping mechanics are implemented (namely, a basic container and a basic container ship), I'll likely delve into some missions involving specialized container types.  Some examples:

- Transport 5 containers carrying helicopters to Vail
- Haul 35 families and their prefabricated homes to a trailer park on New Boston
- Deliver 25 mining excavators and 5 portable field offices to a mining operation on Bounty
- etc.

Whether or not these specialized containers are something which you could buy in a shipyard is TBD.  There'd probably be no point to it, though I'm not one to stop someone from wasting money (especially if it's for roleplaying purposes or perhaps to resell somewhere else).

## Ain't this the same thing the Boxwing already does?

Kinda.  Containers are basically the drone version of the Boxwing.  Notable differences:

* Containers are drones, and thus don't require crew
* Containers are drones, and thus take up drone slots instead of fighter slots
* Containers are meant to make Boxwings look like Flivvers in comparison
* Containers have a fraction of the Boxwing's cargo space (currently 25%; I might bump that to 50% once I'm ready to actually dive into balancing)

Additionally, this plugin will feature actual missions/jobs/etc. revolving around container delivery, so it's certainly not limited to just adding a bunch of ships.

## Any gotchas?

* Containers deploy alongside the rest of your fighters and drones, so keep that in mind when you're in the heat of battle.
* Containers added by a container-hauling mission launch separately from your container ship, even if your own fighters/drones/containers are already docked.  This applies to all launches (haven't tested with wormholes yet).  Be sure to wait for your mission-added containers to redock between takeoff and jumping.
* Container-hauling missions currently don't have any multiplier for the number of containers or the distance involved.  [A bug/enhancement report has already been filed to hopefully rectify this.](https://github.com/endless-sky/endless-sky/issues/2569)

## What's the license?

GPLv3, with some CC-BY-SA-4.0 artistic assets.