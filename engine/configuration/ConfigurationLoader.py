import json
import os

class ConfigurationLoader:
    def __init__(self, configuration_file_path = "default_execution_configuration.json"):
        self.base_path = "engine/configuration/json/"
        self.configuration_file_path = configuration_file_path

    def get_default_configuration(self):
        configuration_file_final_path =  os.path.join(self.base_path, self.configuration_file_path)
        return json.load(open(configuration_file_final_path, "r"))
