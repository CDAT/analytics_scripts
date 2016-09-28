import vcs
import json
import cdms2
import numpy


with open("data/geolocate_activity.json") as f:
    geo_data = json.load(f)

template = vcs.createtemplate()
template.blank()
template.data.priority = 1
template.box1.priority = 1
template.xtic1.priority = 1
template.ytic1.priority = 1
template.xlabel1.priority = 1
template.ylabel1.priority = 1

base_marker = vcs.createmarker()
base_marker.worldcoordinate = [-180, 180, -90, 90]
base_marker.viewport = [template.data.x1, template.data.x2, template.data.y1, template.data.y2]

max_count = 0
for p in geo_data:
    max_count = max(p["count"], max_count)

markers = {
}

zeroes = cdms2.MV2.ones((180, 360))
lon = cdms2.createAxis(numpy.arange(-180, 180, 1), id="lon")
lat = cdms2.createAxis(numpy.arange(-90, 90, 1), id="lat")
zeroes.setAxis(1, lon)
zeroes.setAxis(0, lat)

for p in geo_data:
    size = int(p["count"] / float(max_count) * 9)
    marker = markers.get(size, None)
    if marker is None:
        marker = vcs.createmarker(source=base_marker)
        marker.x = []
        marker.y = []
        marker.size = range(0, 10)[size] + 2
        markers[size] = marker
    marker.x.append(p["longitude"])
    marker.y.append(p["latitude"])

x = vcs.init()
blanked = vcs.createisofill()
blanked.levels = [1, 1]
blanked.fillareacolors = [0, 0,0,0]

x.plot(zeroes, blanked, template)
for _, marker in markers.items():
    x.plot(marker)

x.png("geo")