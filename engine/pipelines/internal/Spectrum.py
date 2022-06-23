from engine.pipelines.internal.TimeSeries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np
import copy

class Spectrum:
    BRAIN_WAVES_DEFINITIONS = {
        "delta": {"name" : "Delta wave", "low" : 1, "high" : 4},
        "theta": {"name" : "Theta wave", "low" : 4, "high" : 8},
        "alpha": {"name" : "Alpha wave", "low" : 8, "high" : 12},
        "beta": {"name" : "Beta wave", "low" : 13, "high" : 30},
        "low_gamma": {"name" : "Low Gamma wave", "low" : 30, "high" : 70},
        "high_gamma": {"name" : "High Gamma wave", "low" : 70, "high" : 150}
    }
    
    def __init__(self, time_series: TimeSeries):
        self.name = time_series.name
        self.sampling_frequency = time_series.sampling_frequency
        self.spectrum_data_length = time_series.time_data_length
        self.spectrum_data = np.fft.fft(time_series.time_data)
        self.measuring_unit = time_series.measuring_unit
        self.frequencies = np.fft.fftfreq(self.spectrum_data_length, 1 / self.sampling_frequency)

    def get_coefficients_sum(self) -> float:
        return np.where(self.spectrum_data > 0)[0].sum()

    def band_pass_brain_wave(self, brain_wave) -> object:
        brain_wave_definition = Spectrum.BRAIN_WAVES_DEFINITIONS[brain_wave]
        return self.band_pass_filter(brain_wave_definition["low"], brain_wave_definition["high"])

    def band_pass_filter(self, low_cut_off: float, high_cut_off: float) -> object:
        spectrum_frequencies = self.frequencies

        # cutting the lower frequencies
        filtered_spectrum_data = self.spectrum_data * (np.absolute(spectrum_frequencies) > low_cut_off) 
        
        # cutting the higher frequencies
        filtered_spectrum_data = filtered_spectrum_data * (np.absolute(spectrum_frequencies) < high_cut_off)
        
        return self.new_spectrum(filtered_spectrum_data)

    def new_spectrum(self, new_spectrum_data: np.array) -> object:
        new_spectrum = copy.deepcopy(self)
        new_spectrum.spectrum_data = new_spectrum_data
        return new_spectrum

    def to_time_series(self) -> TimeSeries:
        time_data = np.real(np.fft.ifft(self.spectrum_data))
        
        return TimeSeries(
            name = self.name,
            sampling_frequency = self.sampling_frequency,
            time_data_length = len(time_data),
            time_data = time_data,
            measuring_unit = self.measuring_unit
        )

    def plot(self, from_index: int = None, to_index:int  = None) -> None:
        spectrum_data = abs(self.spectrum_data[0: int(self.spectrum_data_length / 2)])
        spectrum_x = self.frequencies[0: int(self.spectrum_data_length / 2)]

        if from_index != None:
            from_index = int(from_index * self.spectrum_data_length / self.sampling_frequency)
        
        if to_index != None:
            to_index = int(to_index * self.spectrum_data_length / self.sampling_frequency)
        
        if from_index != None and to_index != None:
            spectrum_data = spectrum_data[from_index:to_index]
            spectrum_x = spectrum_x[from_index:to_index]
        elif from_index != None:
            spectrum_data = spectrum_data[from_index:]
            spectrum_x = spectrum_x[from_index:]
        elif to_index != None:
            spectrum_data = spectrum_data[:to_index]
            spectrum_x = spectrum_x[:to_index]
        
        plt.figure(figsize=(12,3), dpi= 100, facecolor='w', edgecolor='k')
        plt.xlabel('Frequency');
        plt.ylabel('Power');
        plt.stem(spectrum_x, spectrum_data)
