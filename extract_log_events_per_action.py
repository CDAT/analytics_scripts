from stats.models import Action
import json
import datetime
from django.utils import timezone

modules_tracked = "cdutil", "genutil", "cdms2", "vcs"

actions = []
modules = {}

for a in Action.objects.all():
    for m in modules_tracked:
        if a.name.startswith(m):
            actions.append(a)
            modules[a.name] = m
            break
    else:
        continue

events = {}
one_day = datetime.timedelta(1)

for action in actions:
    print "Handling", action.name
    timeseries = events.get(modules[action.name], {})
    print "Retrieving log events..."
    for logevent in action.logevent_set.all():
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
            count = timeseries.get(date_of_event, 0)
            count += logevent.frequency / len(dates)
            timeseries[date_of_event] = count

    events[modules[action.name]] = timeseries

with open("module_activity.json", "w") as f:
    json.dump(events, f)
