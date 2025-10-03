import pygame
import random


class PocionItem:
    """Representa una poción física que aparece en la pista"""
    
    TIPOS_POCIONES = {
        "velocidad": "assets/images/pocion_velocidad.png",
        "lentitud": "assets/images/pocion_lentitud.png",
        "inmunidad": "assets/images/pocion_inmunidad.png"
    }
    
    def __init__(self, x, y, tipo, velocidad=5):
        """
        Poción que aparece en la pista
        :param x: Posición inicial en x
        :param y: Posición inicial en y
        :param tipo: Tipo de poción ('velocidad', 'lentitud', 'inmunidad')
        :param velocidad: Velocidad de caída
        """
        self.tipo = tipo
        self.image = pygame.image.load(self.TIPOS_POCIONES[tipo])
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = velocidad

    def update(self):
        """Mueve la poción hacia abajo"""
        self.rect.y += self.velocidad

    def draw(self, screen):
        """Dibuja la poción en la pantalla"""
        screen.blit(self.image, self.rect)

    def esta_fuera_pantalla(self, alto_pantalla):
        """Verifica si la poción está fuera de la pantalla"""
        return self.rect.y > alto_pantalla
    
    @staticmethod
    def crear_aleatoria(x, y, velocidad=5):
        """Crea una poción de tipo aleatorio"""
        tipo = random.choice(list(PocionItem.TIPOS_POCIONES.keys()))
        return PocionItem(x, y, tipo, velocidad)
