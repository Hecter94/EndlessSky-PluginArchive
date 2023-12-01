#!/bin/bash
declare -A plugins
plugins[Aben]=https://github.com/Adde-Endless-Sky/Aben
plugins[Adamas Project]=https://github.com/kestrel1110/Adamas-Project
plugins[Amphibious Ships]=https://github.com/AvianGeneticist/Amphibious-Ships
plugins[Arion]=https://github.com/Spectre907YT/Endless-Sky---Arion
plugins[Beyond the Sky]=https://github.com/1010todd/Beyond-the-Sky
plugins[Blended Ships]=https://github.com/mOctave/blended-ships
plugins[BSRC]=https://github.com/phenix2/BSRC
plugins[Celestial Strands]=https://github.com/Saugia/celestial-strands
plugins[Chroma Expansion]=https://github.com/OcelotWalrus/Cromha-Expansion-plugin
plugins[Czartraks Ship Pack]=https://github.com/czartrak/Czartraks-Ship-Pack
plugins[Derogam]=https://github.com/Lorantine/derogam
plugins[ES Galactic Exploration]=https://github.com/lumbar527/ES-Galactic-Exploration
plugins[Eternals]=https://github.com/comnom/Eternals
plugins[Fighter Factory]=https://github.com/1010todd/Fighter-Factory
plugins[Fire Corporation Plugin]=https://github.com/lumbar527/Fire-Corporation
plugins[Fluff]=https://github.com/Adde-Endless-Sky-Mods/Fluff
plugins[Galactic War]=https://github.com/1010todd/Galactic-War
plugins[Galaxias]=https://github.com/mdpiper/galaxias
plugins[Gander]=https://github.com/williaji/Gander
plugins[Haulers Expansion]=https://github.com/JPG7D/Haulers-Expansion-v2
plugins[Irm]=https://github.com/Adde-Endless-Sky-Mods/Irm
plugins[Kinetic Weaponry]=https://github.com/kestrel1110/KineticWeaponry
plugins[Kor Fighter Additions]=https://github.com/EjoThims/Kor-Fighter-Additions
plugins[Legendary Pirates]=https://github.com/Galaucus/Endless-Sky-Legendary-Pirates
plugins[Levis Customs]=https://github.com/AvianGeneticist/Levi-s-Customs
plugins[Lost in Midnight]=https://github.com/MidnightPlugins/Lost-in-Midnight
plugins[Mega Freight]=https://github.com/1010todd/Mega-Freight
plugins[Mata]=https://github.com/Karirawri/Mata
plugins[Midnight Expansion]=https://github.com/MidnightPlugins/Midnight-Expansion
plugins[Midnight Scrapyard]=https://github.com/MidnightPlugins/Midnight-Scrapyard
plugins[Mining Pinger]=https://github.com/AvianGeneticist/MiningPinger
plugins[sensor]=https://github.com/orbitalsupershell/sensor/
plugins[Sestor Expansion]=https://github.com/AvianGeneticist/Sestor-Expansion
plugins[Sheragi Rebirth]=https://github.com/Petersupes/sheragi-rebirth
plugins[Spinaleviathan]=https://github.com/AvianGeneticist/Spinaleviathan
plugins[The Enclave]=https://github.com/1010todd/The-Enclave
plugins[The Peacebringer]=https://github.com/Polaria1/The-Peacebringer
plugins[Unfettered Innovations]=https://github.com/Hurleveur/unfettered-innovations

pushd ../../plugins > /dev/null
for plugin_name in "${!plugins[@]}"
do
	if [ -d "$plugin_name" ]; then
		echo "Updating $plugin_name..."
		git -C "$plugin_name" pull
	else
		echo "Installing $plugin_name..."
		git clone --depth 1 "${plugins[$plugin_name]}" "$plugin_name"
	fi
done
popd > /dev/null
