# LEEST Commit Message Guidelines

Eventually, we will have a script that automatically generates LEEST changelogs.

## Format
```xml
<type>(<scope>): <subject>
<blank-line>
<body>
<blank-line>
<footer>
```

### Fields
| Field | Description
|---|---|
| `<type>` | The type of the commit, such as `feat`, `fix`, `refactor`, or other types.
| `<scope>` | The scope of the commit. For example, changes to the map would be `feat(map)`.
| `<subject>` | The subject of the commit. Ideally, under 50 characters (includes the type and scope).
| `<body>` | The body of the commit, which can explain the commit and the intentions behind it in greater detail.
| `<footer>` | Optional. Usually trailers like `Co-authored-by` and in more recent times, a patch number (`v0.10.16-patch69`). The patch number should only be added if the plugin itself is modified. Changes to documentation do not have this patch number added.

### Trailers
| Trailer | Description
|---|---|
| `Changelog-item` | The item to be added to the changelog, such as `Added bounty hunters to hunt down player if they insult Anne Rice`. This is usually written in past tense, while the git commit messages are in the imperative mood.
| `Reverts-commit` | The commits that are reverted. Again, used by the script (coming soon) to generate the changelog.

Other trailers can be added, such as `Co-authored-by` and `Signed-off-by`. This README section only lists the trailers which are specific to LEEST.
