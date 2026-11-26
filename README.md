# Armenia GTFS (research draft)

BASA only. Not for public journey planning. Historical fleet/cycle estimates, assumed 05:00–22:00 departure window, weekdays excluding Colombian holidays. Stops are proximity candidates within 30 m, not verified boarding sequences. R28 second ID block retained provisionally. See [research status](docs/research-status.md).

```sh
pip install -r requirements.txt
python fetch_data.py
python generate.py --start 2026-11-26 --end 2027-02-28 --allow-estimates
```

CI fetches current source snapshots rather than the original local snapshots, so counts may differ. Existing local data files are reused when present. No SETP-only routes or raw vehicle data are exported. OpenStreetMap data © OpenStreetMap contributors, ODbL (https://www.openstreetmap.org/copyright). Verify BASA redistribution rights before public release. No production release is configured.
