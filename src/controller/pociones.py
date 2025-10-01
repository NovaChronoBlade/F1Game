import pygame
from models.carro import Carro
from models.pocion import PocionesInterface

class PocionVelocidad(PocionesInterface):
    def __init__(self, duracion: int, aumento_velocidad: int):
        super().__init__("Poción de Velocidad", "Aumenta la velocidad del carro", duracion)
        self.aumento_velocidad = aumento_velocidad

    def operar(self, carro: Carro):
        print("Poción de Velocidad aplicada.")
        carro.velocidad += self.aumento_velocidad
        self.tiempo_inicio = pygame.time.get_ticks()

    def revertir(self, carro: Carro):
        print("Poción de Velocidad expirada.")
        carro.velocidad -= self.aumento_velocidad

class PocionLentitud(PocionesInterface):
    def __init__(self, duracion: int, disminuir_velocidad: int):
        super().__init__("Poción de Lentitud", "Disminuye la velocidad del carro", duracion)
        self.disminuir_velocidad = disminuir_velocidad

    def operar(self, carro: Carro):
        print("Poción de Lentitud aplicada.")
        carro.velocidad -= self.disminuir_velocidad
        self.tiempo_inicio = pygame.time.get_ticks()

    def revertir(self, carro: Carro):
        print("Poción de Lentitud expirada.")
        carro.velocidad += self.disminuir_velocidad

class PocionEscudo(PocionesInterface):
    def __init__(self, duracion: int):
        super().__init__("Poción de Escudo", "Hace al carro invulnerable", duracion)

    def operar(self, carro: Carro):
        print("Poción de Escudo aplicada.")
        carro.inmunidad = True
        self.tiempo_inicio = pygame.time.get_ticks()

    def revertir(self, carro: Carro):
        print("Poción de Escudo expirada.")
        carro.inmunidad = False