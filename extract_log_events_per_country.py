from stats.models import NetInfo
import json
import datetime
from django.utils import timezone

one_day = datetime.timedelta(1)

count = {}

for info in NetInfo.objects.all():
    pos = str(info.country)
    print pos
    if pos == "--":
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
                if info.country != "--":
                    continue
                print "matched session", pos, info.country
                pos = info.country
                break
        else:
            continue
    timeseries = count.get(pos, {})
    for session in info.session_set.all():
        for logevent in session.events.all():
            start = logevent.session.startDate
            end = logevent.session.lastDate

            num_days = 0
            d = end
            dates = [end]
            while d > start:
                d = d - one_day
                dates.append(d)
            if logevent.frequency < len(dates):
                # Division is going to round badly.
                d = "%d-%d-%d" % (dates[0].year, dates[0].month, dates[0].day)
                timeseries[d] = timeseries.get(d, 0) + logevent.frequency
                continue
            for date in dates:
                date_of_event = "%d-%d-%d" % (date.year, date.month, date.day)
                c = timeseries.get(date_of_event, 0)
                c += logevent.frequency / len(dates)
                timeseries[date_of_event] = c
    count[pos] = timeseries

with open("activity_by_country_timeseries.json", "w") as f:
    json.dump(count, f)
