#!/usr/bin/env python

from plugin_manager import PluginManager


def main():
    rulesInstances = []
    pm = PluginManager()
    for pi in pm.list_available():
	    pm.load(pi)
    pm.list_loaded()

    # rulesInstances.append(pm.loadedPlugins['p1'])

    # for r in rulesInstances:
    #     print r.description()

if __name__=='__main__':
    main()
