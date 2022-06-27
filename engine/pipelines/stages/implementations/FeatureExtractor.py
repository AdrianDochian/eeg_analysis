from engine.pipelines.internal.Spectrum import Spectrum
from engine.pipelines.stages.ProcessingStage import ProcessingStage
from engine.pipelines.internal.TimeSeries import TimeSeries
import numpy as np
import typing

class FeatureExtractor(ProcessingStage):
    def __init__(self, kwargs):
        self.features = kwargs["features"]

    def execute(self, X: np.array, X_extra_information: np.array) -> typing.Tuple[np.array, np.array]:
        new_X = []
        for row_index in range(len(X)):
            row = X[row_index]
            row_extra_information = X_extra_information[row_index]
            new_row = []
            for feature in self.features:
                feature_method = getattr(self, feature)
                new_row.append(feature_method(row, row_extra_information))

            new_X.append(np.array(new_row))
        return np.array(new_X), X_extra_information
    
    def alpha_spectrum_coeffiecients_mean(self, array : np.array, array_extra_information: dict):
        return self.__get_coeffiecients_mean_for_brain_wave(array, array_extra_information, "alpha")

    def beta_spectrum_coeffiecients_mean(self, array : np.array, array_extra_information: dict):
        return self.__get_coeffiecients_mean_for_brain_wave(array, array_extra_information, "beta")
    
    def low_gamma_spectrum_coeffiecients_mean(self, array : np.array, array_extra_information: dict):
        return self.__get_coeffiecients_mean_for_brain_wave(array, array_extra_information, "low_gamma")
    
    def high_gamma_spectrum_coeffiecients_mean(self, array : np.array, array_extra_information: dict):
        return self.__get_coeffiecients_mean_for_brain_wave(array, array_extra_information, "high_gamma")
    
    def delta_spectrum_coeffiecients_mean(self, array : np.array, array_extra_information: dict):
        return self.__get_coeffiecients_mean_for_brain_wave(array, array_extra_information, "delta")
    
    def theta_spectrum_coeffiecients_mean(self, array : np.array, array_extra_information: dict):
        return self.__get_coeffiecients_mean_for_brain_wave(array, array_extra_information, "theta")

    def mean(self, array : np.array, _):
        return array.mean()
    
    def standard_deviation(self, array : np.array, _):
        return array.std() 
    
    def __get_coeffiecients_mean_for_brain_wave(self, array: np.array, array_extra_information: dict, brain_wave: str):
        time_series = self.__get_time_series_from_array(array, array_extra_information)
        return Spectrum(time_series)\
            .band_pass_brain_wave(brain_wave)\
            .get_coefficients_mean()

    def __get_time_series_from_array(self, array, array_extra_information):
        return TimeSeries(
            name = "",
            sampling_frequency = array_extra_information["sampling_frequency"],
            time_data_length = len(array),
            time_data = array,
            measuring_unit = ""
        )
