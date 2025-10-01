import pygame
from abc import abstractmethod, ABC
from carro import Carro

class PocionesInterface(ABC):
    def __init__(self, nombre: str, descripcion: str, duracion: int):
        self.nombre = nombre
        self.descripcion = descripcion
        self.duracion = duracion  # Duración en segundos
        self.tiempo_inicio = 0
        super().__init__()

    @abstractmethod
    def operar(self, carro: Carro):
        ...

    def ha_expirado(self):
        # Verifica si el tiempo de la poción ha expirado
        if self.tiempo_inicio == 0:
            return False
        tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicio) / 1000
        return tiempo_transcurrido >= self.duracion