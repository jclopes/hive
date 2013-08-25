# Plugin manager

import json
import imp
import os.path

class PluginManager(object):
    """
    This class is responsible to find and load the hive plugins
    """

    def __init__(self):
        configFile = open('plugin_conf.js', 'r')
        self.config = json.load(configFile)

        self.pluginFolder = 'plugins'
        self.loadedPlugins = {}

    def load(self, pluginId):
        """
        Loads the plugin with id = pluginId
        """
        pFileName = pluginId + '.py'
        try:
            pPath = os.path.join(self.pluginFolder, pFileName)
            pFile = open(pPath, 'r')
        except IOError, e:
            return False
        
        try:
            dymod = imp.load_source(pluginId, pPath, pFile)
            self.loadedPlugins[pluginId] = dymod.Plugin()
        except ImportError, e:
            return False
        finally:
            pFile.close()

        return True    

    def list_available(self):
        """
        List all plugins available
        returns a list of tuples (id, name, description)
        """
        return self.config['plugins']

    def list_loaded(self):
        """
        List all plugins available
        returns a list of tuples (id, name, description)
        """
        for p in self.loadedPlugins:
            print '(%s, %s)' % (p, self.loadedPlugins[p].description())
