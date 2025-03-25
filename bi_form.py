# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bi_form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QSizePolicy,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1100, 600)
        Dialog.setMinimumSize(QSize(1100, 550))
        self.horizontalLayout_2 = QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.bi_web_engine_view_1 = QWebEngineView(Dialog)
        self.bi_web_engine_view_1.setObjectName(u"bi_web_engine_view_1")
        self.bi_web_engine_view_1.setUrl(QUrl(u"about:blank"))

        self.horizontalLayout_2.addWidget(self.bi_web_engine_view_1)

        self.bi_web_engine_view_2 = QWebEngineView(Dialog)
        self.bi_web_engine_view_2.setObjectName(u"bi_web_engine_view_2")
        self.bi_web_engine_view_2.setUrl(QUrl(u"about:blank"))

        self.horizontalLayout_2.addWidget(self.bi_web_engine_view_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"BI", None))
    # retranslateUi

