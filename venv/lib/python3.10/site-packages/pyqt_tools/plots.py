from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QSizePolicy
from guiqwt.plot import CurveDialog

from .utils import set_size_policy


class Plot(QtWidgets.QWidget):

    def __init__(self, main, title, ylabel, xlabel, yunit, xunit, itemlist=False, toolbar=False):
        super(Plot, self).__init__()

        self._plot = CurveDialog(toolbar=toolbar, wintitle=title,
                                 options=dict(ylabel=ylabel, yunit=yunit,
                                              xlabel=xlabel, xunit=xunit))

        if itemlist:
            self._plot.get_itemlist_panel().show()

        set_size_policy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        set_size_policy(self._plot, QSizePolicy.Expanding, QSizePolicy.Expanding)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.setObjectName("Plot")

        main.addWidget(self._plot)

    def add(self, item):
        self._plot.get_plot().add_item(item)
