from engine.pipelines.internal.KnowledgeAcquisition import KnowledgeAcquisition
from engine.pipelines.PreprocessingPipeline import PreprocessingPipeline
from engine.pipelines.ProcessingPipeline import ProcessingPipeline
from engine.pipelines.internal.TimeSeries import TimeSeries
from engine.exceptions.InvalidUsageException import InvalidUsageException
from engine.configuration.ConfigurationLoader import ConfigurationLoader
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
import pandas as pd
import os
import typing

class EEGVisualizer:
    EEG_CHANNELS = ["ECoG F", "ECoG P", "STIM", "EKG"]

    def __init__(self, dataset_path = 'data', configuration = None):
        self.__init_configuration(configuration)
        self.__init_knowledge(dataset_path)
        self.__init_preprocessing_pipeline()
        self.__init_processing_pipeline()
        self.__init_t_sne_models()

    def __init_configuration(self, configuration):
        if configuration == None:
            configuration = self.__get_default_configuration()
        self.configuration = configuration

    def __get_default_configuration(self):
        return ConfigurationLoader().get_default_configuration()

    def __init_knowledge(self, dataset_path):
        self.files_name = []
        self.knowledge_acquisitions = []
        for file_name in os.listdir(dataset_path):
            self.knowledge_acquisitions.append(KnowledgeAcquisition(dataset_path, file_name))

            if file_name not in self.files_name:
                self.files_name.append(file_name)

    def __init_preprocessing_pipeline(self):
        self.preprocessing_pipeline = PreprocessingPipeline(self.configuration)
    
    def __init_processing_pipeline(self):
        self.processing_pipeline = ProcessingPipeline(self.configuration)

    def __init_t_sne_models(self):
        self.t_sne_models = []

        for t_sne_model_config in self.configuration["t_sne_models"]:
            t_sne_model_config_name = t_sne_model_config["model_name"]
            t_sne_parameters = t_sne_model_config["parameters"]
            self.t_sne_models.append(tuple([t_sne_model_config_name, TSNE(**t_sne_parameters)]))

    def build(self,
            files_name: typing.List[str] = [],
            eeg_channels: typing.List[str] = []) -> None:
        self.__load_time_series_list(files_name, eeg_channels)

    def __load_time_series_list(self, files_name, eeg_channels) -> None:
        files_name, eeg_channels = self.__validate_and_process_inputs(files_name, eeg_channels)

        time_series_list = []
        for knowledge_acquisition in self.knowledge_acquisitions:
            if knowledge_acquisition.file_name not in files_name:
                continue

            for biopac_channel in knowledge_acquisition.get_biopac_channels():
                if biopac_channel.name not in eeg_channels:
                    continue

                time_series_list.append(
                    TimeSeries(biopac_channel = biopac_channel)
                        .set_file_name_and_return(knowledge_acquisition.file_name)
                )

        self.time_series_list = time_series_list

    def execute(self) -> None:
        time_series_list = self.preprocessing_pipeline.execute(self.time_series_list)
        self.X, self.y = self.processing_pipeline.execute(time_series_list)
        self.__execute_t_snee()

    def __validate_and_process_inputs(self, files_name, eeg_channels):
        for file_name in files_name:
            if file_name not in self.files_name:
                raise InvalidUsageException("files_name", file_name)

        for eeg_channel in eeg_channels:
            if eeg_channel not in self.EEG_CHANNELS:
                raise InvalidUsageException("eeg_channels", eeg_channel)
        
        if len(files_name) == 0:
            files_name = self.files_name
        
        if len(eeg_channels) == 0:
            eeg_channels = self.EEG_CHANNELS
        
        return files_name, eeg_channels

    def describe(self):
        for knowledge_acquisition in self.knowledge_acquisitions:
            print("file_name", knowledge_acquisition.file_name)
            for biopac_channel in knowledge_acquisition.get_biopac_channels():
                print("\tbiopac_channel", biopac_channel.name)

    def __execute_t_snee(self):
        self.t_sne_dataframes = dict()
        for (t_sne_model_name, t_sne_model) in self.t_sne_models:
            tsne_data = t_sne_model.fit_transform(self.X)
    
            t_sne_y = self.__get_y_for_t_sne()
            tsne_data = np.vstack((tsne_data.T, t_sne_y)).T

            t_sne_dataframe = pd.DataFrame(data=tsne_data, columns=("First dimension", "Second dimension", "label"))
            t_sne_dataframe["label"] = self.y

            self.t_sne_dataframes[t_sne_model_name] = t_sne_dataframe
                
    def __get_y_for_t_sne(self):
        unique_labels = np.array(list(set(self.y)))
        return list(map(lambda label: np.where(unique_labels == label)[0][0], self.y))

    def plot(self):
        combined_df = pd.DataFrame(columns=("First dimension", "Second dimension", "label", "model_name"))
        for t_sne_model_name in self.t_sne_dataframes:
            t_sne_dataframe = self.t_sne_dataframes[t_sne_model_name]

            # column used for grouped plot
            t_sne_dataframe["model_name"] = t_sne_model_name            

            combined_df = combined_df.append(t_sne_dataframe)
        
        sn.set(font_scale=1.35)
        sn.FacetGrid(combined_df, hue="label", col="model_name", col_wrap=4, height=6) \
            .map(plt.scatter, "First dimension", "Second dimension") \
            .add_legend()
        plt.show()
