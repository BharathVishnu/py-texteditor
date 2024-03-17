import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTextEdit, QFileDialog, QVBoxLayout, QWidget, QLabel, QDialog, QPushButton, QHBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.textEdit.setFont(QFont("Courier New"))  # Set a monospaced font for better code readability
        self.setCentralWidget(self.textEdit)

        self.createMenuBar()

        # Add status bar to display word count
        self.statusBar = self.statusBar()
        self.wordCountLabel = QLabel("Word count: 0")
        self.statusBar.addWidget(self.wordCountLabel, 1) 

        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)

        # Connect textChanged signal to updateWordCount slot
        self.textEdit.textChanged.connect(self.onTextChanged)

    def createMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        openFileAction = QAction('&Open', self)
        openFileAction.triggered.connect(self.openFile)
        fileMenu.addAction(openFileAction)

        saveFileAction = QAction('&Save', self)
        saveFileAction.triggered.connect(self.saveFile)
        fileMenu.addAction(saveFileAction)

        # Add Edit menu with Find and Replace option
        editMenu = menubar.addMenu('&Edit')

        findReplaceAction = QAction('&Find and Replace', self)
        findReplaceAction.triggered.connect(self.findAndReplace)
        editMenu.addAction(findReplaceAction)

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'Text Files (*.txt)')
        if filename:
            with open(filename, 'r') as file:
                text = file.read()
                self.textEdit.setPlainText(text)

    def saveFile(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '.', 'Text Files (*.txt)')
        if filename:
            with open(filename, 'w') as file:
                text = self.textEdit.toPlainText()
                file.write(text)

    def findAndReplace(self):
        dialog = FindReplaceDialog(self)
        dialog.exec_()

    def onTextChanged(self):
        # Count the number of words in the text and update the status bar
        text = self.textEdit.toPlainText()
        word_count = len(text.split())
        self.wordCountLabel.setText(f"Word count: {word_count}")


class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find and Replace")

        layout = QVBoxLayout()

        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        find_layout.addWidget(self.find_input)

        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace with:"))
        self.replace_input = QLineEdit()
        replace_layout.addWidget(self.replace_input)

        buttons_layout = QHBoxLayout()
        find_button = QPushButton("Find")
        find_button.clicked.connect(self.findText)
        buttons_layout.addWidget(find_button)

        replace_button = QPushButton("Replace")
        replace_button.clicked.connect(self.replaceText)
        buttons_layout.addWidget(replace_button)

        layout.addLayout(find_layout)
        layout.addLayout(replace_layout)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def findText(self):
        text = self.parent().textEdit.toPlainText()
        find_text = self.find_input.text()
        if find_text:
            index = text.find(find_text)
            if index != -1:
                self.parent().textEdit.moveCursor(1, QTextEdit.MoveAnchor)
                self.parent().textEdit.moveCursor(3, QTextEdit.KeepAnchor)
                self.parent().textEdit.setFocus()
                self.parent().textEdit.ensureCursorVisible()

    def replaceText(self):
        text = self.parent().textEdit.toPlainText()
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        if find_text and replace_text:
            text = text.replace(find_text, replace_text)
            self.parent().textEdit.setPlainText(text)
            QMessageBox.information(self, "Replacement", "Text replaced successfully.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
