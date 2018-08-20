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

    'Gronsfeld': (encrypt.gronsfeld,
    "Uses the digits in the key to shift (as in Caesar cipher)"
    " the letters in the text. If it's shorter than the text,"
    " the key is repeated."),

    'Vigenere': (encrypt.vigenere,
    "Uses the letters in the key to shift (as in Caesar cipher)"
    " the letters in the text (A:0, B:1, Z:25). If it's shorter"
    " than the text, the key is repeated."),

    'Morse': (encrypt.morse,
    "Transpose in standard morse code."),

    'Affine': (encrypt.affine,
    "Given a and b constants, x letter of the plain text and"
    " y letter of the encrypted one, : y = ax + b (modulo 26).\n"
    "Note that if a = 0, it's equivalent to Caesar cipher, and"
    " if b = 0, 'A' is always ciphered 'A'"),

    'Beaufort': (encrypt.beaufort,
    "A bit like the opposite of Vigenere cipher. Instead of"
    " adding the key's letters to those of the plain text ;"
    " we substract the plain text's letters to those of the key"),

    'Collon': (encrypt.collon,
    "With the help of the grid on the left (which you can generate"
    " with the key), each letter is converted to a bigram\n("
    "a group of two letters) representing the abscissa and ordinate"
    " (or the ordinate and abscissa) in the grid.\nFor instance,"
    " R will become CS (or SC). The script will randomly alternate"
    "these two options to renforce the cipher.\n\n"
    "Then, each bigram is entered under the letter in the two lines,"
    " and following a given number,\nthe first and second line are"
    " added to the ciphered text. Here the number being 7,\nit will"
    " be ICQCKKK then QZSQZSS then KKCICEE etc. until the end.\n\n"
    "Notice that the ciphered text will be twice longer than the"
    " plain one: ICQCKKKQZSQZSSKKCICEEZVQQVVQCS.")
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
        self.algoCombo.activated.connect(self.change_keys)

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

        self.keyEdit2 = QLineEdit()
        self.keyEdit2.setPlaceholderText('Second key if needed')
        self.keyEdit2.setEnabled(False) # The first cipher needs one key

        self.encryptBtn = QPushButton('&Encrypt',
        shortcut='Ctrl+E', clicked=lambda: self.process(True))

        self.decryptBtn = QPushButton('&Decrypt',
        shortcut='Ctrl+D', clicked=lambda: self.process(False))

        layout.addWidget(self.encryptEdit, 0, 0)
        layout.addWidget(self.decryptEdit, 0, 1)
        layout.addWidget(self.keyEdit, 1, 0, 1, 2)
        layout.addWidget(self.keyEdit2, 2, 0, 2, 2)
        layout.addWidget(self.encryptBtn, 4, 0)
        layout.addWidget(self.decryptBtn, 4, 1)

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
                '<b>Cryptix</b> is a small tool for quick encrypting and'
                ' decrypting of small texts, using known basic methods.'
                ' It is developed by FrenchMasterSword and available on'
                ' <a href="https://github.com/FrenchMasterSword/Cryptix">github</a>')

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

    def process(self, encrypt: bool):
        args = [self, encrypt]
        if encrypt:
            args.append(self.encryptEdit.toPlainText())
        else:
            args.append(self.decryptEdit.toPlainText())

        algo = self.algoCombo.currentText()
        if self.keyEdit.isEnabled():
            args.append(self.keyEdit.text())
        if self.keyEdit2.isEnabled():
            args.append(self.keyEdit2.text())

        result = algoDict[algo][0](*args)

        if type(result) == str:
            # Avoid erasing input if incorrect
            if encrypt:
                self.decryptEdit.setPlainText(result)
            else:
                self.encryptEdit.setPlainText(result)

    def change_keys(self):
        if 'key' in algoDict[self.algoCombo.currentText()][0].__annotations__:
        #and not self.keyEdit.isEnabled()
            self.keyEdit.setEnabled(True)
        else:
            self.keyEdit.setEnabled(False)
        if 'key2' in algoDict[self.algoCombo.currentText()][0].__annotations__:
            self.keyEdit2.setEnabled(True)
        else:
            self.keyEdit2.setEnabled(False)

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
    # wid = QComboBox()
    # for method in dir(wid):
    #     if '__' not in method: print(method)
    # print(title)
    # print("Cryptix Version 0.3.0")
    # print("----------------------------------------\n")
    sys.exit(app.exec_())
