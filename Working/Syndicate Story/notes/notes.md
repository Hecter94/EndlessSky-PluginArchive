- starting ship automatically depreciates to 25% value; this is correct. Beware this doesn't change with game code changes!
- can't see any way to make Whitewashed Princess launch with 1 crew in event of decline :-(
- [Bug] interest rates >= 1% or <0.1% format wrong in bank display
- TODO easter egg if complete FW story with Sc good-luck start
- current package-drop probably completes in Jan 2014, at odds with FW 'mid-June'.
- naming scheme "syndicate x" probably cause conflicts if merged with main
- immersion break if piloting single-pilot ship while co-pilot still around
- seems `not <>` conditions are ready immediately from intro conversation, but `has <>` are only ready after taking off and landing!
- bootstrap 1b dest Amazon, is a frontier world... better somewhere easier to land, but check surrounding story for consistency
- bootstrap 3a not sure how to change payment based on whether you need advance for weapons
- potential bug bootstrap 3a/b: a has 1 passenger requirement; b has none (temporarily 1 to avoid this bug) but b silently fails on a accepted otherwise auto-accepted
- need Syndicate Intro Complete to allow Hephaestus meeting to trigger
- "to fail" dialogues don't appear to be working.
- 'visit' messages
- ships on bootstrap 3b keep chasing even into republic space!
	+ can make them "staying launching"
- is it just good luck that in Package Delivery you don't get caught if scanned?
- have obituaries column occasionally in news, if Syndicate Bootstrap Too-Late
- no way to set payment within mission conversation? if there is, can allow player to accept offer without getting best bargain. (Sc Bootstrap Too-Late) ... maybe can apply credits in the on-complete block
- if change payment on Bootstrap 5, must change text on Bootstrap Too-Late
- should logs be first or second person? seems most FW logs are carefully crafted to be neither
- make Co-Pilot person ship, if complete Sc Package 5
- is there some way to refuel on Mutiny? Awkward to get stuck there with no fuel! Could briefly add a spaceport? but makes fitting with the story harder
- some missions (e.g. Hai-human outfitter) assume you're the hero of humanity if "main plot completed" but others also depend on it to know the war's over.
- many of the payments (especially early in Rescue) in ScS aren't well thought through or compared to FW and other missions
- also some incongruity in dialogue if passenger space only on escorts not flagship
- Offering a mission based on condition set in conversation doesn't enable until re-entering planet.
	+ instead need to e.g. test not something, then set in alternative dialogue if not wanting
- can rewrite all transport-or-escort missions `to spawn` instead of two missions
- Log few months before reach pug: "Finally scraped together enough money for starship"

- [bug] luxury accommodations are tested installed into flagship and/or held in cargo.
- [todo] event: Poisonwood independence/reverts are both FW specific

extras:

- check what triggers cannibal mission allowed after intro. Seems to be allowed before checking back in with Downey (Which is okay, if other blocking is still working)

come back after break missions

- are currently `minor`. Better to trigger on-landing?

governments

- can you get in trouble killing too many Independent (Killable)s - that new ones will start hostile?
- Is there a downside to proliferating minor governments for mission purposes?