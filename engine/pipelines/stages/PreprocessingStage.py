from abc import ABC, abstractmethod
import typing
from engine.pipelines.internal.TimeSeries import TimeSeries

class PreprocessingStage(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def execute(self, time_series_list: typing.List[TimeSeries]) -> typing.List[TimeSeries]:
        pass
