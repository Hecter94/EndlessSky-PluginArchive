## Intent:

Performing the below actions should result in a working directory `<work_dir>` which will permit the map editor and game to both correctly load the plugin while still keeping the plugin repository safely seperated from the root game data.

### Assumptions:
   - The repo was simply cloned to `%appdata%\endless-sky\plugins\ES_ExpandedTerritory`
   - that steam is installed to the default location `%ProgramFiles(x86)%\Steam`
   - that Endless Sky is installed to the default install location set by steam (`<steam_dir>\steamapps\common\...`)

### Commands:
```
cd <work_dir>
mklink /J data "%appdata%\endless-sky\plugins\ES_ExpandedTerritory\data"
mklink /J images "%ProgramFiles(x86)%\Steam\steamapps\common\Endless Sky\images"
mklink /J repo "%appdata%\endless-sky\plugins\ES_ExpandedTerritory"

cd "%ProgramFiles(x86)%\Steam\steamapps\common\Endless Sky\images"
mklink es_et "%appdata%\endless-sky\plugins\ES_ExpandedTerritory\images\es_et"
```

When opening in the map editor, please open files by way of the `<work_dir>\data` directory tree.
