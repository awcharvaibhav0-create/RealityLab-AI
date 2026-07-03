class PluginRegistry:
    def __init__(self):
        self.plugins = {}

    def register(self, name, instance):
        self.plugins[name] = instance

    def get_plugin(self, name):
        return self.plugins.get(name)

    def list_plugins(self):
        return list(self.plugins.keys())


plugin_registry = PluginRegistry()
