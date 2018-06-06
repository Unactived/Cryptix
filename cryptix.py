from PySide2 import QtWidgets, QtGui, QtCore
# from PySide2.QtUiTools import QUiLoader

# mainWindow = QWidget()
# mainWindow.resize(550, 400)
# file = QtCore.QFile("Cryptix1.ui")
# file.open(QtCore.QFile.ReadOnly)

# loader = QUiLoader()
# mainWindow = loader.load(file)
# mainWindow.resize(1064, 900)
# mainWindow.setWindowTitle('Cryptix - a0.0.1')
# mainWindow.setWindowIcon(QtGui.QIcon('lock.png'))
# mainWindow.show()

# encryptTextWid = QPlainTextEdit()
# algoWid = QComboBox()
# algoWid.show()

# def hello():
#     print("Hello !")


# hbtn = QPushButton("Say hello")
# hbtn.clicked.connect(hello)
# hbtn.show()

# qbtn = QPushButton("Quit")
# qbtn.clicked.connect(app.exit)
# qbtn.show()


# label = QLabel("<font color=red size=40>Hey there</font>")
# label.show()

# msg_box = QMessageBox()
# msg_box.setText("<font color=black size=40>Hello World !</font>")
# msg_box.exec_()

# combo = QComboBox()
# combo.addItem("Classic (custom)")
# combo.addItem("Cesar")
# combo.addItem("Polybe")
# combo.addItem("ADFVGX")
# combo.addItem("Vigenere")
# combo.setGeometry(300, 300, 300, 300)
# QtCore.QObject.connect(combo, QtCore.SIGNAL("clicked()"), app)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.create_actions()
        self.create_menus()
        self.create_status_bar()

        self.resize(900, 800)
        self.setWindowTitle('Cryptix - a0.0.1')
        self.setWindowIcon(QtGui.QIcon('lock.png'))
        self.show()

    def create_actions(self):
        self.openAct = QtWidgets.QAction('&Open file', self,
            shortcut=QtGui.QKeySequence.Open,
            statusTip="Open an existing file",
            triggered=self.open)

        self.guideAct = QtWidgets.QAction('&Guide', self,
            shortcut='Ctrl + H',
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

    def open(self):
        fileName, filtr = QtWidgets.QFileDialog.getOpenFileName(self)
        if fileName:
            self.loadFile(fileName)

    def guide(self):
        QtWidgets.QMessageBox.information(self, "How to use Cryptix",
                "To encrypt or decrypt text : paste it respectively"
                " in the first and second text block, and press"
                " the according button.\n\n"

                "To change the current algorithm, use the popup list"
                " on the left.\n\n"

                "Depending of algorithms, you might change specific"
                " settings (You dispose of one 'custom slot') if"
                " possible.\n\n"

                "A quick memo for the current algorithm is"
                " accessible with the button next to the list.")

    def about(self):
        QtWidgets.QMessageBox.about(self, "About Cryptix",
                "<b>Cryptix</b> is a small tool for quick encrypting and"
                " decrypting of small texts, using known basic methods.")


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
