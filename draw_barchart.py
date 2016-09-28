import json, vcs


def pct_barchart(values, labels=None, title=None):
    x = vcs.init()

    total_y = sum(values)
    count = len(values)

    fill_width = .8
    fill_height = .8

    per_bar_width = fill_width / float(count)
    per_bar_fill_width = per_bar_width - per_bar_width * .05

    fill = vcs.createfillarea()
    fill.x = [[.1 + i * per_bar_width] * 2 + [.1 + i * per_bar_width + per_bar_fill_width] * 2 for i in range(count)]
    fill.y = [[.1, .1 + values[i] / float(total_y), .1 + values[i] / float(total_y), .1] for i in range(count)]
    fill.color = vcs.getcolors(range(len(values)))
    x.plot(fill)

    if labels is None:
        labels = [str(i) for i in range(count)]

    xlabel = vcs.createtext()
    xlabel.string = labels
    xlabel.x = [sum(fill.x[i][1:3]) / 2. for i in range(count)]
    xlabel.y = [.09]
    xlabel.valign = "top"
    xlabel.halign = "center"
    x.plot(xlabel)

    pctlabel = vcs.createtext()
    pctlabel.string = [ "%.03f%%" % (values[i] / float(total_y) * 100) for i in range(count)]
    pctlabel.x = xlabel.x
    pctlabel.y = [fill.y[i][1] + .01 for i in range(count)]
    pctlabel.valign = "bottom"
    pctlabel.halign = "center"
    x.plot(pctlabel)

    if title:
        title_label = vcs.createtext()
        title_label.string = [title]
        title_label.x = .5
        title_label.y = .96
        title_label.height = 24
        title_label.valign = "bottom"
        title_label.halign = "center"
        x.plot(title_label)

    return x
