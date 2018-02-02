# Introduction
# ============
# 
# RIDE allows adding additional functionality via plugins. Several plugins are included in the basic installation, and additional plugins may be available from other sources.
# 
# Managing Plugins
# ================
# 
# Selecting ```Tools|Manage Plugins``` from main menu opens a Plugin manager. The
# available plugins are listed, and there's a possibility to activate/deactivate
# them.
# 
# Installing Plugins
# ------------------
# 
# See "Finding Plugins" in the [Plugin API documentation](https://github.com/robotframework/RIDE/blob/master/src/robotide/pluginapi/__init__.py)
# 
# 
# Plugin Development Template
# ------------------
# ```
# from pprint import pprint
# from robotide import publish
# from robotide.pluginapi import Plugin
# from robotide.publish import RideDataChanged
# 
# 
# class PulginTemp(Plugin):
#     """This plugin description."""
#     def __init__(self, ride_app_ref):
#         Plugin.__init__(self, ride_app_ref, initially_enabled=False)
# 
#     def enable(self):
#         self.log('Plugin template enabled')
# 
#         self.subscribe(self.OnRideDataChanged, RideDataChanged)
# 
#     def disable(self):
#         self.log('Plugin template disabled')
# 
#     def OnRideDataChanged(self, msg):
#         self.log('OnRideDataChanged')
#         self.__print_attrs(msg)
# 
#     # RIDE log
#     def log(self, data):
#         publish.RideLogMessage(data).publish()
# 
#     # Ensure the [log_to_console = True] in settings.cfg first.
#     def __print_attrs(self, object):
#         pprint([attr for attr in dir(object) if not callable(attr) and not attr.startswith('__')])
# ```
