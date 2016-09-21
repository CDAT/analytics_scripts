import json
from draw_barchart import pct_barchart

with open("data/version_activity_histo.json") as f:
    histo_data = json.load(f)

def get_version(v):
    values = v.split(".")
    if len(values) < 3:
        values = (values[0], values[1], 0)
    return tuple([int(v) for v in values])

version_mapped = {get_version(k): v for k, v in histo_data.items()}
versions = sorted(version_mapped.keys())
values = [version_mapped[v] for v in versions]
labels = [".".join([str(ver) for ver in v]) for v in versions]
canvas = pct_barchart(values, labels, "% Total Events from Last 30 days by Version of UV-CDAT")
canvas.png("events_by_version.png")

with open("data/version_activity_by_session.json") as f:
    histo_data = json.load(f)

version_mapped = {get_version(k): v for k, v in histo_data.items()}
versions = sorted(version_mapped.keys())
values = [version_mapped[v] for v in versions]
labels = [".".join([str(ver) for ver in v]) for v in versions]
canvas = pct_barchart(values, labels, "% Total Sessions from Last 30 days by Version of UV-CDAT")
canvas.png("sessions_by_version.png")