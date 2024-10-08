from datetime import datetime

import numpy as np

from .plots import Plot


def keep_last(num, curve):
    x, y = curve.get_data()

    if num >= len(y):
        return x, y

    new_y = []
    new_x = []

    for i in range(-num, 0):
        new_y.append(y[i])
        new_x.append(x[i])

    return new_x, new_y


class Axis:

    def __init__(self, label, title):
        self.label = label
        self.unit = title


class Axes:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Curve:

    def __init__(self, c):
        self._c = c

    def keep_last(self, num):
        x, y = keep_last(num, self._c)
        self._c.set_data(x, y)

    def clear(self):
        self._c.set_data([], [])

    def append(self, x_val, y_val):
        x, y = self._c.get_data()
        x = np.append(x, x_val)
        y = np.append(y, y_val)
        self._c.set_data(x, y)


class CurveTime(Curve):

    def __init__(self, c):
        super(CurveTime, self).__init__(c)

        self._start = datetime.now()

    def clear(self):
        super(CurveTime, self).clear()
        self._start = datetime.now()

    def append(self, y_val):
        offset = (datetime.now() - self._start).total_seconds()
        super(CurveTime, self).append(offset, y_val)


def generate_styles(num_curves):
    from guiqwt.styles import style_generator

    styles = style_generator()
    return [next(styles) for _ in range(num_curves)]


def make_curves(styles, names):
    from guiqwt.builder import make

    curves = []
    for s, n in zip(styles, names):
        c = make.curve([], [], color=s[0], linestyle=s[1:], title=n)
        curves.append(c)

    return curves


def create_styled_curves(names):
    styles = generate_styles(len(names))
    return make_curves(styles, names)


def add_curves_to_plot(plot, curves):
    for c in curves:
        plot.add(c)


def build_plot(widget, title, x, y, curve_names, itemlist=False, toolbar=False, curve=Curve):
        curves = create_styled_curves(curve_names)
        plot = Plot(widget, title, y.label, x.label, y.unit, x.unit, itemlist, toolbar)

        add_curves_to_plot(plot, curves)

        wrapped_curves = [curve(c) for c in curves]

        return plot, wrapped_curves
