# West Virginia sources and calibration (checked 2026-11-05)

## Official sources
| Source | What it has | Can a script read it? | Used |
|---|---|---|---|
| Local health departments (64CSR17; oehs.wvdhhr.org/phs/food-safety/, which says permits and inspections are the LHDs' job) | inspections | no results as data | the Food Safety page is linked from every place |
| Digital Health Department portal (inspections.myhealthdepartment.com/<slug>, 25 LHDs) | reports | no: search-only, robots.txt disallows all crawlers incl. ClaudeBot | not read |
| ABCA license search (wvabca.com/licensesearch.aspx) | on-premise licenses, CSV download | a form; no terms posted | no: Nick's call |

## Calibration
- Census CBP 2023: 3,271 NAICS 722 establishments (the prompt). Overture: 7,179 eating and drinking listings; 7,148 after cleaning;
  the keep rule keeps 3,500; the App Store build ships **3,414 places, 3,339 restaurants** (55 counties).
- Google 2021 (private, web build only): 4,403 WV food listings, 3,191 matched.
- Website links: 1,578 OK after the check.

## Research sources (each place cites its own)
- West Virginia Tourism's company listings (wvtourism.com/company/<slug>, 2,503 in its sitemap; robots allows them), read by
  scripts/read_wvt.py; its Pepperoni Roll Trail page (updated 2025-10-23) and ramp-season guide (updated 2026-03-11).
- Tasting Table's oldest restaurant in every state (2025-09-23): North End Tavern & Brewery, Parkersburg, 1899.
- jamesbeard.org: 2026 nominees and semifinalists, 2025 semifinalists, 2024 winners, 2019 and 2026 America's Classics.
- Not usable: wvgazettemail.com, herald-dispatch.com, wvnews.com (robots disallow Claude's fetcher).
