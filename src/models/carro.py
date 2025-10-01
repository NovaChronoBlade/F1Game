from abc import abstractmethod, ABC

class Carro(ABC):
    def __init__(self, velocidad: int, inmunidad: bool = False):
        self.velocidad = velocidad
        self.inmunidad = inmunidad
        super().__init__()

    @abstractmethod
    def correr():
        ...