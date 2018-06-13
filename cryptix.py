# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#####################################################################

# FrenchMasterSword, Cryptix, 2018
#####################################################################

from PySide2 import QtWidgets, QtGui, QtCore
import encrypt

algoDict = {
    'Simple':   (encrypt.simple,),
    'Caesar':   (encrypt.caesar,),
    'Polybe':   (encrypt.polybe,),
    'ADFGVX':   (encrypt.adfgvx,),
    'Vigenere': (encrypt.vigenere,),
    'Morse':    (encrypt.morse,)
}

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)

        self.create_actions()
        self.create_menus()
        self.create_status_bar()
        self.create_algo_box()
        self.create_crypto_box()

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setSpacing(10)

        mainLayout.addWidget(self.algoBox)
        mainLayout.addWidget(self.cryptoBox)

        self.resize(900, 800)
        self.setWindowTitle('Cryptix')
        self.setWindowIcon(QtGui.QIcon('lock.png'))

        widget.setLayout(mainLayout)

    def create_actions(self):
        self.openAct = QtWidgets.QAction('&Open file', self,
            shortcut=QtGui.QKeySequence.Open,
            statusTip="Open an existing file",
            triggered=self.open)

        self.guideAct = QtWidgets.QAction('&Guide', self,
            shortcut='Ctrl+H',
            statusTip="Displays a quick How-To",
            triggered=self.guide)

        self.aboutAct = QtWidgets.QAction('&About', self,
            statusTip="Displays info about this software",
            triggered=self.about)

        self.aboutQtAct = QtWidgets.QAction('About &Qt', self,
            statusTip="Show the Qt library's About box",
            triggered=QtWidgets.qApp.aboutQt)

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
        self.algoBox = QtWidgets.QGroupBox('Cipher')
        layout = QtWidgets.QHBoxLayout()

        self.algoCombo = QtWidgets.QComboBox()
        self.algoCombo.addItems([*algoDict])

        self.algoHelp = QtWidgets.QPushButton('&Reminder',
        shortcut='Ctrl+R', clicked=self.reminder)

        layout.addWidget(self.algoCombo)
        layout.addWidget(self.algoHelp)

        self.algoBox.setLayout(layout)

    def create_crypto_box(self):
        self.cryptoBox = QtWidgets.QGroupBox()
        layout = QtWidgets.QGridLayout()

        self.encryptEdit = QtWidgets.QTextEdit()
        self.encryptEdit.setPlaceholderText('Encrypt text')

        self.decryptEdit = QtWidgets.QTextEdit()
        self.decryptEdit.setPlaceholderText('Decrypt text')

        self.keyEdit = QtWidgets.QLineEdit()
        self.keyEdit.setPlaceholderText('Key if needed')

        self.encryptBtn = QtWidgets.QPushButton('&Encrypt',
        shortcut='Ctrl+E', clicked=self.encrypt)

        self.decryptBtn = QtWidgets.QPushButton('&Decrypt',
        shortcut='Ctrl+D', clicked=self.decrypt)

        layout.addWidget(self.encryptEdit, 0, 0)
        layout.addWidget(self.decryptEdit, 0, 1)
        layout.addWidget(self.keyEdit, 1, 0, 1, 2)
        layout.addWidget(self.encryptBtn, 2, 0)
        layout.addWidget(self.decryptBtn, 2, 1)

        self.cryptoBox.setLayout(layout)

    def open(self):
        fileName, filtr = QtWidgets.QFileDialog.getOpenFileName(self)
        if fileName:
            self.load_file(fileName)

    def guide(self):
        QtWidgets.QMessageBox.information(self, "How to use Cryptix",
                "To encrypt or decrypt text : paste it respectively"
                " in the first and second text block, and press"
                " the according button.\n\n"

                "To change the current cipher, use the popup list"
                " on the left.\n\n"

                "Depending of ciphers, you might change specific"
                " settings (You dispose of one 'custom slot') if"
                " possible.\n\n"

                "A quick reminder for the current cipher is"
                " accessible with the button next to the list.")

    def about(self):
        QtWidgets.QMessageBox.about(self, "About Cryptix",
                "<b>Cryptix</b> is a small tool for quick encrypting and"
                " decrypting of small texts, using known basic methods.")

    def reminder(self):
        pass

    def encrypt(self):
        algo = self.algoCombo.currentText()
        text = self.encryptEdit.toPlainText()
        key = self.keyEdit.text()

        result = algoDict[algo][0](self, True, text, key=key)

        if type(result) == str:
            self.decryptEdit.setPlainText(result)

    def decrypt(self):
        algo = self.algoCombo.currentText()
        text = self.decryptEdit.toPlainText()
        key = self.keyEdit.text()

        result = algoDict[algo][0](self, False, text, key=key)

        if type(result) == str:
            # Avoid erasing input if incorrect
            self.encryptEdit.setPlainText(result)

    def load_file(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(self, "Cryptix",
            f"Cannot read {fileName} :\n{file.errorString()}")
            return

        stream = QtCore.QTextStream(file)
        self.encryptEdit.setPlainText(stream.readAll())

        self.statusBar().showMessage("File loaded", 2000)

if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
