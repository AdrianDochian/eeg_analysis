from engine.pipelines.internal.TimeSeries import TimeSeries
from engine.pipelines.stages.StageLoader import StageLoader
import typing

class PreprocessingPipeline:
    def __init__(self, configuration):
        self.preprocessing_stages = self.__init_preprocessing_stages(configuration)
    
    def __init_preprocessing_stages(self, configuration):
        preprocessing_stages = []
        
        for preprocessing_pipeline_stage in configuration["preprocessing_pipeline_stages"]:
            stage_name = preprocessing_pipeline_stage["stage_name"]
            constructor_kwargs = preprocessing_pipeline_stage["constructor_kwargs"]
            
            stage_class_definition = StageLoader(stage_name, stage_name).get_class_definition()
            stage_instance = stage_class_definition(constructor_kwargs)
            
            preprocessing_stages.append(stage_instance)
        
        return preprocessing_stages

    def execute(self, time_series_list) -> typing.List[TimeSeries]:
        for preprocessing_stage in self.preprocessing_stages:
            time_series_list = preprocessing_stage.execute(time_series_list)
        return time_series_list
