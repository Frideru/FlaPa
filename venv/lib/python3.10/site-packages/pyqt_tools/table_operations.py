from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


def set_item(table, row, row_items):
    for idx, item in enumerate(row_items):
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        table.setItem(row, idx, item)


def create_item(table, item_number, *args):
    row_items = [QTableWidgetItem(str(e)) for e in args]
    set_item(table, item_number, row_items)
