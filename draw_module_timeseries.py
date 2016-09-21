import json, vcs, cdms2, numpy



with open("data/module_activity.json") as f:
    data = json.load(f)


import cdtime
variables = []
minval = 0
maxval = 0

for module in data:
    times = data[module].keys()

    real_times = []
    for t in times:
        year, month, day = [int(c) for c in t.split("-")]
        real_time = cdtime.comptime(year, month, day)
        real_times.append(real_time)
    real_times.sort()

    time_arr = numpy.ndarray((len(real_times),))
    units = "days since %d-%d-%d" % (real_times[0].year, real_times[0].month, real_times[0].day)
    for i, t in enumerate(real_times):
        rel = t.torel(units)
        time_arr[i] = rel.value

    time_axis = cdms2.createAxis(time_arr, id="time")
    time_axis.units = units
    value_arr = numpy.ndarray((len(real_times),))

    for i, t in enumerate(real_times):
        value_arr[i] = data[module]["%d-%d-%d" % (t.year, t.month, t.day)]

    variable = cdms2.createVariable(value_arr, axes=[time_axis], id=str(module))
    variables.append(variable)
    maxval = max(maxval, variable.max())

x = vcs.init()
oned = vcs.create1d()
oned.datawc_y1 = minval
oned.datawc_y2 = maxval

t = vcs.createtemplate()
t_dud = vcs.createtemplate()
t_dud.blank()
t_dud.data.priority = 1

x.plot(variables[0], oned, t)
for v in variables[1:]:
    x.plot(v, oned, t_dud)

x.png("module_timeseries")
