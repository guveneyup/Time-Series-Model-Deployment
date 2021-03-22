from PyQt5 import QtCore, QtGui, QtWidgets
import pickle
import os
import pandas as pd
model = pickle.load(open('final_tes_model.pkl', 'rb'))

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(984, 802)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(160, 450, 221, 51))
        self.pushButton.setObjectName("pushButton")
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(420, 130, 351, 371))
        self.listView.setObjectName("listView")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(160, 350, 221, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(600, 530, 171, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(160, 310, 200, 16))
        self.label.setObjectName("label")
        self.items = []
        self.pushButton.clicked.connect(self.click)
        self.pushButton_2.clicked.connect(self.file_save)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def click(self):

        self.pred = int(self.lineEdit.text())
        self.y_pred = model.forecast(self.pred)
        self.model = QtGui.QStandardItemModel(self.listView)

        self.listView.setModel(self.model)
        for i in self.y_pred:
            self.item = QtGui.QStandardItem(str(i))
            self.model.appendRow(self.item)
            self.items.append(self.item)

    def file_save(self):
        file = QtWidgets.QFileDialog.getSaveFileName(Form, "Dosya Kaydet", os.getenv("HOME"))
        with open(file[0], "w") as fil:
            for item in self.items:
                fil.write(item.text() + "\n")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Tahmin Et"))
        self.pushButton_2.setText(_translate("Form", "Kaydet"))
        self.label.setText(_translate("Form", "Kaç Adım Tahmin Edilmek İsteniyor"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
