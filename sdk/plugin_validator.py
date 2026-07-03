class PluginValidator:
    def validate(self, manifest):
        return "version" in manifest


plugin_validator = PluginValidator()
