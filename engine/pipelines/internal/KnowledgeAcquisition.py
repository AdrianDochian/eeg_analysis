import bioread
import os
import typing

class KnowledgeAcquisition:
    def __init__(self, dataset_path: str, file_name: str):
        file_absolute_path = os.path.join(dataset_path, file_name)

        self.file_name = file_name
        self.knowledge_acquisition: bioread.biopac.Datafile = bioread.read_file(file_absolute_path)

    def get_biopac_channels(self) -> typing.List[bioread.biopac.Channel]:
        return self.knowledge_acquisition.channels
