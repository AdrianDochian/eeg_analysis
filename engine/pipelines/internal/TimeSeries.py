import matplotlib.pyplot as plt
import bioread
import numpy as np

class TimeSeries:
    def __init__(self, **kwargs):
        if "biopac_channel" in kwargs:
            self.init_from_biopac_channel(kwargs["biopac_channel"])
        else:
            self.__init_from_data(**kwargs)

    
    def init_from_biopac_channel(self, biopac_channel: bioread.biopac.Channel) -> None:
        self.__init_from_data(
            name = biopac_channel.name,
            sampling_frequency = biopac_channel.samples_per_second,
            time_data_length = biopac_channel.point_count,
            time_data = biopac_channel.data,
            measuring_unit = biopac_channel.units
        )

    def __init_from_data(self, **kwargs) -> None:
        self.name = kwargs["name"]
        self.sampling_frequency = kwargs["sampling_frequency"]
        self.time_data_length = kwargs["time_data_length"]
        self.time_data = kwargs["time_data"]
        self.measuring_unit = kwargs["measuring_unit"]
        
        if "file_name" in kwargs:
            self.file_name = kwargs["file_name"]
    
    def set_file_name_and_return(self, file_name: str) -> object:
        self.file_name = file_name
        return self

    def clone_with_new_time_data(self, new_time_data) -> object:
        return TimeSeries(
            name = self.name,
            sampling_frequency = self.sampling_frequency,
            time_data = new_time_data,
            time_data_length = len(new_time_data),
            measuring_unit = self.measuring_unit,
            file_name = self.file_name
        )

    def describe(self):
        description = {
            "measuring_unit": "{}".format(self.measuring_unit),
            "sampling_frequency": "{:.2f}".format(self.sampling_frequency), 
            "seconds": "{:.2f}".format(self.time_data_length / self.sampling_frequency), 
            "mean": "{:.4f}".format(self.time_data.mean()), 
            "deviation": "{:.4f}".format(self.time_data.std()), 
            "min": "{:.4f}".format(self.time_data.min()), 
            "max": "{:.4f}".format(self.time_data.max()), 
        }
        print(description)
        return description

    def plot(self):
        time_data_ox_axis = np.linspace(0, self.time_data_length - 1, self.time_data_length)

        plt.figure(figsize=(12,3), dpi= 100, facecolor='w', edgecolor='k')
        plt.plot(time_data_ox_axis, self.time_data,
                color = 'red',
                label="({})".format(self.name)); 
        plt.xlabel("Time(s)")
        plt.ylabel('Amplitude(' + self.measuring_unit + ")")
        plt.legend()
