import sys
import pandas as pd
import re
import multiprocessing
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QLineEdit, QPushButton, QTextEdit, QHBoxLayout, 
                             QLabel, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
from parcers.russianrealty_prcr import Russianrealty as rlprcr
from parcers.mirkvartir_prcr import MirKvartir as mkprcr
from parcers.metrtv_prcr import MetrTv as mtprcr
from parcers.move_prcr import MoveRu as mvprcr
from parcers.upn_prcr import Upn as upnprcr

def rr_worker(link, queue):
    result = rlprcr(link) 
    queue.put(result)  # Помещаем результат в очередь

def mk_worker(link, queue):
    result = mkprcr(link)
    queue.put(result)  # Помещаем результат в очередь

def mt_worker(link, queue):
    result = mtprcr(link)
    queue.put(result)  # Помещаем результат в очередь

def mv_worker(link, queue):
    result = mvprcr(link)
    queue.put(result)  # Помещаем результат в очередь

def upn_worker(link, queue):
    result = upnprcr(link)
    queue.put(result)  # Помещаем результат в очередь

# 
# 1. Вкладка просмотра таблицы
# 

class CSVTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        # Загрузка данных из CSV. Сама CSV таблица
        self.file_path = 'data.csv' # Путь к CSV файлу
        self.data = pd.read_csv(self.file_path)
        self.table = QTableWidget()
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(len(self.data.columns))
        self.table.setHorizontalHeaderLabels(self.data.columns)
        self.table.setFixedHeight(500)

        # Заполнение таблицы
        self.populate_table()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        # Кнопка для сохранения изменений
        self.save_button = QPushButton("Сохранить изменения")
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_button)
        
        # Фильтры
        self.filters = []
        filter_layout = QHBoxLayout()
        for col in self.data.columns:
            filter_widget = QVBoxLayout()
            label = QLabel(col)
            combo = QComboBox()
            combo.addItem("Все")
            unique_values = self.data[col].unique()
            for value in unique_values:
                combo.addItem(str(value))
            combo.setFixedWidth(100)  # Установите фиксированную ширину для QComboBox
            combo.currentIndexChanged.connect(self.apply_filters)
            filter_widget.addWidget(label)
            filter_widget.addWidget(combo)
            self.filters.append(combo)
            filter_layout.addLayout(filter_widget)
        
        self.layout.addLayout(filter_layout)

    # Заполнение таблицы
    def populate_table(self):
        for i in range(len(self.data)):
            for j in range(len(self.data.columns)):
                item = QTableWidgetItem(str(self.data.iat[i, j]))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)  # Сделать ячейки редактируемыми
                self.table.setItem(i, j, item)

    # Применить фильтры
    def apply_filters(self):
        filtered_data = self.data
        for i, combo in enumerate(self.filters):
            if combo.currentText() != "Все":
                filtered_data = filtered_data[filtered_data.iloc[:, i] == combo.currentText()]
        filtered_data = filtered_data.drop_duplicates()
        self.update_table(filtered_data)

    # Обновить таблицу
    def update_table(self, filtered_data):
        self.table.setRowCount(len(filtered_data))
        for i in range(len(filtered_data)):
            for j in range(len(filtered_data.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(filtered_data.iat[i, j])))

    # Сохранить изменения
    def save_changes(self):
        # Сохранение изменений в CSV файл
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                self.data.iat[i, j] = self.table.item(i, j).text()
        self.data.to_csv(self.file_path, index=False)
        QMessageBox.information(self, "Сохранение", "Изменения сохранены в файл.")

# 
# 2. Вкладка парсинга
# 

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
        self.log_output.clear()
        links     = self.input_field.toPlainText().split(',')
        pattern   = r'^https?://([a-zA-Z]*)?\.?(domclick|mirkvartir|russianrealty|metrtv|move|upn)\.[a-z]{,3}\/[a-zA-Z]*'
        not_found = []

        for link in links:
            link = link.strip()
            if re.findall(pattern, link):
                if re.findall(r'russianrealty', link):
                    queue      = multiprocessing.Queue()
                    rr_process = multiprocessing.Process(target=rr_worker, args=(link, queue))
                    rr_process.start()
                    rr_process.join()

                    rr_result = queue.get()
                    if(rr_result == "OK!"):
                        self.log_output.append(f"- Информация с сайта Russianrealty записана!\nЗаписанная ссыслка: {link}")
                elif re.findall(r'mirkvartir', link):
                    queue      = multiprocessing.Queue()
                    mk_process = multiprocessing.Process(target=mk_worker, args=(link, queue))
                    mk_process.start()
                    mk_process.join()

                    mk_result = queue.get()
                    if(mk_result == "OK!"):
                        self.log_output.append(f"- Информация с сайта Mirkvartir записана!\nЗаписанная ссыслка: {link}")
                
                elif re.findall(r'metrtv', link):
                    queue      = multiprocessing.Queue()
                    mt_process = multiprocessing.Process(target=mt_worker, args=(link, queue))
                    mt_process.start()
                    mt_process.join()

                    mt_result = queue.get()
                    if(mt_result == "OK!"):
                        self.log_output.append(f"- Информация с сайта Metrtv записана!\nЗаписанная ссыслка: {link}")
                
                elif re.findall(r'move', link):
                    queue      = multiprocessing.Queue()
                    mt_process = multiprocessing.Process(target=mv_worker, args=(link, queue))
                    mt_process.start()
                    mt_process.join()

                    mt_result = queue.get()
                    if(mt_result == "OK!"):
                        self.log_output.append(f"- Информация с сайта Move записана!\nЗаписанная ссыслка: {link}")
                
                elif re.findall(r'upn', link):
                    queue      = multiprocessing.Queue()
                    upn_process = multiprocessing.Process(target=upn_worker, args=(link, queue))
                    upn_process.start()
                    upn_process.join()

                    upn_result = queue.get()
                    if(upn_result == "OK!"):
                        self.log_output.append(f"- Информация с сайта Upn записана!\nЗаписанная ссыслка: {link}")
            else:
                not_found.append(link)

        if not_found:
            self.log_output.append("--- ---\nНекорректные ссылки:")
            for link in not_found:
                self.log_output.append(f'* {link}')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица и Парсинг сайтов")
        self.setGeometry(100, 100, 600, 400)  # Установите ширину и высоту окна

        self.tabs = QTabWidget()
        self.csv_tab = CSVTab()
        self.link_checker_tab = LinkCheckerTab()

        self.tabs.addTab(self.csv_tab, "CSV Данные")
        self.tabs.addTab(self.link_checker_tab, "Парсинг сайтов")

        self.setCentralWidget(self.tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
