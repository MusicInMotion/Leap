from abc import ABC, abstractmethod

class ShaderInterface(ABC):
    @abstractmethod
    def params(self):
        pass

    @abstractmethod
    def fragShader(self):
        pass
