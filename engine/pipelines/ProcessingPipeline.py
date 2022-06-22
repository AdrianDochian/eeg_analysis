from engine.pipelines.stages.implementations.FeatureExtractor import FeatureExtractor
from engine.pipelines.stages.StageLoader import StageLoader
import typing
import numpy as np

class ProcessingPipeline:
    def __init__(self, configuration):
        self.processing_stages = self.__init_processing_stages(configuration)

    def __init_processing_stages(self, configuration):
        processing_stages = []
        
        for processing_pipeline_stage in configuration["processing_pipeline_stages"]:
            stage_name = processing_pipeline_stage["stage_name"]
            constructor_kwargs = processing_pipeline_stage["constructor_kwargs"]
            
            stage_class_definition = StageLoader(stage_name, stage_name).get_class_definition()
            stage_instance = stage_class_definition(constructor_kwargs)
            
            processing_stages.append(stage_instance)
        
        return processing_stages

    def execute(self, time_series_list) -> typing.Tuple[np.array, np.array]:
        X = np.array(list(map(lambda time_series: time_series.time_data, time_series_list)))
        X_extra_information = np.array(list( \
            map(lambda time_series: {"sampling_frequency": time_series.sampling_frequency}, time_series_list)\
        ))
        y = np.array(list(map(lambda time_series: time_series.name + "_" + time_series.file_name, time_series_list)))

        for processing_stage in self.processing_stages:
            X, X_extra_information = processing_stage.execute(X, X_extra_information)

        return X, y
