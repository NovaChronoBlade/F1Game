import pygame
import random


class Roca:
    def __init__(self, x, y, imagen_path, velocidad=5):
        """
        Roca obstáculo
        :param x: Posición inicial en x
        :param y: Posición inicial en y
        :param imagen_path: Ruta a la imagen de la roca
        :param velocidad: Velocidad de caída
        """
        self.image = pygame.image.load(imagen_path)
        self.image = pygame.transform.scale(self.image, (100, 100))  # Redimensionar la roca
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = velocidad

    def update(self):
        """Mueve la roca hacia abajo"""
        self.rect.y += self.velocidad

    def draw(self, screen):
        """Dibuja la roca en la pantalla"""
        screen.blit(self.image, self.rect)

    def esta_fuera_pantalla(self, alto_pantalla):
        """Verifica si la roca está fuera de la pantalla"""
        return self.rect.y > alto_pantalla
