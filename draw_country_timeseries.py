import json, vcs, cdms2, numpy



with open("data/activity_by_country_timeseries.json") as f:
    data = json.load(f)


import cdtime
variables = []
mindate = None
maxdate = None

minval = 0
maxval = 0

for country in data:
    times = data[country].keys()

    real_times = []
    for t in times:
        year, month, day = [int(c) for c in t.split("-")]
        real_time = cdtime.comptime(year, month, day)
        real_times.append(real_time)
    real_times.sort()

    time_arr = numpy.ndarray((len(real_times),))
    units = "days since 2000"
    for i, t in enumerate(real_times):
        rel = t.torel(units)
        time_arr[i] = rel.value

    time_axis = cdms2.createAxis(time_arr, id="time")
    time_axis.units = units
    value_arr = numpy.ndarray((len(real_times),))

    for i, t in enumerate(real_times):
        value_arr[i] = data[country]["%d-%d-%d" % (t.year, t.month, t.day)]
    # Values are too darn big
    variable = cdms2.MV2.log10(cdms2.createVariable(value_arr, axes=[time_axis], id=str(country)))
    variable.id = str(country)
    variables.append(variable)
    start_date = cdtime.reltime(time_axis[0], time_axis.units).tocomp()
    end_date = cdtime.reltime(time_axis[-1], time_axis.units).tocomp()

    if mindate is None:
        mindate = start_date
    else:
        mindate = min(start_date, mindate)

    if maxdate is None:
        maxdate = end_date
    else:
        maxdate = max(maxdate, end_date)

    maxval = max(maxval, variable.max())

x = vcs.init()
oned = vcs.create1d()
oned.datawc_y1 = minval
oned.datawc_y2 = maxval
oned.datawc_x1 = mindate
oned.datawc_x2 = maxdate

scale = vcs.utils.mkscale(minval, maxval)
labels = numpy.array(scale)
labels = (10 ** labels)
labels = numpy.round(labels, 0)
labels = list(labels)
labels[0] = 0

nice_labels = []
for i in range(len(labels)):
    val = int(labels[i])
    if val >= 1000:
        val = val / 1000
        val = "%dk" % val
    nice_labels.append(str(val))

oned.yticlabels1 = {s: l for s, l in zip(scale, nice_labels)}
oned.linewidth = 2


t = vcs.createtemplate()
t.blank()
t.data.priority = 1
t.data.x1 = .1
t.data.x2 = .9
t.box1.priority = 1
t.box1.x1 = .1
t.box1.x2 = .9
t.ytic1.priority = 1
t.ytic1.x1 = .1
t.ytic1.x2 = .09
t.ylabel1.x = .09
t.ylabel1.priority = 1
t.xlabel1.priority = 1
t.xtic1.priority = 1

t_dud = vcs.createtemplate(source=t)
t_dud.blank()
t_dud.data.priority = 1

templates = [t] + [t_dud] * (len(variables) - 1)
colors = ["#D00000", "#E1CA96", "#3EC300", "#B7FDFE", "#14213D", "#8E5572", "#F5BB00", "#694873"]
rgbs = []
for c in colors:
    r = int(c[1:3], 16) / 2.56
    g = int(c[3:5], 16) / 2.56
    b = int(c[5:], 16) / 2.56
    rgbs.append([r, g, b])
colors = rgbs[:len(variables)]

legend = vcs.createfillarea()
legend.x = []
legend.y = []
legend.color = []
legend.viewport = [.1, .9, .05, t.xlabel1.y - .05]

legend_labels = vcs.createtext()
legend_labels.x = []
legend_labels.y = []
legend_labels.string = []
legend_labels.valign = "top"
legend_labels.halign = "center"
legend_labels.color = "black"
legend_labels.viewport = legend.viewport
oned.markersize = 5
for i, c, v, t in zip(range(len(variables)), colors, variables, templates):
    legend.x.append([i / float(len(variables)), (i + 1) / float(len(variables)), (i + 1) / float(len(variables)), (i) / float(len(variables))])
    legend.y.append([.25, .25, .5, .5])
    legend.color.append(c)
    legend_labels.string.append(v.id)
    legend_labels.x.append((legend.x[i][0] + legend.x[i][1])/2)
    legend_labels.y.append(.2)
    oned.linecolor = c
    oned.markercolor = c
    x.plot(v, oned, t)

x.plot(legend)
x.plot(legend_labels)

title = vcs.createtext()
title.height = 24
title.string = "Total events by country over time"
title.x = .5
title.y = .95
title.halign = "center"
title.valign = "top"

x.plot(title)

axis_info = vcs.createtext()
axis_info.angle = 270
axis_info.string = "Number of events"
axis_info.x = .02
axis_info.y = (t.data.y2 - t.data.y1) / 2. + t.data.y1
axis_info.valign = "top"
axis_info.halign = "center"
x.plot(axis_info)
x.png("country_timeseries")
