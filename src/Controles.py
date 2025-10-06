import pygame

class Controles():
    def __init__(self):
        self.nombre = "Control genérico"

    def get_nombre(self):
        return self.nombre

    def mover_izquierda(self):
        raise NotImplementedError

    def mover_derecha(self):
        raise NotImplementedError


class MouseAdapter(Controles):
    def __init__(self):
        super().__init__()
        self.nombre = "Mouse"

    def mover_izquierda(self):
        botones = pygame.mouse.get_pressed()
        return botones[0]

    def mover_derecha(self):
        botones = pygame.mouse.get_pressed()
        return botones[2]  


class TecladoAdapterWASD(Controles):
    def __init__(self):
        super().__init__()
        self.nombre = "Teclado WASD"

    def mover_izquierda(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_a]

    def mover_derecha(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_d]

class TecladoAdapterFlechas(Controles):
    def __init__(self):
        super().__init__()
        self.nombre = "Teclado Flechas"

    def mover_izquierda(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_LEFT]

    def mover_derecha(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_RIGHT]


class ControladorCompuesto(Controles):
    def __init__(self, controles_list):
        super().__init__()
        self.controles_list = controles_list
        self.nombre = "Control Compuesto"

    def mover_izquierda(self):
        return any(control.mover_izquierda() for control in self.controles_list)

    def mover_derecha(self):
        return any(control.mover_derecha() for control in self.controles_list)
