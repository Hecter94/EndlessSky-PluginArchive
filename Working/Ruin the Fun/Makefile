# Endless Sky's data folder:
ES_DATA = ~/projects/endless-sky/data/
# Enable this line if you are using the main game's plugins directory:
#ES_DATA = ../../data

# Default Pilot save, used to generate some stuff.
# DO NOT CHANGE THIS TO YOUR PILOT NAME. Create that pilot instead.
ES_DEFAULT_PILOT_SAVE = "../../saves/Default Pilot"

# List of files to be generated (recipes defined bellow):
GENERATED_DATA_FILES += data/outfitters/all-outfits.txt
GENERATED_DATA_FILES += data/shipyards/all-base-ships.txt
GENERATED_DATA_FILES += data/shipyards/all-ship-variants.txt
GENERATED_DATA_FILES += data/map/planets.txt
GENERATED_DATA_FILES += data/map/systems.txt
RTF_JOB_FILES += data/jobs/reputation.txt
RTF_JOB_FILES += data/jobs/conditions/conditions.txt
RTF_JOB_FILES += data/jobs/combat-ships/combat-ships.txt
RTF_JOB_FILES += data/jobs/combat-fleets/combat-fleets.txt
RTF_JOB_FILES += data/jobs/escort-ships/escort-ships.txt
RTF_JOB_FILES += data/jobs/escort-fleets/escort-fleets.txt
RTF_JOB_FILES += data/jobs/visit-systems.txt
RTF_JOB_FILES += data/jobs/visit-planets.txt
GENERATED_DATA_FILES += $(RTF_JOB_FILES)
GENERATED_DATA_FILES += data/events/all-licenses.txt
GENERATED_DATA_FILES += data/plugin-support/all-outfitters.txt
GENERATED_DATA_FILES += data/plugin-support/all-shipyards.txt

# List of files that must be included in the plugin's zip
# This may not exactly match .gitignore
PLUGIN_FILES += about.txt
PLUGIN_FILES += copyright
PLUGIN_FILES += $(shell find data/ -type f -name '*.txt')
PLUGIN_FILES += icon.png
PLUGIN_FILES += images/hardpoint
PLUGIN_FILES += images/icon
PLUGIN_FILES += images/outfit
PLUGIN_FILES += images/projectile
PLUGIN_FILES += LICENSE
PLUGIN_FILES += plugin.txt
PLUGIN_FILES += README.md



.PHONY: update 
update: $(GENERATED_DATA_FILES)

$(ES_DATA):
	@printf "\e[31mERROR: The endless-sky data folder, configured in the Makefile, does not exist.\e[0m\n"
	return 2

$(ES_DEFAULT_PILOT_SAVE):
	@printf "\e[31mERROR: Please create a pilot called 'Default Pilot', with only the wished plugins enabled.\e[0m\n"
	return 2

tmp:
	@mkdir -p tmp

tmp/data-dirs.tmp: | tmp $(ES_DATA)
	@echo "Overriding data sources..."
	@echo $(ES_DATA) > $@
	@echo "Sources used:"
	@cat $@

tmp/available-plugin-data-dirs.tmp: | tmp
	@echo "Overriding available plugin data sources..."
	@tools/ls-data-plugins.sh | sed 's|^\(.*\)$$|"../../plugins/\1/data/"|' > $@
	@echo "Available plugin sources:"
	@cat $@

tmp/all-data-dirs.tmp: tmp/data-dirs.tmp tmp/available-plugin-data-dirs.tmp | tmp
	@echo "Overriding extended data sources..."
	@cat tmp/data-dirs.tmp tmp/available-plugin-data-dirs.tmp | sort | uniq > $@
	@echo "Extended sources used:"
	@cat $@

tmp/enabled-plugins.tmp: ../../plugins.txt | tmp
	@echo "Updating enabled plugin list..."
	@cat $< | grep " 1$$" | sed "s/ 1$$//" | sed 's/^[[:space:]]*//' > $@

tmp/available-plugins.list.tmp: | tmp
	@echo "Updating available plugin list..."
	@tools/ls-data-plugins.sh > $@

.PHONY: plugin-update
plugin-update: tmp/enabled-plugins.tmp tmp/data-dirs.tmp
	@echo "Inserting enabled plugin list into data sources..."
	@cat $< | sed "s/^/..\/..\/plugins\//" | sed "/ruin-the-fun/d" | sed "s/$$/\/data\//" >> tmp/data-dirs.tmp
	@make update

.PHONY: install-supported-plugins
install-supported-plugins: tools/install-supported-plugins.sh
	@tools/install-supported-plugins.sh

tmp/re.tmp: | tmp
	@touch $@

tmp/deprecated-outfits.list.tmp: tmp/data-dirs.tmp
	@echo "Listing deprecated outfits..."
	@cat tmp/data-dirs.tmp | sed "s|$$|_deprecated/|" | xargs grep -R "^outfit " | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:outfit //" | tools/unquote.sh | sort | uniq > $@

tmp/deprecated-ships.list.tmp: tmp/data-dirs.tmp
	@echo "Listing deprecated ship..."
	@cat tmp/data-dirs.tmp | sed "s|$$|_deprecated/|" | xargs grep -R "^ship " | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:ship //" | tools/unquote-ship.sh | sort | uniq > $@

tmp/outfits.list.tmp: tmp/data-dirs.tmp tmp/deprecated-outfits.list.tmp | tmp
	@echo "Listing outfits..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^outfit " | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:outfit //" | tools/unquote.sh | sort | uniq > tmp/tmp.list.tmp
	@comm -23 tmp/tmp.list.tmp tmp/deprecated-outfits.list.tmp > $@

tmp/ship-lines.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Finding ship definitions..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^ship " | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:ship //" | sort | uniq > $@

tmp/base-ships.list.tmp: tmp/ship-lines.list.tmp tmp/deprecated-ships.list.tmp | tmp
	@echo "Listing base ships..."
	@cat tmp/ship-lines.list.tmp | tools/unquote-ship-base.sh | sort | uniq > tmp/tmp.list.tmp
	@comm -23 tmp/tmp.list.tmp tmp/deprecated-ships.list.tmp > $@

tmp/ships.list.tmp: tmp/ship-lines.list.tmp | tmp
	@echo "Listing ships..."
	@cat tmp/ship-lines.list.tmp | tools/unquote-ship.sh | sort | uniq > tmp/tmp.list.tmp
	@comm -23 tmp/tmp.list.tmp tmp/deprecated-ships.list.tmp > $@

tmp/ship-variants.list.tmp: tmp/base-ships.list.tmp tmp/ships.list.tmp | tmp
	@echo "Listing ship variants..."
	@comm -23 tmp/ships.list.tmp tmp/base-ships.list.tmp > $@

tmp/systems.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Listing systems..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^system" | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:system //" | tools/unquote.sh | sort | uniq > $@

tmp/wormholes.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Listing wormholes..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^wormhole" | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:wormhole //" | tools/unquote.sh | sort | uniq > $@

tmp/objects.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Listing objects..."
	@cat tmp/data-dirs.tmp | xargs grep -P -R '^\t\t?object ' | tr -d '\r' | grep '\.txt:' | sed 's|^.*\.txt:\t\t\?object ||' | tools/unquote.sh | sort | uniq > $@

tmp/planets.list.tmp: tmp/data-dirs.tmp tmp/wormholes.list.tmp tmp/objects.list.tmp | tmp
	@echo "Listing planets..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^planet" | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:planet //" | tools/unquote.sh | sort | uniq > tmp/tmp.tmp
	@comm -23 tmp/tmp.tmp tmp/wormholes.list.tmp > tmp/tmp2.tmp
	@comm -12 tmp/tmp2.tmp tmp/objects.list.tmp > $@

tmp/outfitters.list.tmp: tmp/all-data-dirs.tmp | tmp
	@echo "Listing outfitters..."
	@cat tmp/all-data-dirs.tmp | xargs grep -R "^outfitter" | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:outfitter //" | tools/unquote.sh | sort | uniq > $@

tmp/plugin-outfitters.list.tmp: tmp/available-plugin-data-dirs.tmp | tmp
	@echo "Listing plugin outfitters..."
	@cat tmp/available-plugin-data-dirs.tmp | xargs grep -R "^outfitter" | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:outfitter //" | tools/unquote.sh | sort | uniq > $@

tmp/shipyards.list.tmp: tmp/all-data-dirs.tmp | tmp
	@echo "Listing shipyards..."
	@cat tmp/all-data-dirs.tmp | xargs grep -R "^shipyard" | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:shipyard //" | tools/unquote.sh | sort | uniq > $@

tmp/plugin-shipyards.list.tmp: tmp/available-plugin-data-dirs.tmp | tmp
	@echo "Listing plugin shipyards..."
	@cat tmp/available-plugin-data-dirs.tmp | xargs grep -R "^shipyard" | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:shipyard //" | tools/unquote.sh | sort | uniq > $@

tmp/governments.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Listing governments..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^government" | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:government //g" | tools/unquote.sh | sort | uniq | sed "/^Escort$$/d" > $@

tmp/fleets.list.tmp: tmp/data-dirs.tmp | tmp 
	@echo "Listing fleets..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^fleet" | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:fleet //g" | tools/unquote.sh | sort | uniq > $@

tmp/licenses.list.tmp: tmp/all-data-dirs.tmp | tmp
	@echo "Listing licenses..."
	@cat tmp/all-data-dirs.tmp | xargs grep -P -R 'outfit.*License[`"]?$$' | tr -d '\r' | grep "\.txt:" | sed "s/^.*\.txt:outfit //" | tools/unquote.sh | sed 's| License$$||' | sort | uniq > $@

tmp/reputation-resets.tmp: default-reputations.txt | tmp
	@cat default-reputations.txt | sed -e "s/^\(\t\"\|\t\)/\"reputation: /" | sed "s/\(.*\)\" \(-\?.*\)$$/\1 \2/" | sed -r 's/ ([^ ]*)$$/" = \1/' > $@

tmp/friendlies-reputation-resets.tmp: default-reputations.txt | tmp
	@cat default-reputations.txt | sed "/ -/d" | sed -e "s/^\(\t\"\|\t\)/\"reputation: /" | sed "s/\(.*\)\" \(-\?.*\)$$/\1 \2/" | sed -r 's/ ([^ ]*)$$/" = \1/' > $@

tmp/friendly-reputation-sets.tmp: tmp/governments.list.tmp | tmp
	@cat tmp/governments.list.tmp | sed 's/^\(.*\)$$/"reputation: \1" = 10/' > $@

tmp/hostile-reputation-sets.tmp: tmp/governments.list.tmp | tmp
	@cat tmp/governments.list.tmp | sed 's/^\(.*\)$$/"reputation: \1" = -10/' > $@

data/outfitters/all-outfits.txt: tmp/outfits.list.tmp | tmp
	@echo "Updating all-outfits outfitter..."
	@cat $@ | sed "/\t/d" > tmp/tmp.tmp
	@mv tmp/tmp.tmp $@
	@cat tmp/outfits.list.tmp | sed 's|^\(.*\)$$|\t`\1`|' >> $@

data/shipyards/all-base-ships.txt: tmp/base-ships.list.tmp | tmp
	@echo "Updating base-ships shipyard..."
	@cat $@ | sed "/\t/d" > tmp/tmp.tmp
	@mv tmp/tmp.tmp $@
	@cat tmp/base-ships.list.tmp | sed 's|^\(.*\)$$|\t`\1`|' >> $@

data/shipyards/all-ship-variants.txt: tmp/ship-variants.list.tmp | tmp
	@echo "Updating ship-variants shipyard..."
	@cat $@ | sed "/\t/d" > tmp/tmp.tmp
	@mv tmp/tmp.tmp $@
	@cat tmp/ship-variants.list.tmp | sed 's|^\(.*\)$$|\t`\1`|' >> $@

data/map/planets.temp: tmp/outfitters.list.tmp tmp/shipyards.list.tmp | tmp
	@printf "Updating RTF planet template...\n"
	@cat $@ | sed "/^\tshipyard /d" | sed "/\toutfitter /d" | sed "/^]]$$/d" > tmp/tmp.tmp
	@mv tmp/tmp.tmp $@
	@echo '\toutfitter "Ruin-The-Fun Outfits"' >> $@
	@echo '\toutfitter "Ruin-The-Fun Stat Outfits"' >> $@
	@echo '\toutfitter "Ruin-The-Fun All Outfits"' >> $@
	@echo '\tshipyard "Ruin-The-Fun All Base Ships"' >> $@
	@echo '\tshipyard `modships`' >> $@
	@echo '\toutfitter `modoutfits`' >> $@
	@cat tmp/outfitters.list.tmp | sed 's/^\(.*\)$$/\toutfitter `\1`/' >> $@
	@cat tmp/shipyards.list.tmp | sed 's/^\(.*\)$$/\tshipyard `\1`/' >> $@
	@echo "]]" >> $@

data/jobs/visit-systems.txt: tmp/systems.list.tmp | tmp
	@echo "Updating job $@..."
	@cat $@ | sed '/\tvisit /d' > tmp/tmp.tmp
	@mv tmp/tmp.tmp $@
	@cat tmp/systems.list.tmp | sed 's|^\(.*\)$$|\tvisit `\1`|' >> $@

data/jobs/visit-planets.txt: tmp/planets.list.tmp | tmp
	@echo "Updating job $@..."
	@cat $@ | sed '/\t"visit planet" /d' > tmp/tmp.tmp
	@mv tmp/tmp.tmp $@
	@cat tmp/planets.list.tmp | sed 's/^\(.*\)$$/\t"visit planet" `\1`/' >> $@

data/events/all-licenses.txt: tmp/licenses.list.tmp | tmp
	@echo "Updating licenses..."
	@cat $@ | sed "/\t/d" > tmp/tmp.tmp
	@mv tmp/tmp.tmp $@
	@cat tmp/licenses.list.tmp | sed 's|^\(.*\)$$|\tset `license: \1`|' >> $@

default-reputations.txt:
	$(error This is currently not generated)
	#TODO: generate from $(ES_DEFAULT_PILOT_SAVE)

data/plugin-support/all-outfitters.txt: tmp/plugin-outfitters.list.tmp
	@sed 's|^\(.*\)$$|outfitter `\1`\n\tadd "Ruin-The-Fun Overridable Outfit"|' $< > $@
	
data/plugin-support/all-shipyards.txt: tmp/plugin-shipyards.list.tmp
	@sed 's|^\(.*\)$$|shipyard `\1`\n\tadd "Ruin-The-Fun Overridable Ship"|' $< > $@

data/jobs/reputation.txt: data/jobs/reputation.temp tmp/reputation-resets.tmp tmp/friendlies-reputation-resets.tmp tmp/friendly-reputation-sets.tmp tmp/hostile-reputation-sets.tmp
data/jobs/conditions/conditions.txt: data/jobs/conditions/conditions.temp data/jobs/conditions/condition-switches.list data/jobs/conditions/karma-values.list
data/jobs/combat-ships/combat-ships.txt: tmp/base-ships.list.tmp
data/jobs/combat-fleets/combat-fleets.txt: tmp/fleets.list.tmp
data/map/planets.txt: data/map/systems.csv
data/map/systems.txt: data/map/systems.csv
%.txt: %.temp
	@echo "Generating $@ from $<..."
	@tools/substitute-template.py $< > $@

tmp/-es-ruin-the-fun.zip: $(PLUGIN_FILES) | tmp
	@echo "Generating $@..."
	@rm -f $@
	@zip -r $@ $(PLUGIN_FILES)

.PHONY: clean
clean:
	@echo "Cleaning up..."
	@rm -rf tmp/

.PHONY: re
re: clean update
