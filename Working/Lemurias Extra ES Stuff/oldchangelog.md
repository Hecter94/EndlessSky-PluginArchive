Yes, a changelog.

# Most recent changelog
### v0.5.2
Due to some minor, trivial GitHub mess-ups, this changelog is not on any local copy of the plugin downloaded.

#### Name fixes
* Properly indented names
* Added "word" attribute to a phrase that didn't have it.

# Changes
## 0
### 0.1
* Basic plugin in place
### 0.2
* Orbona is now a battlefield between two governments: the Sayari Plushie Authority and the Counter Sayari Strike Force.
* Added two new governments that constantly battle in Orbona.
### 0.3
#### Annoying Bugs
* Fixed bug where <credits> would show up instead of mission payment. (Blame's on no-one here!)
#### New Content
* Added spoiled child delivery mission (Does not affect gameplay but has different dialog)
* Added the data drive commodity so the plugin won't require any dependencies
* 10 new star systems
* Why is there a Korath automaton in the Illumina Regions harvesting a gas giant? (We don't know why, and we also don't know where it is, so if you could find it and inform us on Laateli, Illumina, we'll get to investigating it right away.)
* Removed an unused government (It was a reference to a certain singer from Earth, particularly in a place called "Indonesia".)
* Populated some star systems with random stellar objects
### 0.4
#### New Content
* Earth's texture has been modified.
* Watch out: SPA and CSSF fleets are taking the fight to Suerolli.
* Added Yinachr
* Added Pedinai
* Populated several systems with celestial bodies. Systems populated include:
>* Suerolli
>* Kailoo-ereki
>* Aljuik
>* Serfeiia
>* Fevbaa
>* Iloke
 ### 0.5
#### New Content
* Earth's texture was changed back.
* Added new planets.
* Populated some systems with celestial bodies.
* First part of the SPA storyline out.
* Significantly reduced asteroids in Markaai to reduce lag
* Changed Markaai's orbit slightly
* Gave SPA ships names
* Bug: Fixed Pedinai's security (was `38` instead of `0.38`)
* Added SPA Falcon fleet (`spa.general.Falcon.lrg.1`)
* Rebalancing: De-intensified CSSF-SPA fleet battles to reduce lag on low-spec computers
* Added the Khoramelia Mission Office.
* Added more SPA fleets
* Added Arlok to Serfeiia
* Orbona battle made even more intense
* There's so much stuff that it's a good idea to read the commit history.
#### 0.5.1
##### Annoying bugs
* The ship names San Juan and Las Pinas (Filipino place names) were not quotemarked properly confusing the Endless Sky parser.
* Dialogue: The name of the recruit you escort to Khoramelia is Scott. Fixed dialogue option mistakenly referring to him as George, the person you meet on Millrace.
* Ship names under `spa.royalNavy.b` were not formatted properly (no `word` declaration and indent).
* The accept flag in the Millrace dialogue was not indented properly preventing the storyline from advancing further.
* Dialogue `goto` for the "Alright." option in label `gladWereSafe` under `spaContactFomalhaut` was not indented correctly, prematurely ending the story.
* Reputation modifiers for `spaRecruitPitch` were not formatted correctly. The CSSF will now hate on you if you accept the SPA's offer to join.
#### New content
* Added new SPA campaign jobs.

#### Notes
Well, we hope this plugin makes you happy!
#### v0.5.2
Due to some minor, trivial GitHub mess-ups, this changelog is not on any local copy of the plugin downloaded.

##### Name fixes
* Properly indented names
* Added "word" attribute to a phrase that didn't have it.
 
# Roadmap
### Next version
* Sporadic SPA-CSSF fleet battles in Republic/Synd space
* Populate Illumina Regions with stellar objects
* Add trade prices to Illumina Regions systems
