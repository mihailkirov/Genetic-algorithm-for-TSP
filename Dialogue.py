# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialogue.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import PVC_Algo_Genetique as pvc

# Boite de dialogue préliminaire
# --------------------------------------------------------------------
class Dialog(QtWidgets.QDialog):
    def __init__(self, parent = 0):
        super().__init__(parent)
        self.setObjectName("PVC Settings")
        self.resize(312, 451)
        self.setSizeGripEnabled(False)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(22)
        self.verticalLayout.setObjectName("verticalLayout")

        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)

        font = QtGui.QFont()
        font.setPointSize(9)

        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setCheckable(True)
        self.groupBox_2.setChecked(False)
        self.groupBox_2.setObjectName("groupBox_2")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_5.setContentsMargins(7, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setObjectName("choose_button")
        self.horizontalLayout_5.addWidget(self.pushButton)

        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setEnabled(True)
        self.groupBox.setFont(font)
        self.groupBox.setCheckable(True)
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName("groupBox")

        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(90, 30, 131, 20))
        self.lineEdit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.lineEdit.setObjectName("rand_pop")

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_4.setSpacing(14)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setObjectName("valid")
        self.pushButton_3.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.pushButton_3)

        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setObjectName("quit")
        self.horizontalLayout_4.addWidget(self.pushButton_2)

        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)

        verticalSpacer = QtWidgets.QSpacerItem(10, 10)
        self.verticalLayout.addItem(verticalSpacer)

        self.retranslateUi()
        self.groupBox_2.clicked['bool'].connect(self.groupBox.setDisabled)
        self.groupBox.clicked['bool'].connect(self.groupBox_2.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.pyqtSlot()
    def on_choose_button_clicked(self):
        src = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", "./", "Text Files (*.txt)")
        self.fileName = src[0]
        self.label.setText(self.fileName.split("/")[-1])
        if self.fileName:
            self.pushButton_3.setEnabled(True)

        else:
            self.label.setText("No file chosen")
            self.pushButton_3.setEnabled(False)

    @QtCore.pyqtSlot(str)
    def on_rand_pop_textEdited(self):
        self.pushButton_3.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_valid_clicked(self):
        if self.groupBox_2.isChecked():
            self.L = pvc.init_villes_fich(self.fileName)

        else:
            self.L = pvc.init_villes_aleat(int(self.lineEdit.text()))
        
        pvc.init_tournee(self.L)
        self.close()

    @QtCore.pyqtSlot()
    def on_quit_clicked(self):
        QtWidgets.QApplication.quit()


    # Traduction des noms et textes
    def retranslateUi(self):
        """ Méthode de traduction des noms et textes. """

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "PVC settings"))
        ligne = open("Presentation.txt", "r").read()
        self.textEdit.setHtml(_translate("Dialog", ligne))
        self.pushButton.setText(_translate("Dialog", "Choose file "))
        self.label.setText(_translate("Dialog", "No file chosen"))
        self.groupBox_2.setTitle(_translate("Dialog", "Cities generation from file"))
        self.groupBox.setTitle(_translate("Dialog", "Cities random generation"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Cities numbers"))
        self.pushButton_3.setText(_translate("Dialog", "OK"))
        self.pushButton_2.setText(_translate("Dialog", "Quit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialogue = Dialog()
    dialogue.show()
    sys.exit(app.exec_())

