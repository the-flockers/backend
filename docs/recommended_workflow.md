# Recommended Workflow

Generally, production processes will follow this:

1. Every so often, you'll need to refresh the map of ALPRs as locations change. Currently, _there is no automated way to do so_. Our map is sourced from OpenStreetMap data provided by Geofabrik [here](https://download.geofabrik.de/north-america/us/california/socal.html).

2. Run this command to bound the map to the San Diego area (requires [Osmium](https://osmcode.org/osmium-tool/)):
```
osmium extract \
  -b -117.6,32.6,-116.9,33.1 \
  -s smart \
  -o san-diego.osm.pbf \
  socal-260423.osm.pbf
```

3. The `docker-compose.yml` file handles camera extract automatically in addition to setting up the ORS instance in the same network:
```
docker-compose up -d --build
```
