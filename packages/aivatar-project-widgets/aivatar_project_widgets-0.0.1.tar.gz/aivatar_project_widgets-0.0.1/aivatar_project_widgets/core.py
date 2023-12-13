# -*- coding:utf-8 -*-
"""widgets for aivatar_project_widgets"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import locale
import os
import sys

# Import third-party modules
from Qt import QtCore, QtWidgets
from Qt.QtGui import QIcon

from aivatar_project_api import AivProjectAPI


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding("utf8")

MODULE_PATH = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

LOCALE, __ = locale.getdefaultlocale()
IS_ZH = "zh" in LOCALE.lower()
WINDOW_NAME = u"项目选择" if IS_ZH else "Project Selection"
TITLE_TIPS = u"请选择一个项目：" if IS_ZH else "Please choose a project:"
LINK_TIPS = u"想创建一个项目？" if IS_ZH else "Create a new project?"
LINK_TEXT = u"申请接入" if IS_ZH else "Apply"
COMBO_HINT = u"  请先申请项目" if IS_ZH else "  Please apply a project firstly."
BTN_NAME = u"确 认" if IS_ZH else "Confirm"


class AivProjectWindow(QtWidgets.QMainWindow):
    def __init__(
            self,
            token,
            terminal_type,
            business_type,
            parent_window=None,
            on_confirm = None,
            is_test=False
    ):
        super(AivProjectWindow, self).__init__(parent=parent_window)

        self.project_api = AivProjectAPI(token, terminal_type, business_type, is_test)
        self.__project_items = []
        self.__new_project_id = -1
        self.__current_project_id = -1
        self.__current_project_experiment = 0
        self.__current_project_name = ""
        self.on_confirm = on_confirm

        self.__init_widgets(business_type)
    
    def __init_widgets(self, business_type):
        # Window
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("project_widget")
        self.setCentralWidget(self.central_widget)

        # self.setGeometry(300, 300, 380, 220)
        self.setFixedSize(400, 260)
        self.setWindowTitle("{} - {}".format(business_type, WINDOW_NAME))
        style_sheet = "QMainWindow {background-color: #222;}" \
        "QLabel {font-size: 12px; font-family: \'Microsoft YaHei\'}" \
        "QComboBox {font-size: 18px; font-family: \'Microsoft YaHei\'; background-color: #2f2f2f; border-radius: 3px;}" \
        "QComboBox::drop-down {width: 10px; border: none; padding: 18;}" \
        "QComboBox::item {icon-size: 18px 18px;}" \
        "QPushButton { border-radius: 20; height: 40; background-color: #999; font-size: 16px; font-family: \'Microsoft YaHei\'; font-color: #eee}" \
        "QPushButton::hover { background-color: #1E90FF}"
        style_sheet += "QComboBox::down-arrow {image: url("+ MODULE_PATH + "/icons/arrow-down-16.png" +");}"
        self.setStyleSheet(style_sheet)

        # Title labels
        widget_title = QtWidgets.QWidget(self)
        label_tips = QtWidgets.QLabel(widget_title)
        label_tips.setText(TITLE_TIPS)
        
        spacer_h = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
        label_link_tips = QtWidgets.QLabel(widget_title)
        label_link_tips.setText(LINK_TIPS)
        # link
        label_link = QtWidgets.QLabel(widget_title)
        label_link.setOpenExternalLinks(True)
        label_link.setText("<a style='color: #00BFFF; text-decoration: none' " \
        "href={}>{}</a>".format(self.project_api.config.get_manager_page_url(), LINK_TEXT))
        
        layout_title = QtWidgets.QHBoxLayout(widget_title)
        layout_title.addWidget(label_tips)
        layout_title.addItem(spacer_h)
        layout_title.addWidget(label_link_tips)
        layout_title.addWidget(label_link)
        # layout_title.setAlignment(label_tips, QtCore.Qt.AlignLeft)
        # layout_title.setAlignment(label_link_tips, QtCore.Qt.AlignLeft)
        # layout_title.setAlignment(label_link, QtCore.Qt.AlignLeft)       
        widget_title.setLayout(layout_title)
        
        # Dropdown
        widget_main = QtWidgets.QWidget(self.central_widget)
        self.combo_projects = QtWidgets.QComboBox(widget_main)
        self.combo_projects.setFixedHeight(50)
        self.combo_projects.setMinimumWidth(300)
        self.combo_projects.setMaximumSize(500, 50)
        self.combo_projects.currentIndexChanged.connect(self._on_selection_changed)
        combo_hint = QtWidgets.QLineEdit()
        combo_hint.setPlaceholderText(COMBO_HINT)
        combo_hint.setReadOnly(True)
        self.combo_projects.setLineEdit(combo_hint)
        
        spacer_v = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # Button
        self.btn_confirm = QtWidgets.QPushButton(BTN_NAME, self.central_widget)
        self.btn_confirm.clicked.connect(self._on_confirm_clicked)
        self.btn_confirm.setMaximumWidth(180)
        self.btn_confirm.setMinimumWidth(180)
        
        layout_main = QtWidgets.QVBoxLayout(widget_main)
        layout_main.addWidget(widget_title)
        layout_main.addWidget(self.combo_projects)
        layout_main.addItem(spacer_v)
        layout_main.addWidget(self.btn_confirm)
        # layout_main.setAlignment(widget_title, QtCore.Qt.AlignCenter)
        layout_main.setAlignment(self.btn_confirm, QtCore.Qt.AlignCenter)
        layout_main.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        
        # window layout
        layout_central = QtWidgets.QVBoxLayout(self.central_widget)
        layout_central.addWidget(widget_main)
        layout_central.setAlignment(widget_main, QtCore.Qt.AlignCenter)
        self.central_widget.setLayout(layout_central)

    @property
    def current_project_id(self):
        return self.__current_project_id

    @property
    def current_project_name(self):
        return self.__current_project_name

    @property
    def current_project_experiment(self):
        return self.__current_project_experiment

    @property
    def project_items(self):
        return self.__project_items

    def popup(self):
        self.__project_items = self.project_api.get_project_items()
        current_project_id = self.project_api.current_project_id
        ids = [pi.project_id for pi in self.__project_items]
        
        self.combo_projects.clear()
        self.combo_projects.addItems([" {name} ({id})".format(name=pi.project_name, id=pi.project_id) for pi in self.__project_items])
        if current_project_id in ids:
            self.combo_projects.setCurrentIndex(ids.index(current_project_id))
        icon = QIcon(os.path.join(MODULE_PATH, "icons/project-0-50.png"))
        for i in range(self.combo_projects.count()):
            self.combo_projects.setItemIcon(i, icon) 
        self.__new_project_id = -1
        self.show()
    
    def should_popup(self):
        valid = self.project_api.is_project_record_valid()
        if valid:
            self.__sync_project_record()
        return not valid
    
    def _on_selection_changed(self, index):
        if index < 0: return
        self.__new_project_id = self.__project_items[index].project_id
        # self.__current_project_experiment = self.__project_items[index].experiment
        # self.project_api.current_project_id = self.__current_project_id
    
    def _on_confirm_clicked(self):
        if self.__new_project_id >= 0:
            self.project_api.current_project_id = self.__new_project_id
        self.close()
    
    def __sync_project_record(self):
        self.__current_project_id = self.project_api.current_project_id
        self.__current_project_name = self.project_api.current_project_name
        self.__current_project_experiment = self.project_api.current_project_experiment

    def closeEvent(self, event):
        if self.isVisible():
            self.__sync_project_record()
            if self.on_confirm:
                self.on_confirm(self.__current_project_id, self.__current_project_name, self.__current_project_experiment)
        event.accept()
