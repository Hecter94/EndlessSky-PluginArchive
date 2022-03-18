# Contributing to this project

Do not manually modify the [`data/`](data) directory.  This directory is completely
and automatically generated from vanilla Endless Sky source code and supporting
metadata.

You can modify any other source file except those in the data directory.  To
change the `data` directory we run the [`generate-plugin-data.sh`][sh] shell
script.

# How to update data

Updating the [`data/`](data) directory means you'll need to completely
regenerate it.  Assuming you also have the [endless-sky][ES] one directory up
you would refresh the data directory the following way.

    rm -rf data
    ./generate-plugin-data.sh ../endless-sky

[ES]: https://github.com/endless-sky/endless-sky
[sh]: generate-plugin-data.sh
