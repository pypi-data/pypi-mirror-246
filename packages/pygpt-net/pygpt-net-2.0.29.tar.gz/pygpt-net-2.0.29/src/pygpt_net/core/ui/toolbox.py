#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.08 22:00:00                  #
# ================================================== #
import os

from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItemModel, Qt, QIcon
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSplitter, QWidget, QCheckBox, QSizePolicy

from .widget.textarea import NameInput
from .widget.settings import SettingsSlider, SettingsTextarea
from .widget.select import SelectMenu, PresetSelectMenu, AssistantSelectMenu
from ..utils import trans


class Toolbox:
    def __init__(self, window=None):
        """
        Toolbox UI

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """
        Setups toolbox

        :return: QSplitter
        """
        # modes and models
        mode_widget = QWidget()
        model_widget = QWidget()
        mode_widget.setLayout(self.setup_list('prompt.mode', trans("toolbox.mode.label")))
        model_widget.setLayout(self.setup_list('prompt.model', trans("toolbox.model.label")))
        mode_widget.setMinimumHeight(150)

        self.window.splitters['toolbox.mode'] = QSplitter(Qt.Horizontal)
        self.window.splitters['toolbox.mode'].addWidget(mode_widget)
        self.window.splitters['toolbox.mode'].addWidget(model_widget)

        # presets
        presets = self.setup_presets('preset.presets', trans("toolbox.presets.label"))
        self.window.models['preset.presets'] = self.create_model(self.window)
        self.window.data['preset.presets'].setModel(self.window.models['preset.presets'])

        self.window.data['presets.widget'] = QWidget()
        self.window.data['presets.widget'].setLayout(presets)
        self.window.data['presets.widget'].setMinimumHeight(150)

        # assistants
        assistants = self.setup_assistants('assistants', trans("toolbox.assistants.label"))
        self.window.models['assistants'] = self.create_model(self.window)
        self.window.data['assistants'].setModel(self.window.models['assistants'])

        self.window.data['assistants.widget'] = QWidget()
        self.window.data['assistants.widget'].setLayout(assistants)
        self.window.data['assistants.widget'].setMinimumHeight(150)

        # initial prompt text
        prompt = self.setup_prompt()
        prompt_widget = QWidget()
        prompt_widget.setLayout(prompt)

        self.window.splitters['toolbox.presets'] = QSplitter(Qt.Horizontal)
        self.window.splitters['toolbox.presets'].addWidget(self.window.data['presets.widget'])  # prompts list
        self.window.splitters['toolbox.presets'].addWidget(self.window.data['assistants.widget'])  # assistants list

        self.window.splitters['toolbox'] = QSplitter(Qt.Vertical)
        self.window.splitters['toolbox'].addWidget(self.window.splitters['toolbox.mode'])  # mode and model list
        self.window.splitters['toolbox'].addWidget(self.window.splitters['toolbox.presets'])  # presets and assistants list
        self.window.splitters['toolbox'].addWidget(prompt_widget)  # prompt text (editable)

        # AI and users names
        names_layout = QHBoxLayout()
        names_layout.addLayout(self.setup_name_input('preset.ai_name', trans("toolbox.name.ai")))
        names_layout.addLayout(self.setup_name_input('preset.user_name', trans("toolbox.name.user")))

        # bottom
        self.window.data['temperature.label'] = QLabel(trans("toolbox.temperature.label"))
        self.window.config_option['current_temperature'] = SettingsSlider(self.window, 'current_temperature',
                                                                          '', 0, 200,
                                                                          1, 100, False)

        self.window.data['img_variants.label'] = QLabel(trans("toolbox.img_variants.label"))
        self.window.config_option['img_variants'] = SettingsSlider(self.window, 'img_variants',
                                                                   '', 1, 4,
                                                                   1, 1, False)

        self.window.config_option['img_raw'] = QCheckBox(trans("img.raw"))
        self.window.config_option['img_raw'].stateChanged.connect(
            lambda: self.window.controller.image.toggle_raw(self.window.config_option['img_raw'].isChecked()))

        dalle_label = QLabel(trans("toolbox.img_variants.label"))

        # dalle layout
        dalle_opts_layout = QHBoxLayout()
        dalle_opts_layout.addWidget(self.window.config_option['img_raw'])
        dalle_opts_layout.addWidget(self.window.config_option['img_variants'])

        dalle_layout = QVBoxLayout()
        dalle_layout.addWidget(dalle_label)
        dalle_layout.addLayout(dalle_opts_layout)

        self.window.data['dalle.options'] = QWidget()
        self.window.data['dalle.options'].setLayout(dalle_layout)
        self.window.data['dalle.options'].setContentsMargins(0, 0, 0, 0)

        self.window.data['vision.capture.enable'] = QCheckBox(trans("vision.capture.enable"))
        self.window.data['vision.capture.enable'].stateChanged.connect(
            lambda: self.window.controller.camera.toggle(self.window.data['vision.capture.enable'].isChecked()))

        self.window.data['vision.capture.auto'] = QCheckBox(trans("vision.capture.auto"))
        self.window.data['vision.capture.auto'].stateChanged.connect(
            lambda: self.window.controller.camera.toggle_auto(self.window.data['vision.capture.auto'].isChecked()))

        self.window.data['vision.capture.label'] = QLabel(trans('vision.capture.options.title'))

        # cap layout
        cap_layout = QHBoxLayout()
        cap_layout.addWidget(self.window.data['vision.capture.enable'])
        cap_layout.addWidget(self.window.data['vision.capture.auto'])

        # cap
        cap_vlayout = QVBoxLayout()
        cap_vlayout.addWidget(self.window.data['vision.capture.label'])
        cap_vlayout.addLayout(cap_layout)

        # cap widget
        self.window.data['vision.capture.options'] = QWidget()
        self.window.data['vision.capture.options'].setLayout(cap_vlayout)
        self.window.data['vision.capture.options'].setContentsMargins(0, 0, 0, 0)

        temp_layout = QVBoxLayout()
        temp_layout.addWidget(self.window.data['temperature.label'])
        temp_layout.addWidget(self.window.config_option['current_temperature'])
        temp_layout.addWidget(self.window.data['dalle.options'])
        temp_layout.addWidget(self.window.data['vision.capture.options'])

        path = os.path.abspath(os.path.join(self.window.config.get_root_path(), 'data', 'logo.png'))

        logo_button = QPushButton()
        logo_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        logo_button.setIcon(QIcon(path))
        logo_button.setIconSize(QSize(100, 28))
        logo_button.setFlat(True)
        logo_button.clicked.connect(lambda: self.window.controller.info.goto_website())

        bottom = QHBoxLayout()
        bottom.addLayout(temp_layout, 80)
        bottom.addWidget(logo_button, 20)
        bottom.setStretchFactor(logo_button, 1)
        bottom.setAlignment(logo_button, Qt.AlignRight | Qt.AlignBottom)

        temp_widget = QWidget()
        temp_widget.setLayout(bottom)

        bottom_layout = QVBoxLayout()
        bottom_layout.addLayout(names_layout)
        bottom_layout.addWidget(temp_widget)

        names_widget = QWidget()
        names_widget.setLayout(bottom_layout)

        self.window.splitters['toolbox'].addWidget(names_widget)

        return self.window.splitters['toolbox']

    def setup_prompt(self):
        """
        Setups preset prompt

        :return: QVBoxLayout
        """
        self.window.data['cmd.enabled'] = QCheckBox(trans('cmd.enabled'))
        self.window.data['cmd.enabled'].stateChanged.connect(
            lambda: self.window.controller.input.toggle_cmd(self.window.data['cmd.enabled'].isChecked()))

        self.window.data['toolbox.prompt.label'] = QLabel(trans("toolbox.prompt"))
        self.window.data['toolbox.prompt.label'].setStyleSheet(self.window.controller.theme.get_style('text_bold'))

        self.window.data['preset.clear'] = QPushButton(trans('preset.clear'))
        self.window.data['preset.clear'].clicked.connect(
            lambda: self.window.controller.presets.clear())
        self.window.data['preset.use'] = QPushButton(trans('preset.use'))
        self.window.data['preset.use'].clicked.connect(
            lambda: self.window.controller.presets.use())
        self.window.data['preset.use'].setVisible(False)

        header = QHBoxLayout()
        header.addWidget(self.window.data['toolbox.prompt.label'])
        header.addWidget(self.window.data['cmd.enabled'])
        header.addWidget(self.window.data['preset.use'], alignment=Qt.AlignRight)
        header.addWidget(self.window.data['preset.clear'], alignment=Qt.AlignRight)

        self.window.data['preset.prompt'] = SettingsTextarea(self.window, 'preset.prompt', True)
        layout = QVBoxLayout()
        layout.addLayout(header)
        layout.addWidget(self.window.data['preset.prompt'])
        return layout

    def setup_list(self, id, title):
        """
        Setups list

        :param id: ID of the list
        :param title: Title of the list
        :return: QVBoxLayout
        """
        label_key = id + '.label'
        self.window.data[label_key] = QLabel(title)
        self.window.data[label_key].setStyleSheet(self.window.controller.theme.get_style('text_bold'))
        self.window.data[id] = SelectMenu(self.window, id)
        layout = QVBoxLayout()
        layout.addWidget(self.window.data[label_key])
        layout.addWidget(self.window.data[id])

        self.window.models[id] = self.create_model(self.window)
        self.window.data[id].setModel(self.window.models[id])
        return layout

    def setup_presets(self, id, title):
        """
        Setups list

        :param id: ID of the list
        :param title: Title of the list
        :return: QVBoxLayout
        """
        self.window.data['preset.presets.new'] = QPushButton(trans('preset.new'))
        self.window.data['preset.presets.new'].clicked.connect(
            lambda: self.window.controller.presets.edit())

        self.window.data['preset.presets.label'] = QLabel(title)
        self.window.data['preset.presets.label'].setStyleSheet(self.window.controller.theme.get_style('text_bold'))
        header = QHBoxLayout()
        header.addWidget(self.window.data['preset.presets.label'])
        header.addWidget(self.window.data['preset.presets.new'], alignment=Qt.AlignRight)
        header.setContentsMargins(0, 0, 0, 0)

        header_widget = QWidget()
        header_widget.setLayout(header)

        self.window.data[id] = PresetSelectMenu(self.window, id)
        layout = QVBoxLayout()
        layout.addWidget(header_widget)
        layout.addWidget(self.window.data[id])

        self.window.models[id] = self.create_model(self.window)
        self.window.data[id].setModel(self.window.models[id])
        return layout

    def setup_assistants(self, id, title):
        """
        Setups list

        :param id: ID of the list
        :param title: Title of the list
        :return: QVBoxLayout
        """
        self.window.data['assistants.new'] = QPushButton(trans('assistant.new'))
        self.window.data['assistants.new'].clicked.connect(
            lambda: self.window.controller.assistant.edit())

        self.window.data['assistants.import'] = QPushButton(trans('assistant.import'))
        self.window.data['assistants.import'].clicked.connect(
            lambda: self.window.controller.assistant.import_assistants())

        self.window.data['assistants.label'] = QLabel(title)
        self.window.data['assistants.label'].setStyleSheet(self.window.controller.theme.get_style('text_bold'))

        header = QHBoxLayout()
        header.addWidget(self.window.data['assistants.label'])
        header.addWidget(self.window.data['assistants.import'], alignment=Qt.AlignRight)
        header.addWidget(self.window.data['assistants.new'], alignment=Qt.AlignRight)
        header.setContentsMargins(0, 0, 0, 0)

        header_widget = QWidget()
        header_widget.setLayout(header)

        self.window.data[id] = AssistantSelectMenu(self.window, id)
        layout = QVBoxLayout()
        layout.addWidget(header_widget)
        layout.addWidget(self.window.data[id])

        self.window.models[id] = self.create_model(self.window)
        self.window.data[id].setModel(self.window.models[id])
        return layout

    def setup_name_input(self, id, title):
        """
        Setups name input

        :param id: ID of the input
        :param title: Title of the input
        :return: QVBoxLayout
        """
        label_key = 'toolbox.' + id + '.label'
        self.window.data[label_key] = QLabel(title)
        self.window.data[id] = NameInput(self.window, id)
        layout = QVBoxLayout()
        layout.addWidget(self.window.data[label_key])
        layout.addWidget(self.window.data[id])
        return layout

    def create_model(self, parent):
        """
        Creates list model
        :param parent: parent widget
        :return: QStandardItemModel
        """
        model = QStandardItemModel(0, 1, parent)
        return model

    def update_list(self, id, data):
        """
        Updates list

        :param id: ID of the list
        :param data: Data to update
        """
        self.window.models[id].removeRows(0, self.window.models[id].rowCount())
        i = 0
        for n in data:
            if 'name' in data[n]:
                self.window.models[id].insertRow(i)
                name = data[n]['name']
                if id == 'preset.presets':
                    if not n.startswith('current.'):
                        name = data[n]['name'] + ' (' + str(n) + ')'
                elif id == 'prompt.mode':
                    name = trans(name)
                self.window.models[id].setData(self.window.models[id].index(i, 0), name)
                i += 1

    def update_list_assistants(self, id, data):
        """
        Updates list

        :param id: ID of the list
        :param data: Data to update
        """
        self.window.models[id].removeRows(0, self.window.models[id].rowCount())
        i = 0
        for n in data:
            self.window.models[id].insertRow(i)
            name = data[n].name
            self.window.models[id].setData(self.window.models[id].index(i, 0), name)
            i += 1
