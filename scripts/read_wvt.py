"""Read West Virginia Tourism company listings (wvtourism.com/company/<slug>/; robots allows them) -> data/research/raw/wvt.json: the
listing's name, address and description, one polite request every 1.5 s. Private research notes only.
Usage: .venv/bin/python scripts/read_wvt.py <slug> ..."""
import html, json, os, re, sys, time
import requests
UA = "WestVirginiaEatsSourceCheck/1.0 (+https://nickstrom5.github.io/west-virginia-eats/; nick@eatsranked.com)"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "research", "raw", "wvt.json")
have = json.load(open(OUT)) if os.path.exists(OUT) else {}
for slug in sys.argv[1:]:
    url = slug if slug.startswith("http") else f"https://wvtourism.com/company/{slug.strip('/')}/"
    if url in have:
        continue
    r = requests.get(url, headers={"User-Agent": UA}, timeout=40)
    t = r.text
    title = re.search(r"<title>(.*?)</title>", t, re.S)
    name = html.unescape(title.group(1)).split(" - Almost Heaven")[0].strip() if title else None
    ad = re.search(r'class="address"[^>]*>(.*?)</a>', t, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', t, re.S)
    rec = {"status": r.status_code, "name": name, "addr": html.unescape(ad.group(1)).strip() if ad else None,
           "desc": html.unescape(desc.group(1)).strip() if desc else ""}
    have[url] = rec
    print(r.status_code, rec["name"], "|", rec["addr"], "|", rec["desc"][:200], flush=True)
    json.dump(have, open(OUT, "w"), indent=1, ensure_ascii=False)
    time.sleep(1.5)
