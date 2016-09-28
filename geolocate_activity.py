from stats.models import NetInfo
import json

def count_for_session(s):
    count = 0
    for le in s.events.all():
        count += le.frequency
    return count

count = {}

for info in NetInfo.objects.all():
    pos = (float(info.longitude), float(info.latitude))
    if info.city == "Unknown":
        # We need to check if there's any mapping ability to
        # determine if this info should belong to another one
        # This is true if the machine/user are the same on a different net info
        for session in info.session_set.all():
            m = session.machine
            for o_session in m.session_set.all():
                if o_session.id == session.id:
                    continue
                if o_session.user.hashed_username != session.user.hashed_username:
                    continue
                if o_session.netInfo.ip == session.netInfo.ip:
                    continue
                pos = (float(o_session.netInfo.longitude), float(o_session.netInfo.latitude))
                count[pos] = count.get(pos, 0) + count_for_session(session)
    else:
        for session in info.session_set.all():
            count[pos] = count.get(pos, 0) + count_for_session(session)

points = [{"latitude": k[1], "longitude": k[0], "count": c} for k, c in count.iteritems()]

with open("geolocate_activity.json", "w") as f:
    json.dump(points, f)

