# Vancouver Transit Real-Time Tracker

An interactive map that visualizes Vancouver's transit network, showing scheduled positions of SkyTrains, RapidBus, 99 B-Line, and SeaBus based on official TransLink GTFS schedule data.

## ✨ Key Features

-   🚊 **Schedule-based vehicle tracking** with smooth animations
-   🗺️ **Interactive map** with route overlays and station markers
-   📱 **Mobile-optimized** Progressive Web App (PWA)
-   ⏱️ **Live arrival times** at stations
-   🛤️ **Realistic route following** with accurate vehicle movement

## 🚇 Supported Services

-   **SkyTrain:** Expo, Millennium, and Canada Lines
-   **RapidBus:** All R-Line services (R1-R6)
-   **99 B-Line:** Broadway/10th Avenue service
-   **SeaBus:** Waterfront ↔ Lonsdale Quay

## 🚀 Quick Start

### Prerequisites

- Python 3.13 and internet access for the feed download
- A web browser

### Build and preview

```bash
python -m pip install -r requirements.txt
python build_site.py
python -m http.server 8000 --directory dist
```

Open http://localhost:8000. The build downloads the current TransLink GTFS feed,
generates schedules for today's date in Vancouver, and packages only browser
assets and compact generated data into `dist/`. Raw feeds and generated files
are ignored by Git.

For a reproducible build with an archived feed and service date:

```bash
python build_site.py --gtfs-zip path/to/feed.zip --date 2025-09-13
```

The requested service date must be covered by that feed. Empty schedules fail the
build before a deployment artifact is published.

### GitHub Pages

Set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**.
The workflow builds and deploys on pushes to `main`, on manual dispatch, and near
Vancouver midnight each day. A failed build prevents the deployment job from
running, preserving the previous deployment. No workflow commits data to Git.
Schedules remain estimates based on GTFS; this is not a real-time vehicle feed.

### History migration

The repository history was filtered to remove `google_transit/` and historical
generated CSV, JSON, and GeoJSON files. Source commit authors, dates, and messages
were retained; commits containing only removed data may disappear. Existing
clones should be replaced with a fresh clone rather than merged into this history.

## 📊 Data Source

Uses official [TransLink GTFS data](https://www.translink.ca/about-us/doing-business-with-translink/app-developer-resources/gtfs/gtfs-data) downloaded during the build into a temporary `google_transit/` directory. The feed is not stored in Git.

## 🎨 Features

### Vehicle Movement

-   Realistic timing (30s stops for trains/buses, 3min for SeaBus)
-   Schedule-based route following
-   Smooth animations

### User Interface

-   Touch-friendly mobile controls
-   Route toggle button (🚇)
-   Live arrival countdowns
-   Dark/light mode support
-   PWA installation support

### Transit Colors

-   **Expo Line:** Blue (#005dab)
-   **Millennium Line:** Yellow (#ffd204)
-   **Canada Line:** Teal (#009ac7)
-   **RapidBus:** Green (#009f4a)
-   **99 B-Line:** Orange (#f37a22)
-   **SeaBus:** Brown (#87746b)
