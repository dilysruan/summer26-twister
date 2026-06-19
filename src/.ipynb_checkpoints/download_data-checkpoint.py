"""
Download all raw data for the tornado radar placement analysis.

Sources:
  - NOAA Storm Events details CSVs (1990–2025)
  - NEXRAD WSR-88D site list (NWS radar API)
  - US Census 2020 county population estimates
  - Census TIGER simplified county boundaries (20m)
"""

import os
import re
import time
import json
import shutil
import requests
from html.parser import HTMLParser

RAW = "../data/raw"
os.makedirs(RAW, exist_ok=True)

STORM_EVENTS_BASE = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
NEXRAD_API = "https://api.weather.gov/radar/stations"
CENSUS_POP_URL = (
    "https://www2.census.gov/programs-surveys/popest/datasets/"
    "2020-2023/counties/totals/co-est2023-alldata.csv"
)
TIGER_COUNTY_URL = (
    "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_20m.zip"
)


def _download(url, dest, desc=""):
    if os.path.exists(dest):
        print(f"  [skip] {os.path.basename(dest)} already exists")
        return dest
    label = desc or os.path.basename(dest)
    print(f"  Downloading {label} ...", end=" ", flush=True)
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 16):
            f.write(chunk)
    print(f"saved → {os.path.basename(dest)}")
    return dest


class _LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self.links.append(v)


def download_storm_events(start_year=1990, end_year=2025):
    print("\n=== NOAA Storm Events ===")
    r = requests.get(STORM_EVENTS_BASE, timeout=120)
    r.raise_for_status()
    parser = _LinkParser()
    parser.feed(r.text)

    year_file = {}
    for link in parser.links:
        m = re.match(r"StormEvents_details-ftp_v1\.0_d(\d{4})_c\d+\.csv\.gz$", link)
        if m:
            yr = int(m.group(1))
            if start_year <= yr <= end_year:
                if yr not in year_file or link > year_file[yr]:
                    year_file[yr] = link

    downloaded = []
    for yr in sorted(year_file):
        fname = year_file[yr]
        dest = RAW + "/" + fname
        _download(STORM_EVENTS_BASE + fname, dest, f"Storm Events {yr}")
        downloaded.append(dest)
        time.sleep(0.1)

    print(f"  Storm Events: {len(downloaded)} files downloaded/verified.")
    return downloaded


def download_nexrad_sites():
    print("\n=== NEXRAD Sites ===")
    dest = RAW + "/nexrad_sites.json"
    if os.path.exists(dest):
        print(f"  [skip] {os.path.basename(dest)} already exists")
        return dest
    print("  Fetching radar station list from api.weather.gov ...", end=" ", flush=True)
    r = requests.get(NEXRAD_API, timeout=120, headers={"Accept": "application/geo+json"})
    r.raise_for_status()
    data = r.json()
    features = [
        f for f in data.get("features", [])
        if f.get("properties", {}).get("stationType") == "WSR-88D"
    ]
    with open(dest, "w") as fh:
        json.dump({"type": "FeatureCollection", "features": features}, fh, indent=2)
    print(f"saved → {os.path.basename(dest)}  ({len(features)} WSR-88D stations)")
    return dest


def download_census_population():
    print("\n=== Census Population ===")
    dest = RAW + "/co-est2023-alldata.csv"
    return _download(CENSUS_POP_URL, dest, "Census county population estimates 2020-2023")


def download_tiger_counties():
    print("\n=== TIGER County Boundaries ===")
    zip_dest = RAW + "/cb_2020_us_county_20m.zip"
    _download(TIGER_COUNTY_URL, zip_dest, "TIGER county shapefile (20m)")
    shp_dir = RAW + "/cb_2020_us_county_20m"
    if not os.path.exists(shp_dir):
        print(f"  Unzipping {os.path.basename(zip_dest)} ...", end=" ", flush=True)
        shutil.unpack_archive(zip_dest, shp_dir)
        print("done")
    return shp_dir


def main():
    print(f"Raw data directory: {os.path.abspath(RAW)}")
    download_storm_events()
    download_nexrad_sites()
    download_census_population()
    download_tiger_counties()
    print("\nAll data download complete.")


if __name__ == "__main__":
    main()
