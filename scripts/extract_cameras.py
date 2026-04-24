import json
import os
import sys

import osmium

"""
Filtering:
    osmium extract \
      -b -117.6,32.6,-116.9,33.1 \
      -s smart \
      -o san-diego.osm.pbf \
      socal-260423.osm.pbf
"""


class ALPRHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.features = []

    def check_tags(self, tags):
        if tags.get("man_made") != "surveillance":
            return False

        values = []

        for key in ["surveillance:type", "surveillance", "camera:type"]:
            if key in tags:
                values.extend(tags[key].lower().split(";"))

        values = [v.strip() for v in values]

        return any(v in ["alpr", "anpr"] for v in values)

    def node(self, n):
        if self.check_tags(n.tags):
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [n.location.lon, n.location.lat],
                },
                "properties": {k: v for k, v in n.tags},
            }
            self.features.append(feature)

    def way(self, w):
        if self.check_tags(w.tags):
            if len(w.nodes) > 0:
                n = w.nodes[0]
                if n.location.valid():
                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [n.location.lon, n.location.lat],
                        },
                        "properties": {k: v for k, v in w.tags},
                    }
                    self.features.append(feature)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_cameras.py <osm_pbf_file>")
        sys.exit(1)

    osm_file = sys.argv[1]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.abspath(
        os.path.join(script_dir, "..", "flaskr", "san_diego_alprs.geojson")
    )

    print(f"Scanning {osm_file} for ALPRs...")

    handler = ALPRHandler()
    handler.apply_file(osm_file, locations=True)

    feature_collection = {"type": "FeatureCollection", "features": handler.features}

    with open(output_file, "w") as f:
        json.dump(feature_collection, f, separators=(",", ":"))

    print(f"Extracted {len(handler.features)} cameras to {output_file}")
