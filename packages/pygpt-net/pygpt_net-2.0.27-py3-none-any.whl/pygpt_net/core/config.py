#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.14 11:00:00                  #
# ================================================== #

import datetime
import os
import re
from pathlib import Path
import shutil
import json


class Config:
    CONFIG_DIR = 'pygpt-net'
    TYPE_STR = 0
    TYPE_INT = 1
    TYPE_FLOAT = 2
    TYPE_BOOL = 3

    def __init__(self):
        """Config handler"""
        self.path = str(Path(os.path.join(Path.home(), '.config', self.CONFIG_DIR)))
        self.initialized = False
        self.models = {}
        self.data = {}
        self.presets = {}
        self.assistants = {}
        self.version = self.get_version()

    def get_root_path(self):
        """
        Returns local data path

        :return: local data path
        """
        if __file__.endswith('.pyc'):  # if compiled with pyinstaller
            return os.path.abspath('.')
        else:
            return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    def get_available_langs(self):
        """
        Returns list with available languages

        :return: list with available languages
        """
        langs = []
        path = os.path.join(self.get_root_path(), 'data', 'locale')
        if not os.path.exists(path):
            return langs

        for file in os.listdir(path):
            if file.endswith(".ini"):
                langs.append(file.replace('locale.', '').replace('.ini', ''))

        # make English first
        if 'en' in langs:
            langs.remove('en')
            langs.insert(0, 'en')
        return langs

    def init(self, all=True, log=False):
        """
        Initializes config

        :param all: load all configs
        :param log: log loading
        """
        if not self.initialized:
            if all:
                v = self.get_version()
                print("Starting PYGPT v{}".format(v))
            self.install()
            self.load(all, log)
            self.initialized = True

    def get_version(self):
        """
        Returns version

        :return: version string
        """
        path = os.path.abspath(os.path.join(self.get_root_path(), '__init__.py'))
        try:
            f = open(path, "r", encoding="utf-8")
            data = f.read()
            f.close()
            result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format("__version__"), data)
            return result.group(1)
        except Exception as e:
            print(e)

    def load(self, all=True, log=False):
        """
        Loads config

        :param all: load all configs
        :param log: log loading
        """
        self.load_config(log)

        if all:
            self.load_models(log)
            self.load_presets()

    def save_preset(self, preset):
        """
        Saves preset into JSON file

        :param preset: preset name (id)
        """
        if preset not in self.presets:
            return

        filepath = os.path.join(self.path, 'presets', preset + '.json')
        try:
            f = open(filepath, "w", encoding="utf-8")
            json.dump(self.presets[preset], f, indent=4)
            f.close()
        except Exception as e:
            print(e)

    def load_models(self, log=False):
        """
        Loads models config from JSON file

        :param log: log loading
        """
        path = os.path.join(self.path, 'models.json')
        if not os.path.exists(path):
            print("FATAL ERROR: {} not found!".format(path))
            return None
        try:
            f = open(path, "r", encoding="utf-8")
            self.models = json.load(f)
            self.models = dict(sorted(self.models.items(), key=lambda item: item[0]))  # sort by key
            f.close()
            if log:
                print("Loaded models: {}".format(path))
        except Exception as e:
            print(e)

    def load_config(self, log=False):
        """
        Loads user config from JSON file

        :param log: log loading
        """
        path = os.path.join(self.path, 'config.json')
        if not os.path.exists(path):
            print("FATAL ERROR: {} not found!".format(path))
            return None
        try:
            f = open(path, "r", encoding="utf-8")
            self.data = json.load(f)
            self.data = dict(sorted(self.data.items(), key=lambda item: item[0]))  # sort by key
            f.close()
            if log:
                print("Loaded config: {}".format(path))
        except Exception as e:
            print(e)

    def load_base_config(self, log=False):
        """
        Loads app config from JSON file

        :param log: log loading
        """
        path = os.path.join(self.get_root_path(), 'data', 'config', 'config.json')
        if not os.path.exists(path):
            print("FATAL ERROR: {} not found!".format(path))
            return None
        try:
            f = open(path, "r", encoding="utf-8")
            self.data = json.load(f)
            self.data = dict(sorted(self.data.items(), key=lambda item: item[0]))  # sort by key
            f.close()
            if log:
                print("Loaded default app config: {}".format(path))
        except Exception as e:
            print(e)

    def sort_presets_by_name(self):
        """Sorts presets by name"""
        pass  # TODO

    def load_presets(self):
        """Loads presets templates from JSON files"""
        path = os.path.join(self.path, 'presets')
        if not os.path.exists(path):
            print("FATAL ERROR: {} not found!".format(path))
            return None
        try:
            for filename in os.listdir(path):
                if filename.endswith(".json"):
                    f = open(os.path.join(path, filename), "r", encoding="utf-8")
                    self.presets[filename[:-5]] = json.load(f)
                    f.close()
            self.sort_presets_by_name()
            self.append_current_presets()
        except Exception as e:
            print(e)

    def build_empty_preset(self):
        """
        Builds empty preset

        :return: dict with empty preset
        """
        return {
            'name': '',
            'ai_name': '',
            'user_name': '',
            'prompt': '',
            'chat': False,
            'completion': False,
            'img': False,
            'vision': False,
            'langchain': False,
            'assistant': False,
            'temperature': 1.0,
        }

    def append_current_presets(self):
        """Appends current presets"""
        # create empty presets
        curr_chat = self.build_empty_preset()
        curr_completion = self.build_empty_preset()
        curr_img = self.build_empty_preset()
        curr_vision = self.build_empty_preset()
        curr_langchain = self.build_empty_preset()
        curr_assistant = self.build_empty_preset()

        # prepare ids
        id_chat = 'current.chat'
        id_completion = 'current.completion'
        id_img = 'current.img'
        id_vision = 'current.vision'
        id_langchain = 'current.langchain'
        id_assistant = 'current.assistant'

        # set default initial prompt for chat mode
        curr_chat['prompt'] = self.data['default_prompt']

        # get data from presets if exists
        if id_chat in self.presets:
            curr_chat = self.presets[id_chat].copy()
            del self.presets[id_chat]
        if id_completion in self.presets:
            curr_completion = self.presets[id_completion].copy()
            del self.presets[id_completion]
        if id_img in self.presets:
            curr_img = self.presets[id_img].copy()
            del self.presets[id_img]
        if id_vision in self.presets:
            curr_vision = self.presets[id_vision].copy()
            del self.presets[id_vision]
        if id_langchain in self.presets:
            curr_langchain = self.presets[id_langchain].copy()
            del self.presets[id_langchain]
        if id_assistant in self.presets:
            curr_assistant = self.presets[id_assistant].copy()
            del self.presets[id_assistant]

        # allow usage in specific mode
        curr_chat['chat'] = True
        curr_completion['completion'] = True
        curr_img['img'] = True
        curr_vision['vision'] = True
        curr_langchain['langchain'] = True
        curr_assistant['assistant'] = True

        # always apply default name
        curr_chat['name'] = '*'
        curr_completion['name'] = '*'
        curr_img['name'] = '*'
        curr_vision['name'] = '*'
        curr_langchain['name'] = '*'
        curr_assistant['name'] = '*'

        # append at first position
        self.presets = {
            id_chat: curr_chat,
            id_completion: curr_completion,
            id_img: curr_img,
            id_vision: curr_vision,
            id_langchain: curr_langchain,
            id_assistant: curr_assistant,
            **self.presets
        }

    def get_mode_by_idx(self, idx):
        """
        Returns mode by index

        :param idx: index of mode
        :return: mode name
        """
        modes = self.get_modes()
        return list(modes.keys())[idx]

    def get_model_by_idx(self, idx, mode):
        """
        Returns model by index

        :param idx: index of model
        :param mode: mode name
        :return: model name
        """
        models = self.get_models(mode)
        return list(models.keys())[idx]

    def get_preset_by_idx(self, idx, mode):
        """
        Returns preset by index

        :param idx: index
        :param mode: mode
        :return: preset name
        """
        presets = self.get_presets(mode)
        return list(presets.keys())[idx]

    def get_modes(self):
        """
        Returns modes

        :return: modes dict
        """
        modes = {}
        modes['chat'] = {
            'name': 'mode.chat'
        }
        modes['completion'] = {
            'name': 'mode.completion'
        }
        modes['img'] = {
            'name': 'mode.img'
        }
        modes['vision'] = {
            'name': 'mode.vision'
        }
        modes['assistant'] = {
            'name': 'mode.assistant'
        }
        modes['langchain'] = {
            'name': 'mode.langchain'
        }
        return modes

    def get_presets(self, mode):
        """
        Returns presets for mode

        :param mode: mode name
        :return: presets dict for mode
        """
        presets = {}
        for key in self.presets:
            if (mode == 'chat' and 'chat' in self.presets[key] and self.presets[key]['chat']) \
                    or (mode == 'completion' and 'completion' in self.presets[key] and self.presets[key]['completion']) \
                    or (mode == 'img' and 'img' in self.presets[key] and self.presets[key]['img']) \
                    or (mode == 'vision' and 'vision' in self.presets[key] and self.presets[key]['vision']) \
                    or (mode == 'langchain' and 'langchain' in self.presets[key] and self.presets[key]['langchain']) \
                    or (mode == 'assistant' and 'assistant' in self.presets[key] and self.presets[key]['assistant']):
                presets[key] = self.presets[key]
        return presets

    def get_models(self, mode):
        """
        Returns models for mode

        :param mode: mode name
        :return: models dict for mode
        """
        models = {}
        for key in self.models:
            if key == '__meta__':
                continue
            if mode in self.models[key]['mode']:
                models[key] = self.models[key]
        return models

    def get_preset_idx(self, mode, name):
        """
        Returns preset index

        :param mode: mode name
        :param name: name of preset
        :return: index of preset
        """
        presets = self.get_presets(mode)
        i = 0
        for key in presets:
            if key == name:
                return i
            i += 1
        return 0

    def delete_preset(self, name, remove_file=True):
        """
        Deletes preset

        :param name: name of preset
        :param remove_file: also remove preset JSON config file
        """
        if name in self.presets:
            self.presets.pop(name)

        if remove_file:
            path = os.path.join(self.path, 'presets', name + '.json')
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    print(e)
            self.load_presets()

    def get_default_mode(self):
        """
        Returns default mode name

        :return: default mode name
        """
        return 'chat'

    def get_default_model(self, mode):
        """
        Returns default model for mode

        :param mode: mode name
        :return: default model name
        """
        models = {}
        items = self.get_models(mode)
        for k in items:
            if k == "__meta__":
                continue
            models[k] = items[k]
        if len(models) == 0:
            return None
        return list(models.keys())[0]

    def get_default_preset(self, mode):
        """
        Returns default preset for mode

        :param mode: mode name
        :return: default prompt name
        """
        presets = self.get_presets(mode)
        if len(presets) == 0:
            return None
        return list(presets.keys())[0]

    def get_preset_duplicate_name(self, name):
        """
        Prepares name for duplicated preset

        :param name: name of preset
        :return: name of duplicated preset
        """
        old_name = self.presets[name]['name']
        i = 1
        while True:
            new_name = name + '_' + str(i)
            if new_name not in self.presets:
                return new_name, old_name + ' (' + str(i) + ')'
            i += 1

    def duplicate_preset(self, name):
        """
        Makes preset duplicate

        :param name: name of preset
        :return: duplicated preset name (ID)
        """
        id, title = self.get_preset_duplicate_name(name)
        self.presets[id] = self.presets[name].copy()
        self.presets[id]['name'] = title
        self.sort_presets_by_name()
        return id

    def save(self, filename='config.json'):
        """Saves config into file"""
        self.data['__meta__'] = self.append_meta()
        dump = json.dumps(self.data, indent=4)
        path = os.path.join(self.path, filename)
        try:
            with open(path, 'w', encoding="utf-8") as f:
                f.write(dump)
                f.close()
        except Exception as e:
            print(e)

    def save_models(self):
        """Saves models config into file"""
        self.models['__meta__'] = self.append_meta()
        dump = json.dumps(self.models, indent=4)
        path = os.path.join(self.path, 'models.json')
        try:
            with open(path, 'w', encoding="utf-8") as f:
                f.write(dump)
                f.close()
        except Exception as e:
            print(e)

    def save_presets(self):
        """Saves presets into files"""
        for key in self.presets:
            self.presets[key]['__meta__'] = self.append_meta()
            path = os.path.join(self.path, 'presets', key + '.json')
            dump = json.dumps(self.presets[key], indent=4)
            try:
                with open(path, 'w', encoding="utf-8") as f:
                    f.write(dump)
                    f.close()
            except Exception as e:
                print(e)

    def get_model_tokens(self, model):
        """
        Returns model tokens

        :param model: model name
        :return: number of tokens
        """
        if model in self.models:
            return self.models[model]['tokens']
        return 1

    def get_model_ctx(self, model):
        """
        Returns model context window tokens

        :param model: model name
        :return: number of ctx tokens
        """
        if model in self.models:
            return self.models[model]['ctx']
        return 4096

    def get_model_cfg(self, model):
        """
        Returns model context window tokens

        :param model: model name
        :return: number of ctx tokens
        """
        if model in self.models:
            return self.models[model]

    def append_meta(self):
        """
        Appends meta data

        :return: meta data dict
        """
        return {
            'version': self.version,
            'app.version': self.version,
            'updated_at': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }

    def install(self):
        """Installs config files"""
        try:
            # create user config directory
            path = Path(self.path)
            path.mkdir(parents=True, exist_ok=True)

            # install config file
            dst = os.path.join(self.path, 'config.json')
            if not os.path.exists(dst):
                src = os.path.join(self.get_root_path(), 'data', 'config', 'config.json')
                shutil.copyfile(src, dst)

            # install models file
            dst = os.path.join(self.path, 'models.json')
            if not os.path.exists(dst):
                src = os.path.join(self.get_root_path(), 'data', 'config', 'models.json')
                shutil.copyfile(src, dst)

            # install prompt presets
            presets_dir = os.path.join(self.path, 'presets')
            if not os.path.exists(presets_dir):
                src = os.path.join(self.get_root_path(), 'data', 'config', 'presets')
                shutil.copytree(src, presets_dir)
            else:
                # copy missing presets
                src = os.path.join(self.get_root_path(), 'data', 'config', 'presets')
                for file in os.listdir(src):
                    src_file = os.path.join(src, file)
                    dst_file = os.path.join(presets_dir, file)
                    if not os.path.exists(dst_file):
                        shutil.copyfile(src_file, dst_file)

            # create history directory
            history_dir = os.path.join(self.path, 'history')
            if not os.path.exists(history_dir):
                os.mkdir(history_dir)

            # create context directory
            context_dir = os.path.join(self.path, 'context')
            if not os.path.exists(context_dir):
                os.mkdir(context_dir)

            # create images directory
            img_dir = os.path.join(self.path, 'img')
            if not os.path.exists(img_dir):
                os.mkdir(img_dir)

            # create output files directory
            files_dir = os.path.join(self.path, 'output')
            if not os.path.exists(files_dir):
                os.mkdir(files_dir)

            # create img capture directory
            capture_dir = os.path.join(self.path, 'capture')
            if not os.path.exists(capture_dir):
                os.mkdir(capture_dir)

        except Exception as e:
            print(e)
