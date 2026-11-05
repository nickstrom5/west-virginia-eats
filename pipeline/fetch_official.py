"""West Virginia's open official records -> data/raw/official/ (git-ignored, never public). Nothing to fetch yet.

Checked 2026-11-05 (playbook/12-sources.md): the local health departments' Digital Health Department portal is search-only and its
robots.txt disallows all crawlers; the state publishes no inspection results; the ABCA license search's CSV download posts no terms.
When a list we may use turns up (an LHD export Nick approves), add its loader to official.py and its download here.
"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "official")
os.makedirs(OUT, exist_ok=True)
json.dump({}, open(os.path.join(OUT, "meta.json"), "w"))
print("West Virginia: no official list to fetch (see the docstring)")
