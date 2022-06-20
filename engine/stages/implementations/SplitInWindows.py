from engine.stages.PreprocessingStage import PreprocessingStage
from engine.internal.TimeSeries import TimeSeries
import typing
import numpy as np

class SplitInWindows(PreprocessingStage):
    def __init__(self, kwargs):
        self.window_size = kwargs["window_size"]

    def execute(self, time_series_list: typing.List[TimeSeries]) -> typing.List[TimeSeries]:
        new_time_series_list = []
        for time_series in time_series_list:
            time_data_windows = self.cut_time_data_in_windows(time_series.time_data, self.window_size)
            for time_data_window in time_data_windows:
                new_time_series_list.append(time_series.clone_with_new_time_data(time_data_window))
        
        return np.array(new_time_series_list)

    def cut_time_data_in_windows(self, time_data, window_size):
        return self.__cut_in_chunks_of_n_and_drop_rest(time_data, window_size)
    
    def __cut_in_chunks_of_n_and_drop_rest(self, array, chunk_size):
        result = []
        array_length = len(array)

        for index in range(0, array_length, chunk_size):
            if (index + chunk_size > array_length):
                break
                
            result.append(array[index: index + chunk_size])
        
        return result
