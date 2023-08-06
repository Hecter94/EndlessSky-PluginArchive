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
RTF_PLANET_FILES += data/map/planets/RTF-0-P.txt
RTF_PLANET_FILES += data/map/planets/RTF-1-P.txt
RTF_PLANET_FILES += data/map/planets/RTF-2-P.txt
RTF_PLANET_FILES += data/map/planets/RTF-3-P.txt
RTF_PLANET_FILES += data/map/planets/RTF-4-P.txt
RTF_PLANET_FILES += data/map/planets/RTF-5-P.txt
RTF_PLANET_FILES += data/map/planets/RTF-6-P.txt
RTF_PLANET_FILES += data/map/planets/RTF-7-P.txt
RTF_PLANET_FILES += data/map/planets/RTF-8-P.txt
RTF_PLANET_FILES += data/map/planets/RTF-9-P.txt
RTF_PLANET_FILES += data/map/planets/RTF-10-P.txt
RTF_JOB_FILES += data/jobs/reputation.txt
RTF_JOB_FILES += data/jobs/visit-systems.txt
RTF_JOB_FILES += data/jobs/visit-planets.txt
GENERATED_DATA_FILES += $(RTF_PLANET_FILES)
GENERATED_DATA_FILES += $(RTF_JOB_FILES)
GENERATED_DATA_FILES += data/events/all-licenses.txt



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

tmp/enabled-plugins.tmp: ../../plugins.txt | tmp
	@echo "Updating enabled plugin list..."
	@cat $< | grep " 1$$" | sed "s/ 1$$//" | sed 's/^[[:space:]]*//' > $@

.PHONY: plugin-update
plugin-update: tmp/enabled-plugins.tmp tmp/data-dirs.tmp
	@echo "Inserting enabled plugin list into data sources..."
	@cat $< | sed "s/^/..\/..\/plugins\//" | sed "/ruin-the-fun/d" | sed "s/$$/\/data\//" >> tmp/data-dirs.tmp
	@make update

tmp/re.tmp: | tmp
	@touch $@

tmp/deprecated-outfits.list.tmp: tmp/data-dirs.tmp
	@echo "Listing deprecated outfits..."
	@cat tmp/data-dirs.tmp | sed "s|$$|_deprecated/|" | xargs grep -R "^outfit " | grep "\.txt:" | sed "s/^.*\.txt:outfit //" | tools/unquote.sh | sort | uniq > $@

tmp/deprecated-ships.list.tmp: tmp/data-dirs.tmp
	@echo "Listing deprecated ship..."
	@cat tmp/data-dirs.tmp | sed "s|$$|_deprecated/|" | xargs grep -R "^ship " | grep "\.txt:" | sed "s/^.*\.txt:ship //" | tools/unquote-ship.sh | sort | uniq > $@

tmp/outfits.list.tmp: tmp/data-dirs.tmp tmp/deprecated-outfits.list.tmp | tmp
	@echo "Listing outfits..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^outfit " | grep "\.txt:" | sed "s/^.*\.txt:outfit //" | tools/unquote.sh | sort | uniq > tmp/tmp.list.tmp
	@comm -23 tmp/tmp.list.tmp tmp/deprecated-outfits.list.tmp > $@

tmp/ship-lines.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Finding ship definitions..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^ship " | grep "\.txt:" | sed "s/^.*\.txt:ship //" | sort | uniq > $@

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
	@cat tmp/data-dirs.tmp | xargs grep -R "^system" | grep "\.txt:" | sed "s/^.*\.txt:system //" | tools/unquote.sh | sort | uniq > $@

tmp/wormholes.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Listing wormholes..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^wormhole" | grep "\.txt:" | sed "s/^.*\.txt:wormhole //" | tools/unquote.sh | sort | uniq > $@

tmp/objects.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Listing objects..."
	@cat tmp/data-dirs.tmp | xargs grep -P -R '^\t\t?object ' | grep '\.txt:' | sed 's|^.*\.txt:\t\t\?object ||' | tools/unquote.sh | sort | uniq > $@

tmp/planets.list.tmp: tmp/data-dirs.tmp tmp/wormholes.list.tmp tmp/objects.list.tmp | tmp
	@echo "Listing planets..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^planet" | grep "\.txt:" | sed "s/^.*\.txt:planet //" | tools/unquote.sh | sort | uniq > tmp/tmp.tmp
	@comm -23 tmp/tmp.tmp tmp/wormholes.list.tmp > tmp/tmp2.tmp
	@comm -12 tmp/tmp2.tmp tmp/objects.list.tmp > $@

tmp/outfitters.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Listing outfitters..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^outfitter" | grep "\.txt:" | sed "s/^.*\.txt:outfitter //" | tools/unquote.sh | sort | uniq > $@

tmp/shipyards.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Listing shipyards..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^shipyard" | grep "\.txt:" | sed "s/^.*\.txt:shipyard //" | tools/unquote.sh | sort | uniq > $@

tmp/governments.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Listing governments..."
	@cat tmp/data-dirs.tmp | xargs grep -R "^government" | grep "\.txt:" | sed "s/^.*\.txt:government //g" | tools/unquote.sh | sort | uniq | sed "/^Escort$$/d" > $@

tmp/licenses.list.tmp: tmp/data-dirs.tmp | tmp
	@echo "Listing licenses..."
	@cat tmp/data-dirs.tmp | xargs grep -P -R "outfit.*License" | grep "\.txt:" | sed "s/^.*\.txt:outfit //" | tools/unquote.sh | sed 's| License$$||' | sort | uniq > $@

.PHONY: data/outfitters/all-outfits.txt
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

data/map/planets/RTF-%-P.txt: tmp/outfitters.list.tmp tmp/shipyards.list.tmp | tmp
	@printf "Updating planet %s...\n" $@
	@cat $@ | sed "/^\tshipyard /d" | sed "/\toutfitter /d" > tmp/tmp.tmp
	@mv tmp/tmp.tmp $@
	@echo '\toutfitter "Ruin-The-Fun Outfits"' >> $@
	@echo '\toutfitter "Ruin-The-Fun Stat Outfits"' >> $@
	@echo '\toutfitter "Ruin-The-Fun All Outfits"' >> $@
	@echo '\tshipyard "Ruin-The-Fun All Base Ships"' >> $@
	@cat tmp/outfitters.list.tmp | sed 's/^\(.*\)$$/\toutfitter `\1`/' >> $@
	@cat tmp/shipyards.list.tmp | sed 's/^\(.*\)$$/\tshipyard `\1`/' >> $@

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

tmp/REPUTATION_RESET_ALL.txt: default-reputations.txt | tmp
	@cat default-reputations.txt | sed -e "s/^\(\t\"\|\t\)/\t\t\t\t\"reputation: /" | sed "s/\(.*\)\" \(-\?.*\)$$/\1 \2/" | sed -r 's/ ([^ ]*)$$/" = \1/' > $@

tmp/REPUTATION_RESET_FRIENDLIES.txt: default-reputations.txt | tmp
	@cat default-reputations.txt | sed "/ -/d" | sed -e "s/^\(\t\"\|\t\)/\t\t\t\t\"reputation: /" | sed "s/\(.*\)\" \(-\?.*\)$$/\1 \2/" | sed -r 's/ ([^ ]*)$$/" = \1/' > $@

tmp/REPUTATION_FRIENDLY_ALL.txt: tmp/governments.list.tmp | tmp
	@cat tmp/governments.list.tmp | sed 's/^\(.*\)$$/\t\t\t\t"reputation: \1" = 10/' > $@

tmp/REPUTATION_HOSTILE_ALL.txt: tmp/governments.list.tmp | tmp
	@cat tmp/governments.list.tmp | sed 's/^\(.*\)$$/\t\t\t\t"reputation: \1" = -10/' > $@

tmp/REPUTATION_TOGGLE_CHOICES.tmp: tmp/governments.list.tmp | tmp
	@cat tmp/governments.list.tmp | sed 's/^\(.*\)$$/\t\t\t\t\`\t\1:\tCurrently Friendly\t(toggle)\`\n\t\t\t\t\tto display\n\t\t\t\t\t\t"reputation: \1" >= 0\n\t\t\t\t\tgoto "toggle hostile: \1"\n\t\t\t\t\`\t\1:\tCurrently Hostile\t(toggle)\`\n\t\t\t\t\tto display\n\t\t\t\t\t\t"reputation: \1" < 0\n\t\t\t\t\tgoto "toggle friendly: \1"/' > $@

tmp/REPUTATION_TOGGLE_LABELS.tmp: tmp/governments.list.tmp | tmp
	@rm -f $@
	@cat tmp/governments.list.tmp | sed 's/^\(.*\)$$/\t\t\tlabel "toggle friendly: \1"\n\t\t\taction\n\t\t\t\t"reputation: \1" = 10\n\t\t\t\`\tReputation with \1 changed to Friendly.\`\n\t\t\t\tgoto toggles/' >> $@
	@cat tmp/governments.list.tmp | sed 's/^\(.*\)$$/\t\t\tlabel "toggle hostile: \1"\n\t\t\taction\n\t\t\t\t"reputation: \1" = -10\n\t\t\t\`\tReputation with \1 changed to Hostile.\`\n\t\t\t\tgoto toggles/' >> $@

data/jobs/reputation.txt: tmp/REPUTATION_RESET_ALL.txt tmp/REPUTATION_RESET_FRIENDLIES.txt tmp/REPUTATION_FRIENDLY_ALL.txt tmp/REPUTATION_HOSTILE_ALL.txt tmp/REPUTATION_TOGGLE_CHOICES.tmp tmp/REPUTATION_TOGGLE_LABELS.tmp
	@echo "Generating job $@..."
	@cp data/jobs/reputation.txt.src data/jobs/reputation.txt
	@sed -i -e "/REPUTATION_RESET_ALL/{r tmp/REPUTATION_RESET_ALL.txt" -e ";d;}" $@
	@sed -i -e "/REPUTATION_RESET_FRIENDLIES/{r tmp/REPUTATION_RESET_FRIENDLIES.txt" -e ";d;}" $@
	@sed -i -e "/REPUTATION_FRIENDLY_ALL/{r tmp/REPUTATION_FRIENDLY_ALL.txt" -e ";d;}" $@
	@sed -i -e "/REPUTATION_HOSTILE_ALL/{r tmp/REPUTATION_HOSTILE_ALL.txt" -e ";d;}" $@
	@sed -i -e "/REPUTATION_TOGGLE_CHOICES/{r tmp/REPUTATION_TOGGLE_CHOICES.tmp" -e ";d;}" $@
	@sed -i -e "/REPUTATION_TOGGLE_LABELS/{r tmp/REPUTATION_TOGGLE_LABELS.tmp" -e ";d;}" $@

.PHONY: update
clean:
	@echo "Cleaning up..."
	@rm -rf tmp/

.PHONY: re
re: clean update
