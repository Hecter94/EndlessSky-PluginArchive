
### Zone of Control ###

**Author: [Timeout](https://github.com/LixiChronikouOriou)**

#### Introduction ####
In vanilla, tributing human space is a bit tedious because there are no mechanisms for making peace with the factions. The only systems which don't cause issues are the Pirates' ones. To tribute the Free Worlds one has to save-edit afterwards, for tributing Republic and Syndicate one has to use the phases during the main campaign to profit from the reputation reset afterwards. Independent systems like Men cause problems with neutral mission NPCs, so one has to save-edit here, too. Also the monastery planets New Tibet cannot be tributed in vanilla, causing ugly spots on the conquest map.

#### Features ####
This post-campaign plugin solves this issue by providing a peace-making mechanism after tributing all systems of a faction, and by introducing polities for independent systems. Further, some planets will pay you tribute without a fight after the completion of a mission chain. Also New Tibet and Harmony will pay symbolic tribute of 1 credit to color the map.

Has individual dialogue boxes for each of the following situations.

| Faction | Requires | Results |
|---------|----------|----------|
| Free Worlds | Main plot complete. All FW systems except Alioth and Girtab dominated. | Recovered reputation for FW and Militia. Revoked militia license will be restored. New Tibet (Alioth) and Harmony (Girtab) will pay symbolic tribute (1 credit) to color the map properly. |
| Republic | Main plot complete. All Republican systems dominated. | Recovered reputation for Republic and Deep Security. Revoked navy licenses will **not** be restored. |
| Syndicate | Main plot complete. All Syndicate systems dominated. | Recovered reputation for Syndicate. |
| Free State <sup>1</sup> | Main plot complete. All Free State systems dominated. | Recovered reputation for Free State and Militia. |
| Commonwealth<sup>2</sup> | Main plot complete. All Commonwealth systems dominated. | Recovered reputation for Commonwealth and Militia. |

1) A new polity for the independent system of Men. Includes Antares, if it remains neutral after the campaign.
2) A new polity if the system Tarazed remains independent after the campaign. Includes also the inhabited systems Dabih and Albireo.

| Planet | Requires | Results |
|--------|----------|---------|
| Haven | 90 days after "Ice Queen 8: done", and Haven isn't tributed currently. | Haven dominated. |
| Norn | 90 days after "Stone to Hope: Thanks: offered", and Norn isn't tributed currently. | Norn dominated. |
| Poisonwood | 30 days after "event: liberation of Poisonwood" (and done it the proper way) and "main plot completed", and Poisonwood isn't tributed currently. | Poisonwood dominated. |
| Windblain | 30 days after "Hjlod Remembers Windblain: done", and Windblain isn't tributed currently. | Windblain dominated. |

**Changelog**

| Date | Version | Comment |
|------|---------|---------|
| 2025-08-09 | 1.0.0 | Initial release. |
