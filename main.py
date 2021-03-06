from mtranslate import translate
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QTableWidgetItem, QFontDialog
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from template import Ui_MainWindow
from srtparse import get_subtitles

class SubLearn(QMainWindow):
    def __init__(self):
        super(SubLearn, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.app_variable()
        self.bind_signal()

    def app_variable(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.font = QFont("Arial", 15)
    
    def bind_signal(self):
        self.ui.open_button.clicked.connect(self.open_file)
        self.ui.font_button.clicked.connect(self.set_font)
        self.ui.next_button.clicked.connect(self.next_item)
        self.ui.previous_button.clicked.connect(self.previous_item)
        self.ui.tableSub.itemSelectionChanged.connect(self.select_subtitle)
        self.ui.listWord.itemSelectionChanged.connect(self.update_lineEdit)
        self.ui.listSentences.itemSelectionChanged.connect(self.update_lineEdit_Sentences)
        self.ui.hold_word_lineEdit.textChanged.connect(self.timer_update)
        self.timer.timeout.connect(self.translate_and_write)
    
    def open_file(self):
        filedialog = QFileDialog()
        filedialog.setFileMode(QFileDialog.AnyFile)
        url = filedialog.getOpenFileName(filter=("*.srt"))[0]
        self.add_item_tableSub(url) if url != "" else ""
        del filedialog
    
    def set_font(self):
        fontdialog = QFontDialog()
        fontdialog.exec()
        font = fontdialog.selectedFont()
        self.font = font
        self.update_font()
        return font
    
    def update_font(self):
        all_table_items = self.ui.tableSub.findItems("", Qt.MatchContains)
        for i in all_table_items: i.setFont(self.font)

    def next_item(self):
        try:
            selected_row = self.ui.tableSub.currentRow()
            self.ui.tableSub.setCurrentCell(selected_row + 1, 0)
        except AttributeError:
            pass

    def previous_item(self):
        try:
            selected_row = self.ui.tableSub.currentRow()
            self.ui.tableSub.setCurrentCell(selected_row - 1, 0)
        except AttributeError:
            pass
    
    def add_item_tableSub(self, file):
        self.ui.tableSub.setRowCount(0)
        sublist = get_subtitles(file)
        for i in sublist:
            rowPosition = self.ui.tableSub.rowCount()
            self.ui.tableSub.insertRow(rowPosition)
            item = QTableWidgetItem(i.content)
            item.setFont(self.font)
            self.ui.tableSub.setItem(rowPosition, 0, item)
        self.ui.tableSub.resizeRowsToContents()
    
    def select_subtitle(self):
        try:
            text = self.ui.tableSub.currentItem().text()
            self.update_listWord(text)
        except AttributeError:
            pass
    
    def select_sentences(self, item):
        text = item.text()
        self.ui.hold_word_lineEdit.setText(text)
    
    def update_listWord(self, text):
        self.ui.listWord.clear()
        self.ui.listSentences.clear()
        word_list = []
        sentences = text.split("\n")
        for i in sentences:
            for word in i.split(" "):
                word_list.append(word)
        for i in word_list:
            word_item = QListWidgetItem()
            word_item.setFont(self.font)
            word_item.setText(i)
            self.ui.listWord.addItem(word_item)
        for i in sentences:
            sentences_item = QListWidgetItem()
            sentences_item.setFont(self.font)
            sentences_item.setText(i)
            self.ui.listSentences.addItem(sentences_item)
    
    def update_lineEdit(self):
        text = ""
        for i in self.ui.listWord.selectedItems():
            text += (" " + i.text())
        
        self.ui.hold_word_lineEdit.setFont(self.font)
        self.ui.hold_word_lineEdit.setText(text.strip())
    
    def update_lineEdit_Sentences(self):
        text = ""
        for i in self.ui.listSentences.selectedItems():
            text += (" " + i.text())
        
        self.ui.hold_word_lineEdit.setFont(self.font)
        self.ui.hold_word_lineEdit.setText(text.strip())

    def timer_update(self, text):
        self.timer.stop()
        self.ui.translateArea.setPlainText("Please wait...")
        self.timer.start()

    def translate_and_write(self):
        self.timer.stop()
        text = self.ui.hold_word_lineEdit.text()
        trans_text = translate(text, "tr", "auto")
        self.ui.translateArea.setFont(self.font)
        self.ui.translateArea.setPlainText(trans_text)

if __name__ == "__main__":
    app = QApplication([])
    window = SubLearn()
    window.show()
    app.exec()