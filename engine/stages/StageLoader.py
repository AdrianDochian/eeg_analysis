import importlib

class StageLoader:
    PACKAGE_NAME = "engine.stages.implementations"

    def __init__(self, file_name, class_name):
        self.file_name = file_name
        self.class_name = class_name

    def get_class_definition(self):
        return getattr(importlib.import_module(self.__get_module_name()), self.class_name)
    
    def __get_module_name(self):
        return ".".join([StageLoader.PACKAGE_NAME, self.file_name])

