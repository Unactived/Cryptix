# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#####################################################################

# FrenchMasterSword, Cryptix, 2018
#####################################################################

from PySide2.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QAction,
    QGroupBox, QHBoxLayout, QComboBox, QPushButton, QGridLayout, QTextEdit,
    QLineEdit, QDialog, QLabel, QApplication, QMessageBox, QFileDialog)
from PySide2.QtGui import QIcon, QPixmap, QKeySequence
from PySide2.QtCore import QFile, QTextStream, Qt
import encrypt

algoDict = {
    'Simple': (encrypt.simple,
    "Simply replace letters in the alphabet with those in the key."
    " You don't have to enter a complete one, as it will be generated from it."),

    'Caesar': (encrypt.caesar,
    "Shifts the text's letter in the alphabet of the number given as key."),

    'Polybe': (encrypt.polybe,
    "Replace letters by their abscissa and ordinate in a grid. If a key is"
    " given, it starts filling the grid, and finishes with the rest of the"
    " alphabet.\nThe second grid is an example with 'CRYPTIX' used as key."
    " As there are only 25 squares, J is removed and replaced with I."),

    'ADFGVX': (encrypt.adfgvx,
    "Same as Polybe, but grid is indexed with these 6 letters,"
    " and also encrypt digits."),

    'Wolseley': (encrypt.wolseley,
    "Replaces letters with a reversed alphabet, missing a letter."),

    'Vigenere': (encrypt.vigenere,
    "Uses the letter in the key to shift (as in Caesar cipher) the letter"
    " in the text. If it's shorter than the text, the key is repeated."),

    'Morse': (encrypt.morse,
    "Transpose in standard morse code.")
}

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        self.create_actions()
        self.create_menus()
        self.create_status_bar()
        self.create_algo_box()
        self.create_crypto_box()

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(10)

        mainLayout.addWidget(self.algoBox)
        mainLayout.addWidget(self.cryptoBox)

        self.resize(900, 800)
        self.setWindowTitle('Cryptix')
        self.setWindowIcon(QIcon('lock.png'))

        widget.setLayout(mainLayout)

    def create_actions(self):
        self.openAct = QAction('&Open file', self,
            shortcut=QKeySequence.Open,
            statusTip="Open an existing file",
            triggered=self.open)

        self.guideAct = QAction('&Guide', self,
            shortcut='Ctrl+H',
            statusTip="Displays a quick How-To",
            triggered=self.guide)

        self.aboutAct = QAction('&About', self,
            statusTip="Displays info about this software",
            triggered=self.about)

        self.aboutQtAct = QAction('About &Qt', self,
            statusTip="Show the Qt library's About box",
            triggered=self.aboutQt)

    def create_menus(self):

        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction(self.openAct)

        self.helpMenu = self.menuBar().addMenu('&Help')
        self.helpMenu.addAction(self.guideAct)
        self.helpMenu.addSeparator();
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def create_status_bar(self):
        self.statusBar().showMessage("Ready")

    def create_algo_box(self):
        self.algoBox = QGroupBox('Cipher')
        layout = QHBoxLayout()

        self.algoCombo = QComboBox()
        self.algoCombo.addItems([*algoDict])

        self.algoHelp = QPushButton('&Reminder',
        shortcut='Ctrl+R', clicked=self.reminder)

        layout.addWidget(self.algoCombo)
        layout.addWidget(self.algoHelp)

        self.algoBox.setLayout(layout)

    def create_crypto_box(self):
        self.cryptoBox = QGroupBox()
        layout = QGridLayout()

        self.encryptEdit = QTextEdit()
        self.encryptEdit.setPlaceholderText('Encrypt text')

        self.decryptEdit = QTextEdit()
        self.decryptEdit.setPlaceholderText('Decrypt text')

        self.keyEdit = QLineEdit()
        self.keyEdit.setPlaceholderText('Key if needed')

        self.encryptBtn = QPushButton('&Encrypt',
        shortcut='Ctrl+E', clicked=self.encrypt)

        self.decryptBtn = QPushButton('&Decrypt',
        shortcut='Ctrl+D', clicked=self.decrypt)

        layout.addWidget(self.encryptEdit, 0, 0)
        layout.addWidget(self.decryptEdit, 0, 1)
        layout.addWidget(self.keyEdit, 1, 0, 1, 2)
        layout.addWidget(self.encryptBtn, 2, 0)
        layout.addWidget(self.decryptBtn, 2, 1)

        self.cryptoBox.setLayout(layout)

    def open(self):
        fileName, filtr = QFileDialog.getOpenFileName(self)
        if fileName:
            self.load_file(fileName)

    def guide(self):
        QMessageBox.information(self, "How to use Cryptix",
                "To encrypt or decrypt text : paste it respectively"
                " in the first and second text block, and press"
                " the according button.\n\n"

                "To change the current cipher, use the popup list"
                " on the left.\n\n"

                "Depending of ciphers, you might change specific settings.\n\n"

                "A quick reminder for the current cipher is"
                " accessible with the button next to the list.")

    def about(self):
        QMessageBox.about(self, "About Cryptix",
                "<b>Cryptix</b> is a small tool for quick encrypting and"
                " decrypting of small texts, using known basic methods.")

    def aboutQt(self):
        QMessageBox.aboutQt(self, "About Qt")

    def reminder(self):
        box = QDialog(self)

        algo = self.algoCombo.currentText()

        pixmap = QPixmap(f'images/{algo.lower()}.png')
        labelImage = QLabel()
        labelImage.setPixmap(pixmap)
        labelImage.setAlignment(Qt.AlignHCenter)

        labelText = QLabel(algoDict[algo][1])
        labelText.setAlignment(Qt.AlignJustify)

        box.setWindowTitle(f"{algo} reminder")

        layout = QVBoxLayout()
        layout.addWidget(labelImage)
        layout.addWidget(labelText)

        box.setLayout(layout)
        box.show()

    def encrypt(self):
        algo = self.algoCombo.currentText()
        text = self.encryptEdit.toPlainText()
        key = self.keyEdit.text()

        result = algoDict[algo][0](self, True, text, key)

        if type(result) == str:
            # Avoid erasing input if incorrect
            self.decryptEdit.setPlainText(result)

    def decrypt(self):
        algo = self.algoCombo.currentText()
        text = self.decryptEdit.toPlainText()
        key = self.keyEdit.text()

        result = algoDict[algo][0](self, False, text, key)

        if type(result) == str:
            # Avoid erasing input if incorrect
            self.encryptEdit.setPlainText(result)

    def load_file(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Cryptix",
            f"Cannot read {fileName} :\n{file.errorString()}")
            return

        stream = QTextStream(file)
        self.encryptEdit.setPlainText(stream.readAll())

        self.statusBar().showMessage("File loaded", 2000)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
