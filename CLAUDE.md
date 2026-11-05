# West Virginia Eats (wv-eats) — notes for Claude Code sessions

Built 2026-11-05 by a side session for Nick's "build Utah, Vermont, Virginia, West Virginia and Wyoming", ported from `../vt-eats/`
(itself from `../ut-eats/` and `../md-eats/`) with every fix to that day (the exact-outline county lookup, the out-of-county truck rule,
Utah's street-word merge fix, Vermont's narrowed "dejavu" rule, Virginia's near-adult-venue fix). Local only: git-ignored data, no
repo, no remote, nothing published. Sources and calibration: `playbook/12-sources.md`. Brand: `playbook/05-naming.md` —
**provisional**, every choice waits for Nick ("West Virginia Eats: Restaurants", Home Screen "West Virginia Eats"; a pepperoni roll
icon, concept A, on ridge green; the landscape palette from `state-prompts/WEST_VIRGINIA_PROMPT.md`: ridge green #2E5E3E, gorge slate
#1F3B5C, rhododendron #C2477A, maple gold #E0A526 fill only, cream; a band of layered Allegheny ridgelines).

## West Virginia is different
- **No official list a script may read.** Local health departments inspect under 64CSR17 and publish no results as data; 25 of them
  post reports on the Digital Health Department portal, which is search-only and whose robots.txt disallows all crawlers (naming
  ClaudeBot): never read, and each place links to the state's Food Safety page (oehs.wvdhhr.org/phs/food-safety/). The ABCA license
  search downloads a CSV but posts no terms: not used, so "Serves alcohol" is unknown everywhere (Nick's call). 0 official places.
- **Counties:** West Virginia's 55; one detail file (`detail-west-virginia.json`), as the prompt asks; the site groups pages by county.
  `fetch_overture.py` checks the river towns on both sides of each line (Huntington in, Ashland KY out; Wheeling in, Bridgeport OH out).
- **Honors:** no MICHELIN Guide covers West Virginia. James Beard: Jim's Steak and Spaghetti House (America's Classics 2019), Figaretti's
  (America's Classics 2026), Paul Smith of 1010 Bridge (Best Chef: Southeast winner 2024), Alma Bea (2026 finalist), Ristorante Abruzzi
  (2025 semifinalist).
- **Guides** (tags in `westvirginia.py` TAGS; bits 1..128): pepperoni rolls (West Virginia Tourism's Pepperoni Roll Trail, updated
  2025-10-23), hot dogs, Italian classics, Appalachian tables (West Virginia Tourism's company listings, read by `scripts/read_wvt.py`),
  ramps (its ramp-season guide, updated 2026-03-11), historic inns and fish sandwiches (one each so far: no Home card), oldest (North
  End Tavern 1899, Tasting Table; Minard's 1937, its listing).
- **Ranking:** "Featured first" (honors, then founding year), as everywhere until Nick decides on the all-factor Ranked score
  (`eats-ranked-score-all-states-proposal-2026-11-05.md` in the shared notes); no health-grade wording anywhere.

## Rebuild
```bash
cd pipeline
../.venv/bin/python check_sources.py URL...   # a new host first
../.venv/bin/python fetch_overture.py && ../.venv/bin/python fetch_extras.py && ../.venv/bin/python fetch_official.py
../.venv/bin/python geocode_official.py && ../.venv/bin/python geocode_census.py && ../.venv/bin/python listings.py
../.venv/bin/python calibrate.py && ../.venv/bin/python westvirginia.py && ../.venv/bin/python build_research.py && ../.venv/bin/python westvirginia.py
WV_APP=1 ../.venv/bin/python westvirginia.py && cd .. && cp data/app/places.json data/app/detail-*.json WestVirginiaEats/Resources/
.venv/bin/python pipeline/check_websites.py --retry-transient   # link verification; re-export after
.venv/bin/python scripts/make-site.py && .venv/bin/python scripts/publish_app_data.py && .venv/bin/python scripts/publish_app_data.py --check
.venv/bin/python scripts/qa-site.py --static
```
(`listings.py` must run before `calibrate.py`, and `westvirginia.py` once before `build_research.py`, which matches names against
`site/westvirginia.json`.) The `.venv` is on the python.org framework Python 3.12 (Homebrew's python@3.12 is gone), with md-eats' versions.
`data/ucsd/meta-West_Virginia.json.gz` (Google 2021, private, web build only) comes from mcauleylab.ucsd.edu's googlelocal set.
`scripts/read_wvt.py` reads West Virginia Tourism's company listings (one request per 1.5 s) into `data/research/raw/` (private).

## App, site, screenshots
- App: `WestVirginiaEats/` (XcodeGen `project.yml`, bundle `com.westvirginiaeats.ios`, display "West Virginia Eats"), tests in `WestVirginiaEatsTests/` (data guards:
  adult venues, blocklisted and multi-URL websites, bad and legal names, non-restaurants, listed twice, no Google data; MICHELIN; the
  outline with Ashland, Steubenville and Bluefield, VA). Run tests: `DEVELOPER_DIR="/Applications/Xcode 1.app/Contents/Developer" xcodebuild test ...
  CODE_SIGNING_ALLOWED=NO` on a temporary simulator. Archive only with Xcode 1.app (now 27.2, 27B52); Xcode.app is a beta.
  Run `xcodegen generate` after the export whenever the set of `Resources/*.json` files changes (an app built without them still
  compiles but opens on "Couldn't open the list").
- Site: `scripts/make-site.py` writes `docs/` and
  `playbook/site-numbers.json`; `scripts/explore.js` is the web app; `scripts/qa-site.py` the QA. Site URL for now:
  nickstrom5.github.io/west-virginia-eats (no CNAME). Rebuild the site before the unit tests: `ShareLinkTests` reads the web app's ids from `docs/`.
- OTA data: `docs/data/app/` via `scripts/publish_app_data.py` (`../OTA-DATA.md`).
- Screenshots: `scripts/capture-screenshots.sh <sim>` (ScreenshotMode pins downtown Charleston; Fairmont for pepperoni rolls and
  Italian), then `scripts/site-images.sh`, then make-site + qa-site. App Store frames: `scripts/appstore-screenshots.py`. Icons:
  `scripts/icon-concepts.swift` (A pepperoni roll and B slaw dog pass `state-prompts/icon-style/check.swift`; C ramps fails the
  centroid rule) and `scripts/make-brand.swift`.
- Not ported: the App Store listing writer and the private Google-2021 leaderboard. `site/` holds the leaderboard's data and is
  git-ignored with `data/`.

## Fixes after the first build (2026-11-05)
- **UI test:** the "my location" map check used Baltimore's Inner Harbor (from md-eats); now this state's own downtown.
- **Last full run** 2026-11-05: app 3,414 places / 3,339 restaurants, 49 unit tests on iPhone 17 Pro Max (iOS 27.0), 12 iPhone +
  6 iPad screens, `qa-site.py --static` OK, OTA 2026-11-05.1 (local only).
- **ZIPs:** the export (`pipeline/westvirginia.py`, the place's `z` and the address-strip pattern) still kept only Maryland's 206xx-219xx, carried
  from md-eats, so the app showed addresses without a ZIP and ZIP search found little. Now this state's own range (247xx-268xx); the
  detail screenshot was re-captured.
- **Web app:** `scripts/explore.js`'s place panel named Utah's "Department of Alcoholic Beverage Services" as the liquor licensor (a
  ut-eats leftover); it now says what the app's PlaceDetailView says.

## Rules
No commits, pushes, public repos, App Store Connect or DNS changes without Nick's yes each time; never submit for review or accept
agreements; never publish Google-derived data. Support email nick@eatsranked.com. Commit author "Nick Soderstrom"
<329204362+nickstrom5@users.noreply.github.com> via `-c user.name -c user.email`.
