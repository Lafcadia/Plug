from plugin.engine.minebbs import Minebbs
from plugin.engine.klpbbs import Klpbbs
from plugin.engine.spigotmc import Spigot
from plugin.engine.tinksp import Tinksp
from concurrent.futures import ThreadPoolExecutor, wait
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QTreeWidgetItem
from PySide6.QtCore import QObject, QThread, Signal, Slot
# from PySide6 import QtCore
import sys
from ui import Ui_MainWindow
import pyperclip

class Worker(QObject):
    _signal = Signal(list)
    def __init__(self):
        super().__init__()
        print("000")

    def work(self, keyword):
        print(111)
        engine = [Spigot, Tinksp, Minebbs, Klpbbs]
        results = []
        with ThreadPoolExecutor(max_workers=6) as executor:
            future_list = []
            for e in engine:
                future = executor.submit(e().search, keyword)
                print(10)
                future_list.append(future)
            wait(future_list)
            for future in future_list:
                for result in future.result():
                    results.append(result)
                    print(1)
        self._signal.emit(results)

class MainWindow(QMainWindow):
    a = Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.worker = Worker()
        self.worker_thread = QThread()
        self.worker._signal.connect(self.shower)
        self.worker.moveToThread(self.worker_thread)
        self.a.connect(self.worker.work)
        self.ui.searchButton.clicked.connect(self.search)
        self.ui.outputTreeWidget.itemDoubleClicked.connect(self.copyUrl)
        self.worker_thread.start()

    def search(self):
        keyword = self.ui.searchLine.text()
        self.ui.outputTreeWidget.clear()
        self.a.emit(keyword)

    def shower(self, results):
        for result in results:
            num = results.index(result)
            title = QTreeWidgetItem(self.ui.outputTreeWidget, [result.title, result.url, result.summary])
    
    def copyUrl(self, item):
        # copy a text to the clipboard.
        pyperclip.copy(item.text(1))
        QMessageBox.information(self, "Copied!", "已将该插件链接复制到剪贴板。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
