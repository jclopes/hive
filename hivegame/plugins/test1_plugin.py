# test plugin
# this should be loaded dynamicly by the plugin manager

from plugin import PluginInterface


class Plugin(PluginInterface):

    def __init__(self):
        self._description = 'Test1 Plugin'

    def description(self):
        return self._description
