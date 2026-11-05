"""Writes data/research/app/*.json (hand-checked West Virginia guides), data/research/michelin.json, jbf.json and closed.json from the
compact lists below. Ported from vt-eats/pipeline/build_research.py.

Each entry cites the page that names it, read on 2026-11-05: West Virginia Tourism's own listing for the business
(wvtourism.com/company/<slug>, read by scripts/read_wvt.py; robots allows them), the Department of Tourism's dated articles (the
Pepperoni Roll Trail, updated 2025-10-23; the ramp-season guide, updated 2026-03-11), or a page dated 2025-26 on a robots-checked host
(check_sources.py). The address comes from the map listing we already hold for that name in that town (site/westvirginia.json); a name
that isn't found exactly once in its town (or at the street number given) is left out and listed in data/research/app/LEADS.md. A place
the map data doesn't show as a place to eat is added only with a street address from its official listing (ADDR).
Usage: ../.venv/bin/python build_research.py   (then westvirginia.py)"""
import json, os, re
from brands import brand_of
from common import norm_name
ROOT = os.path.join(os.path.dirname(__file__), "..")
R = os.path.join(ROOT, "data", "research")
d = json.load(open(os.path.join(ROOT, "site", "westvirginia.json")))
C, M = d["cols"], d["meta"]
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower().replace("'", "").replace("’", ""))).strip()

# each dated on its face, or an official tourism listing (read 2026-11-05)
W = lambda slug: f"https://wvtourism.com/company/{slug}/"                                            # West Virginia Tourism listing
TRAIL = "https://wvtourism.com/bite-by-bite-discover-west-virginias-beloved-snack-on-the-pepperoni-roll-trail/"  # updated 2025-10-23
RAMPS = "https://wvtourism.com/a-foodies-guide-to-ramp-season-in-west-virginia/"                       # updated 2026-03-11
TT_OLDREST = "https://www.tastingtable.com/1975409/oldest-restaurant-every-state-still-open/"          # 2025-09-23
JBF26 = "https://www.jamesbeard.org/stories/james-beard-award-semifinalists-2026"                   # 2026-01-21
JBF26N = "https://www.jamesbeard.org/stories/james-beard-awards-restaurant-and-chef-nominees-2026"  # 2026-03-31
JBF25 = "https://www.jamesbeard.org/stories/the-2025-james-beard-award-semifinalists"               # 2025-01-22
JBF24W = "https://www.jamesbeard.org/stories/the-2024-james-beard-award-winners"                    # 2024 winners
JBF19C = "https://www.jamesbeard.org/stories/announcing-the-2019-americas-classics-winners"          # 2019 America's Classics
JBF26C = "https://www.jamesbeard.org/stories/james-beard-americas-classics-award-winners-2026"       # 2026 America's Classics

# (name as the source writes it or as our listing spells it, town as our listing has it, street number to pick the location (or
# None), note, founded, founded_note, [sources])
GUIDES = {
 "pepperoni roll": [   # the Pepperoni Roll Trail's stops (West Virginia Tourism, updated October 2025)
  ("Country Club Bakery", "Fairmont", "1211", "The bakery the state calls the home of the original pepperoni roll, with fresh rolls out of the oven all day.", None, None,
   [TRAIL, W("country-club-bakery")]),
  ("Colasessano's Pizza", "Fairmont", "141", "Pizza and pepperoni rolls, fresh-baked or frozen, at the White Hall store.", None, None, [TRAIL, W("colasessanos")]),
  ("Tomaro's Bakery", "Clarksburg", "411", "A Glen Elk bakery on the Pepperoni Roll Trail.", None, None, [TRAIL]),
  ("D'Annunzio's Bakery", "Clarksburg", "1909", "A Clarksburg bakery on the Pepperoni Roll Trail.", None, None, [TRAIL]),
  ("Home Industry Bakery", "Clarksburg", "173", "A Clarksburg bakery on the Pepperoni Roll Trail.", None, None, [TRAIL]),
  ("Della's Deli", "Bridgeport", "230", "A downtown deli with fresh-baked pepperoni rolls, Italian specialties and sandwiches.", None, None, [TRAIL, W("dellas-deli-llc")]),
  ("Bakers Nook", "Farmington", "1315", "A Farmington bakery on the Pepperoni Roll Trail.", None, None, [TRAIL]),
  ("Mama Di Roma", "Fairmont", "323", "A Fairmont stop on the Pepperoni Roll Trail.", None, None, [TRAIL]),
  ("Munchies Eats & Sweets", "White Hall", "2600", "A White Hall stop on the Pepperoni Roll Trail.", None, None, [TRAIL]),
  ("The Donut Spot", "Buckhannon", "51", "A Buckhannon stop on the Pepperoni Roll Trail.", None, None, [TRAIL]),
  ("The Humble Tomato", "Lewisburg", "855", "A Lewisburg Italian restaurant, added to the Pepperoni Roll Trail in 2025.", None, None, [TRAIL, W("the-humble-tomato")]),
 ],
 "hot dog": [   # West Virginia Tourism's listings for the stands
  ("Morrison's Drive Inn", "Logan", "126", "Hot dogs, homemade onion rings and curb service in Logan.", None, None, [W("morrisons-drive-inn")]),
  ("Hillbilly Hot Dogs", "Lesage", "6951", "Hot dogs and burgers on the Ohio River Road, home of the Homewrecker.", None, None, [W("hillbilly-hotdogs")]),
  ("The Custard Stand", "Webster Springs", "51", "West Virginia hot dogs under the stand's own chili.", None, None, [W("custard-stand-webster-springs")]),
  ("Jims Drive In", "Lewisburg", "479", "An old-time drive-in: hot dogs, homemade chili and ice cream brought to your car.", None, None, [W("jims-drive-in")]),
  ("Stuart's Smokehouse & Seafood", "Alderson", "1738", "Hot dogs, chili, barbecue and steaks beside the Greenbrier River.", None, None, [W("stuarts-hot-dawg-smokehouse")]),
 ],
 "italian classic": [   # the north-central coal towns and Wheeling, each on its own tourism listing
  ("Muriale's Italian Kitchen", "Fairmont", "1742", "A southern Italian family restaurant since 1969; its sauce is its signature.", None, None, [W("muriales-restaurant")]),
  ("Julio's Café", "Clarksburg", "501", "A family restaurant with old-world recipes handed down through the generations.", None, None, [W("julios-cafe")]),
  ("Minard's Spaghetti Inn", "Clarksburg", "813", "Home-style Italian cooking in Clarksburg since 1937.", 1937,
   "Minard's own West Virginia Tourism listing: since 1937.", [W("minards-spaghetti-inn")]),
  ("Figaretti's Restaurant", "Wheeling", "1035", "Homemade Italian and a long wine list; a James Beard America's Classic (2026).", None, None,
   [W("figarettis-restaurant"), JBF26C]),
  ("Jim's Steak and Spaghetti House", "Huntington", "920", "Spaghetti, haddock fish sandwiches and pie by the slice; a James Beard America's Classic (2019).", None, None,
   [W("jims-steak-and-spaghetti-house"), JBF19C]),
  ("The Humble Tomato", "Lewisburg", "855", "A full-service Italian restaurant in historic Lewisburg, cooking from scratch.", None, None, [W("the-humble-tomato")]),
 ],
 "ramps": [   # West Virginia Tourism's ramp-season guide (updated March 2026): restaurants that serve ramps in spring
  ("Mack's Bingo Kitchen", "Wardensville", "155", "Seasonal cooking from its own organic farm; ramps in spring.", None, None, [RAMPS, W("macks-bingo-kitchen")]),
  ("Ample Pizza", "Hico", "25385", "Pizza near the New River Gorge; ramps in spring.", None, None, [RAMPS]),
  ("Fish Hawk Acres", "Buckhannon", None, "A market, bakery and caterer with food from local farms; ramps in spring.", None, None, [RAMPS, W("fish-hawk-acres")]),
  ("Secret Sandwich Society", "Fayetteville", None, "Sandwiches and burgers with house-made spreads, pickles and chips; ramps in spring.", None, None,
   [RAMPS, W("secret-sandwich-society")]),
 ],
 "appalachian table": [
  ("1010 Bridge Restaurant", "Charleston", "1010", "Appalachian roots with a Lowcountry accent; Paul Smith won Best Chef: Southeast in 2024.", None, None,
   [W("1010-bridge-restaurant-catering"), JBF24W]),
  ("Alma Bea", "Shepherdstown", "202", "Mary Ellen Diaz's Shepherdstown restaurant, a 2026 James Beard finalist.", None, None, [JBF26N]),
  ("Mack's Bingo Kitchen", "Wardensville", "155", "An American restaurant cooking from its own organic farm and its neighbors'.", None, None, [W("macks-bingo-kitchen")]),
  ("Fish Hawk Acres", "Buckhannon", None, "Food sourced from local and regional farms: a bakery, deli and market.", None, None, [W("fish-hawk-acres")]),
 ],
 "historic inn": [
  ("The Main Dining Room at The Greenbrier", "White Sulphur Springs", "300", "The resort's grand dining room, celebrating more than a century of service.", None, None,
   [W("greenbriers-main-dining-room")]),
 ],
 "fish sandwich": [
  ("Coleman's Fish Market", "Wheeling", "2226", "The Centre Market fish market famous for its fish sandwich.", None, None, [W("colemans-fish-market")]),
 ],
 "oldest": [
  ("North End Tavern & Brewery", "Parkersburg", "3500", "A neighborhood tavern and brewery on Emerson Avenue.", 1899,
   "Tasting Table's oldest restaurant in every state (September 2025): West Virginia's is the North End Tavern & Brewery, opened in 1899.", [TT_OLDREST]),
 ],
}
# street addresses for places the map data doesn't show as a place to eat: from the official listing
ADDR = {("Fish Hawk Acres", "Buckhannon"): "5 W Main St", ("Secret Sandwich Society", "Fayetteville"): "103 Keller Ave"}
CUISINE = {("Country Club Bakery", "Fairmont"): "Bakery & Sweets", ("Tomaro's Bakery", "Clarksburg"): "Bakery & Sweets",
           ("D'Annunzio's Bakery", "Clarksburg"): "Bakery & Sweets", ("Home Industry Bakery", "Clarksburg"): "Bakery & Sweets",
           ("Bakers Nook", "Farmington"): "Bakery & Sweets", ("Fish Hawk Acres", "Buckhannon"): "Sandwiches & Deli",
           ("Secret Sandwich Society", "Fayetteville"): "Sandwiches & Deli", ("Morrison's Drive Inn", "Logan"): "Hot Dogs & Sausages",
           ("Hillbilly Hot Dogs", "Lesage"): "Hot Dogs & Sausages", ("The Custard Stand", "Webster Springs"): "Hot Dogs & Sausages",
           ("Jims Drive In", "Lewisburg"): "Hot Dogs & Sausages", ("Coleman's Fish Market", "Wheeling"): "Seafood"}
KINDS = {k: [k] for k in ("pepperoni roll", "hot dog", "italian classic", "ramps", "appalachian table", "historic inn", "fish sandwich", "oldest")}

# no MICHELIN Guide covers West Virginia (guide.michelin.com's West Virginia page answers 404)
MICHELIN = []
MI_MATCH = {}
MI_UT = None
# James Beard (facts with sources): West Virginia's wins (America's Classics 2019 and 2026, Best Chef: Southeast 2024) and its 2025-26
# nominees (finalists) and semifinalists; jamesbeard.org pages read 2026-11-05
SE = "Best Chef: Southeast"
JBF = [{"name": "1010 Bridge Restaurant", "city": "Charleston", "honors": [f"{SE} winner 2024 (Paul Smith)"], "sources": [JBF24W]},
       {"name": "Jim's Steak and Spaghetti House", "city": "Huntington", "honors": ["America's Classics 2019"], "sources": [JBF19C]},
       {"name": "Figaretti's Restaurant", "city": "Wheeling", "honors": ["America's Classics 2026"], "sources": [JBF26C]},
       {"name": "Alma Bea", "city": "Shepherdstown", "honors": [f"{SE} finalist 2026 (Mary Ellen Diaz)"], "sources": [JBF26N, JBF26]},
       {"name": "Ristorante Abruzzi", "city": "Charleston", "honors": [f"{SE} semifinalist 2025 (Chase Collier)"], "sources": [JBF25]}]
# closed, each with a source (none verified this pass)
CLOSED = []


def key(s):
    """The name key without a leading "the": "Varsity" is our "The Varsity"."""
    return re.sub(r"^the ", "", norm(s))


def find(name, town, num):
    k = key(name)
    hits = [i for i, n in enumerate(C["name"]) if C["city"][i] is not None and M["cities"][C["city"][i]] == town
            and (key(n) == k or key(n).startswith(k + " ") or k.startswith(key(n) + " ") or key(n).replace(" ", "") == k.replace(" ", "")
                 or (key(n).split()[:2] == k.split()[:2] and len(k.split()) >= 2))]
    if num:
        hits = [i for i in hits if (C["addr"][i] or "").split(" ")[0] == num]
    return hits


leads, n_out = [], {}
for kind, rows in GUIDES.items():
    out = []
    for name, town, num, note, founded, fnote, srcs in rows:
        hits = find(name, town, num)
        if not hits and (name, town) in ADDR:
            out.append({"name": name, "address": ADDR[(name, town)], "city": town, "zip": None, "kinds": KINDS[kind], "dishes": [], "note": note,
                        "founded": founded, "founded_note": fnote, "website": None, "open": True, "evidence_date": "2026-10",
                        "sources": srcs, "match_names": []} | ({"cuisine": CUISINE[(name, town)]} if (name, town) in CUISINE else {}))
            continue
        if len(hits) != 1:
            leads.append(f"- {kind}: {name} ({town}{', ' + num if num else ''}) — {len(hits)} matches in our data; not added"); continue
        i = hits[0]
        out.append({"name": C["name"][i], "address": C["addr"][i], "city": town, "zip": str(C["zip"][i]) if C["zip"][i] else None,
                    "kinds": KINDS[kind], "dishes": [], "note": note, "founded": founded, "founded_note": fnote, "website": None, "open": True,
                    "evidence_date": "2026-10", "sources": srcs, "match_names": [name.upper()] if norm(name) != norm(C["name"][i]) else []})
        if brand_of(norm_name(name)):   # a chain shows under its own spelling at every branch, whatever the listing says
            out[-1]["display"] = name
        if (name, town) in CUISINE:
            out[-1]["cuisine"] = CUISINE[(name, town)]
    fn = re.sub(r"[^a-z]+", "_", kind).strip("_")
    json.dump(out, open(f"{R}/app/{fn}.json", "w"), indent=1, ensure_ascii=False)
    n_out[kind] = len(out)

MI_ADDR = {}
json.dump({"restaurants": [{"name": n, "address": MI_ADDR.get(n), "city": t, "zip": None, "distinction": dist, "cuisine": cu, "green_star": False,
                             "michelin_url": MI_UT, "sources": [MI_UT], "match_names": [x.upper() for x in MI_MATCH.get(n, [])], "open": True}
                            for n, t, dist, cu in MICHELIN]}, open(f"{R}/michelin.json", "w"), indent=1, ensure_ascii=False)
json.dump([dict({"address": None}, **j, zip=None, open=True) for j in JBF], open(f"{R}/jbf.json", "w"), indent=1, ensure_ascii=False)
json.dump(CLOSED, open(f"{R}/closed.json", "w"), indent=1, ensure_ascii=False)
open(f"{R}/app/LEADS.md", "w").write("# West Virginia research leads (not yet verified)\n\nWritten by pipeline/build_research.py.\n\n" + "\n".join(leads) + """

## Waiting for a source we may use, or for the map data
- Pepperoni rolls: AB Cody's, Chico's and Mountain Top Convenience (on the trail) aren't in our map data under those names; Bonnie
  Belle's Pastries has two stores and the trail names no town.
- Hot dogs: Chum's Hotdogs (Marmet; WV Public's story is from 2021) and Super Weenie (South Charleston; the Department of Tourism's
  hot dog guide was last updated in 2020) wait for a 2025-26 page; Stewart's Original (Huntington) has no tourism listing we found.
- Historic inns: the General Lewis Inn and the Bavarian Inn have no tourism listing in the sitemap; the guide shows once it has three.
- Oldest: Country Club Bakery (1927, the first pepperoni roll) may have moved since; Figaretti's opened in 1948 (James Beard, 2026),
  but not necessarily at its Mount de Chantal Road address.
- Honors: Laury's (2023) and Appalachia Kitchen (2024) semifinalists are older than 2025; Lost Creek Farm (2022) isn't a restaurant open
  to walk in.
- Blocked hosts: wvgazettemail.com, herald-dispatch.com and wvnews.com disallow Claude's fetcher; the Digital Health Department portal
  disallows all crawlers (linked only).
""")
print(n_out, "| leads:", len(leads))
for l in leads: print(l)
