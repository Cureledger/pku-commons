# Adding restaurants

**One rule: say where it came from.** No award required, no approval step, no gate.

Michelin was a way to bound a starting list for one city. It is not the membership rule and never was — a guide that only covers 15 restaurants in Asheville is not usable by a family trying to eat dinner.

## Add one

```bash
python3 src/add.py --name "Sunny Point Cafe" --city Asheville --region NC \
    --website https://sunnypointcafe.com --source community --by nina
```

## Add a list

Paste a best-of list, an association directory, or your own notes into a text file, one per line:

```
# Name | website | address   — website and address optional
Chai Pani | https://chaipani.com | 22 Battery Park Ave
Rhubarb | https://rhubarbasheville.com
Bull & Beggar
```

```bash
python3 src/add.py --batch mylist.txt --city Asheville --region NC \
    --source local_list --by nina --citation "Best of WNC 2025, Best Brunch"
```

That is the scaling path. 60 restaurants from an association directory is one command.

## Add a new city

Nothing to configure. The city id is derived from what you type:

```bash
python3 src/add.py --batch seville.txt --city Seville --country es \
    --source local_list --by contributor --citation "Diario de Sevilla, mejores tapas 2025"
```

`--region` is optional, so non-US addresses work without a state. IDs come out as
`seville-es/casa-morales`, `melbourne-vic-au/attica`, `asheville-nc-us/table`.

## The `--source` values

| source | means |
|---|---|
| `award` | a recognition program named it |
| `local_list` | a city best-of list, reader poll, or critic |
| `association` | a restaurant association directory — the highest-volume route |
| `community` | someone in the PKU community suggested it |
| `self_submitted` | the restaurant asked to be listed |
| `operator_import` | bulk import from a platform or directory |
| `visit` | someone ate there and added it afterwards |

None of these is better than the others. They record *how* the record arrived so a later reader can judge it.

## Awards, when you have one

```bash
python3 src/add.py --name "Cúrate Bar de Tapas" --city Asheville --region NC \
    --source award --award-program "MICHELIN Guide" --award-tier "Selected" \
    --award-year 2025 --by nina --citation "https://..."
```

`awards` is a list, so a restaurant can hold several. Store the tier label **verbatim** — Michelin's current word for the non-starred tier is `Selected`, not `Recommended`. Never flatten two recognitions into one label.

## Reaching the same restaurant twice

Adding an existing restaurant **merges** rather than duplicating: both awards kept, both citations kept, and the second route recorded in `also_found_via`. So you can run a Michelin import, then a Best of WNC import, then an association import over the same city and the overlaps resolve themselves.

## What a new record does not have

`census.status` is `no_menu_captured` and `accommodation.status` is `unverified` until someone does that work. **`unverified` is not zero** — it means nobody has asked yet. A restaurant with no menu captured is still worth listing, because a name plus an address plus a phone number is already more than a family has now.

## What being in the registry does not mean

Not an endorsement, not a rating, not a claim that the food is good or that a PKU diet is possible there. It means the restaurant exists, it is in this city, and here is what we know so far. `data/negative_controls.json` covers false *award* claims only — several names in it are legitimately in the registry.
