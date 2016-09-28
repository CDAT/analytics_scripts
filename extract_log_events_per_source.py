from stats.models import Source
import re
import datetime
import json


sources = []

for source in Source.objects.all():
    if "CDAT" in source.name:
        sources.append(source)

versions = {}

# Clean up versions
for s in sources:
    version = s.version
    if version[0] == "v":
        version = version[1:]

    if version.startswith("uvcdat-"):
        version = version[7:]
    version = re.sub(r"-.*", "", version)
    version = re.sub(r"\.?rc.*", "", version)

    versions[s.version] = version

activity = {}

today = datetime.datetime.now()
# We're only looking in the last 30 days
period = datetime.timedelta(30)

for source in sources:
    real_version = versions[source.version]
    count = activity.get(real_version, 0)
    for le in source.logevent_set.all():
        session = le.session
        if session.lastDate - today > period:
            continue
        count += le.frequency
    activity[real_version] = count

with open("version_activity_histo.json", "w") as f:
    json.dump(activity, f)
