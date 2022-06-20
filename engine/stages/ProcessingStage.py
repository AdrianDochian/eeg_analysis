from abc import ABC, abstractmethod
import numpy as np
import typing

class ProcessingStage(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def execute(self, X: np.array, X_extra_information: np.array) -> typing.Tuple[np.array, np.array]:
        pass