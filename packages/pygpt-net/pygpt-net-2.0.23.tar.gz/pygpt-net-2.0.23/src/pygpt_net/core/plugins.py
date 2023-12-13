#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.05 22:00:00                  #
# ================================================== #

class Plugins:
    def __init__(self, config):
        """
        Plugins handler

        :param config: Config
        """
        self.config = config
        self.plugins = {}

    def apply(self, id, event, data):
        """
        Applies plugin event

        :param id: Plugin id
        :param event: Event name
        :param data: Event data
        :return: Event data
        """
        if id in self.plugins:
            try:
                if event == 'input.before':
                    return self.plugins[id].on_input_before(data)
                elif event == 'ctx.before':
                    return self.plugins[id].on_ctx_before(data)
                elif event == 'ctx.after':
                    return self.plugins[id].on_ctx_after(data)
                elif event == 'ctx.begin':
                    return self.plugins[id].on_ctx_begin(data)
                elif event == 'ctx.end':
                    return self.plugins[id].on_ctx_end(data)
                elif event == 'system.prompt':
                    return self.plugins[id].on_system_prompt(data)
                elif event == 'ai.name':
                    return self.plugins[id].on_ai_name(data)
                elif event == 'user.name':
                    return self.plugins[id].on_user_name(data)
                elif event == 'user.send':
                    return self.plugins[id].on_user_send(data)
                elif event == 'enable':
                    return self.plugins[id].on_enable()
                elif event == 'disable':
                    return self.plugins[id].on_disable()
                elif event == 'cmd.syntax':
                    return self.plugins[id].cmd_syntax(data)
            except AttributeError:
                pass

        return data

    def apply_cmd(self, id, ctx, cmds):
        """
        Applies commands

        :param id: Plugin id
        :param ctx: Event data
        :return: Event data
        """
        if id in self.plugins:
            try:
                return self.plugins[id].cmd(ctx, cmds)
            except AttributeError:
                pass

        return ctx

    def is_registered(self, id):
        """
        Checks if plugin is registered

        :param id: Plugin id
        :return: True if registered
        """
        return id in self.plugins

    def register(self, plugin):
        """
        Registers plugin

        :param plugin: Plugin
        """
        id = plugin.id
        self.plugins[id] = plugin

        try:
            if id in self.config.data['plugins']:
                for key in self.config.data['plugins'][id]:
                    if key in self.plugins[id].options:
                        self.plugins[id].options[key]['value'] = self.config.data['plugins'][id][key]
        except Exception as e:
            print('Error while loading plugin options: {}'.format(id))
            print(e)
