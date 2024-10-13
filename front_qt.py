import sys
import pandas as pd
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QLineEdit, QPushButton, QTextEdit, QHBoxLayout, 
                             QLabel, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt

class CSVTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        # Загрузка данных из CSV
        self.file_path = 'data.csv'  # Укажите путь к вашему CSV файлу
        self.data = pd.read_csv(self.file_path)
        self.table = QTableWidget()
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(len(self.data.columns))
        self.table.setHorizontalHeaderLabels(self.data.columns)

        # Заполнение таблицы
        self.populate_table()

        # Фильтры
        self.filters = []
        for col in self.data.columns:
            filter_layout = QHBoxLayout()
            label = QLabel(col)
            combo = QComboBox()
            combo.addItem("Все")
            unique_values = self.data[col].unique()
            for value in unique_values:
                combo.addItem(str(value))
            combo.setFixedWidth(100)  # Установите фиксированную ширину для QComboBox
            combo.currentIndexChanged.connect(self.apply_filters)
            filter_layout.addWidget(label)
            filter_layout.addWidget(combo)
            self.filters.append(combo)
            self.layout.addLayout(filter_layout)

        # Кнопка для сохранения изменений
        self.save_button = QPushButton("Сохранить изменения")
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_button)

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def populate_table(self):
        for i in range(len(self.data)):
            for j in range(len(self.data.columns)):
                item = QTableWidgetItem(str(self.data.iat[i, j]))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)  # Сделать ячейки редактируемыми
                self.table.setItem(i, j, item)

    def apply_filters(self):
        filtered_data = self.data
        for i, combo in enumerate(self.filters):
            if combo.currentText() != "Все":
                filtered_data = filtered_data[filtered_data.iloc[:, i] == combo.currentText()]
        self.update_table(filtered_data)

    def update_table(self, filtered_data):
        self.table.setRowCount(len(filtered_data))
        for i in range(len(filtered_data)):
            for j in range(len(filtered_data.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(filtered_data.iat[i, j])))

    def save_changes(self):
        # Сохранение изменений в CSV файл
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                self.data.iat[i, j] = self.table.item(i, j).text()
        self.data.to_csv(self.file_path, index=False)
        QMessageBox.information(self, "Сохранение", "Изменения сохранены в файл.")

class LinkCheckerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        self.input_field = QTextEdit()
        self.check_button = QPushButton("Проверить ссылки")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        self.check_button.clicked.connect(self.check_links)

        self.layout.addWidget(QLabel("Введите ссылки (через запятую):"))
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.check_button)
        self.layout.addWidget(QLabel("Логи:"))
        self.layout.addWidget(self.log_output)

        self.setLayout(self.layout)

    def check_links(self):
        links = self.input_field.toPlainText().split(',')
        pattern = r'https?://[^\s]+'  # Регулярное выражение для проверки ссылок
        not_found = []

        for link in links:
            link = link.strip()
            if re.match(pattern, link):
                self.log_output.append(f"Ссылка корректна: {link}")
            else:
                not_found.append(link)

        if not_found:
            self.log_output.append("Некорректные ссылки:")
            for link in not_found:
                self.log_output.append(link)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV и Проверка Ссылок")
        self.setGeometry(100, 100, 600, 400)  # Установите ширину и высоту окна

        self.tabs = QTabWidget()
        self.csv_tab = CSVTab()
        self.link_checker_tab = LinkCheckerTab()

        self.tabs.addTab(self.csv_tab, "CSV Данные")
        self.tabs.addTab(self.link_checker_tab, "Проверка Ссылок")

        self.setCentralWidget(self.tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

