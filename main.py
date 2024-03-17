import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTextEdit, QFileDialog, QVBoxLayout, QWidget, QLabel
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
        self.statusBar = QLabel("Word count: 0")
        self.statusBar.setAlignment(Qt.AlignRight)
        self.setStatusBar(self.statusBar)

        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)

        # Connect textChanged signal to updateWordCount slot
        self.textEdit.textChanged.connect(self.updateWordCount)

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
        # Implement find and replace functionality here
        pass

    def updateWordCount(self):
        # Count the number of words in the text and update the status bar
        text = self.textEdit.toPlainText()
        word_count = len(text.split())
        self.statusBar.setText(f"Word count: {word_count}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
