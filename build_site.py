"""Build a deployable static site from source and a TransLink GTFS feed."""

import argparse
import csv
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.request import Request, urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
FEED_URL = "https://gtfs-static.translink.ca/gtfs/google_transit.zip"
STATIC_FILES = ("index.html", "script.js", "style.css", "sw.js", "manifest.json")
JSON_FILES = ("train_journeys.json", "station_schedules.json", "transit_routes.geojson")
FEED_FILES = ("trips.txt", "stop_times.txt", "stops.txt", "routes.txt", "calendar.txt", "calendar_dates.txt", "shapes.txt", "feed_info.txt")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gtfs-zip", type=Path, help="Use a local feed ZIP instead of downloading")
    parser.add_argument("--date", help="Service date (YYYY-MM-DD); default: today in Vancouver")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    env = os.environ.copy()
    if args.date:
        env["TRANSIT_SERVICE_DATE"] = args.date

    with tempfile.TemporaryDirectory(prefix="transit-build-") as directory:
        stage = Path(directory)
        feed_zip = args.gtfs_zip
        if feed_zip is None:
            feed_zip = stage / "gtfs.zip"
            print(f"Downloading {FEED_URL}", flush=True)
            request = Request(FEED_URL, headers={"User-Agent": "vancouver-transit-tracker"})
            with urlopen(request, timeout=120) as response, feed_zip.open("wb") as output:
                shutil.copyfileobj(response, output)
        feed_dir = stage / "google_transit"
        feed_dir.mkdir()
        with ZipFile(feed_zip) as archive:
            for name in FEED_FILES:
                # Extract only the known root-level GTFS files, never arbitrary ZIP paths.
                with archive.open(name) as source, (feed_dir / name).open("wb") as output:
                    shutil.copyfileobj(source, output)

        for name in ("format_data.py", "extract_routes.py"):
            shutil.copy2(ROOT / name, stage / name)
            subprocess.run([sys.executable, name], cwd=stage, env=env, check=True)

        for name in JSON_FILES:
            path = stage / name
            data = json.loads(path.read_text(encoding="utf-8"))
            if not data or (name.endswith("geojson") and not data.get("features")):
                raise RuntimeError(f"Refusing to deploy empty {name}; check feed dates and route IDs")
            path.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=True) + "\n", encoding="utf-8")
        with (stage / "stations_for_map.csv").open(encoding="utf-8", newline="") as source:
            if not list(csv.DictReader(source)):
                raise RuntimeError("Refusing to deploy an empty station map")

        args.output.mkdir(parents=True, exist_ok=True)
        for name in STATIC_FILES:
            shutil.copy2(ROOT / name, args.output / name)
        for name in (*JSON_FILES, "stations_for_map.csv"):
            shutil.copy2(stage / name, args.output / name)
        (args.output / ".nojekyll").touch()
        print(f"Site built in {args.output}", flush=True)


if __name__ == "__main__":
    main()
