"""Download the Overture Maps extracts that westvirginia.py reads -> data/wv/

- overture_wv_bbox.parquet     every place in West Virginia's bounding box (name, category, address, point)
- overture_wv_sources.parquet  which datasets each West Virginia eating/drinking listing came from (Meta, Foursquare, ...)
- wv_shapes.json               simplified state and county outlines for the map
- wv_state_detail.geojson      the state outline at full detail, for the in-state test

Reads the public Overture bucket over S3 with DuckDB (no account needed). Ported from vt-eats/pipeline/fetch_overture.py.
West Virginia: land division areas; the "counties" are its 55. Most metros cross a state line (Huntington-Ashland, Wheeling, Weirton-
Steubenville, Parkersburg-Marietta, Bluefield, the Hagerstown fringe), so the script checks towns on both sides of each line.
"""
import os, json, time
import duckdb
from shapely import wkb
from shapely.geometry import mapping, Polygon

RELEASE = "2026-10-21.0"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "wv")
# West Virginia (42.73°N–45.02°N, 71.46°W–73.44°W) plus a margin for the border towns (Derby Line, the Upper Valley, Bennington's New York
# West Virginia (37.20°N–40.64°N, 77.72°W–82.65°W) plus a margin for the river towns on its lines
BBOX = "bbox.xmin BETWEEN -82.8 AND -77.6 AND bbox.ymin BETWEEN 37.1 AND 40.7"
EAT = "('restaurant','casual_eatery','bar','fast_food_restaurant','coffee_shop','cafe','smoothie_juice_bar','brewery','food_court')"
os.makedirs(OUT, exist_ok=True)

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial; SET s3_region='us-west-2';")
places = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=places/type=place/*.parquet"

t = time.time()
if not os.path.exists(f"{OUT}/overture_wv_bbox.parquet"):
    con.execute(f"""
COPY (
  SELECT id, names.primary AS name, basic_category AS cat, taxonomy.primary AS tax, taxonomy.hierarchy AS hier, confidence,
         operating_status AS status, brand.names.primary AS brand, addresses[1].freeform AS street, addresses[1].locality AS city,
         addresses[1].postcode AS zip, addresses[1].region AS region, ST_Y(geometry) AS lat, ST_X(geometry) AS lon, websites[1] AS web,
         phones[1] AS phone
  FROM read_parquet('{places}', hive_partitioning=1) WHERE {BBOX}
) TO '{OUT}/overture_wv_bbox.parquet' (FORMAT PARQUET)""")
    print("places in bbox", round(time.time() - t), "s", flush=True)
if not os.path.exists(f"{OUT}/overture_wv_sources.parquet"):
    con.execute(f"""
COPY (
  SELECT id, list_transform(sources, lambda x: x.dataset) AS ds, list_transform(sources, lambda x: x.update_time) AS ut,
         list_transform(sources, lambda x: x.record_id) AS rid,
         len(socials) AS n_soc, len(websites) AS n_web, len(phones) AS n_ph
  FROM read_parquet('{places}', hive_partitioning=1)
  WHERE {BBOX} AND basic_category IN {EAT}
) TO '{OUT}/overture_wv_sources.parquet' (FORMAT PARQUET)""")
    print("sources", round(time.time() - t), "s", flush=True)

areas = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=divisions/type=division_area/*.parquet"
rows = con.execute(f"""
  SELECT subtype, names.primary AS name, ST_AsWKB(geometry) AS g
  FROM read_parquet('{areas}', hive_partitioning=1)
  WHERE country = 'US' AND region = 'US-WV' AND subtype IN ('region', 'county') AND class = 'land'
    AND bbox.xmin > -82.9 AND bbox.xmax < -77.5 AND bbox.ymin > 37.0 AND bbox.ymax < 40.8""").fetchall()


def rings(geom, tol, min_area):
    geom = geom.simplify(tol, preserve_topology=True)
    polys = [p for p in getattr(geom, "geoms", [geom]) if p.geom_type == "Polygon" and p.area >= min_area]
    return [[[round(x, 3), round(y, 3)] for x, y in p.exterior.coords] for p in polys]


out = {"state": None, "counties": []}
for sub, name, g in rows:
    geom = wkb.loads(bytes(g)).buffer(0)
    if sub == "region":
        json.dump(mapping(geom.simplify(0.0005, preserve_topology=True)), open(f"{OUT}/wv_state_detail.geojson", "w"))
        out["state"] = [[r] for r in rings(geom, 0.002, 0.000005)]
    else:
        out["counties"].append({"name": name, "c": rings(geom, 0.004, 0.00002)})
# full-detail county polygons for assigning each place to a county (not shipped)
json.dump({name: mapping(wkb.loads(bytes(g)).buffer(0).simplify(0.0003, preserve_topology=True))
           for sub, name, g in rows if sub == "county"}, open(f"{OUT}/wv_counties_detail.geojson", "w"))
json.dump(out, open(f"{OUT}/wv_shapes.json", "w"), separators=(",", ":"))
print("outlines: state", len(out["state"] or []), "rings +", len(out["counties"]), "counties;", round(time.time() - t), "s total")
# river and border towns: each must fall on the right side of the detailed state outline
from shapely.geometry import shape, Point
st = shape(json.load(open(f"{OUT}/wv_state_detail.geojson")))
for nm, lon, lat, want in [("Huntington", -82.4452, 38.4192, True), ("Ashland, KY", -82.6379, 38.4784, False), ("Wheeling", -80.7209, 40.0640, True),
                           ("Bridgeport, OH", -80.7398, 40.0698, False), ("Weirton", -80.5895, 40.4189, True), ("Steubenville, OH", -80.6340, 40.3698, False),
                           ("Parkersburg", -81.5615, 39.2667, True), ("Marietta, OH", -81.4548, 39.4154, False), ("Bluefield, WV", -81.2223, 37.2698, True),
                           ("Bluefield, VA", -81.2709, 37.2501, False), ("Harpers Ferry", -77.7389, 39.3254, True), ("Hagerstown, MD", -77.7200, 39.6418, False),
                           ("Charleston", -81.6326, 38.3498, True), ("Morgantown", -79.9559, 39.6295, True), ("Point Marion, PA", -79.9026, 39.7376, False)]:
    ok = st.contains(Point(lon, lat))
    print(f"  {nm}: {'inside' if ok else 'outside'}{'' if ok == want else '  <-- WRONG'}")
print("counties:", len(out["counties"]), sorted(c["name"] for c in out["counties"]))

# the neighbours' land (Ohio, Pennsylvania, Maryland, Virginia, Kentucky): listings.py widens West Virginia's outline ~300 m for river
# banks, but only where no neighbour's land is, so an Ohio or Kentucky listing across the river stays out
nb = con.execute(f"""
  SELECT region, ST_AsWKB(geometry) FROM read_parquet('{areas}', hive_partitioning=1)
  WHERE country = 'US' AND region IN ('US-OH', 'US-PA', 'US-MD', 'US-VA', 'US-KY') AND subtype = 'region' AND class = 'land'""").fetchall()
from shapely.ops import unary_union
from shapely.geometry import box
near = box(-82.9, 37.0, -77.5, 40.8)
nbg = unary_union([wkb.loads(bytes(g)).buffer(0).intersection(near) for _, g in nb])
json.dump(mapping(nbg.simplify(0.0002, preserve_topology=True)), open(f"{OUT}/wv_neighbors.geojson", "w"))
print("neighbours:", sorted(r for r, _ in nb))
