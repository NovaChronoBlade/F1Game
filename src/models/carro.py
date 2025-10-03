from abc import abstractmethod, ABC
import pygame
from src.models.carro_decorador import CarroComponent


class Carro(ABC):
    """Clase base abstracta que define el comportamiento de un carro"""
    
    def __init__(self, velocidad: int, inmunidad: bool = False):
        self.velocidad = velocidad
        self.inmunidad = inmunidad
        super().__init__()

    @abstractmethod
    def correr(self):
        """Método abstracto que define el comportamiento de correr del carro"""
        pass


class CarroJugador(CarroComponent, Carro):
    """
    Carro base del jugador - Componente concreto del patrón Decorator.
    Hereda de CarroComponent (para el patrón Decorator) y de Carro (modelo base).
    """
    
    def __init__(self, x, y, imagen_path, velocidad_base: int = 8):
        """
        Carro del jugador
        :param x: Posición inicial en x
        :param y: Posición inicial en y
        :param imagen_path: Ruta a la imagen del carro
        :param velocidad_base: Velocidad base del carro
        """
        # Inicializar Carro con velocidad e inmunidad
        Carro.__init__(self, velocidad=velocidad_base, inmunidad=False)
        
        # Configuración visual del carro
        self.image = pygame.image.load(imagen_path)
        self.image = pygame.transform.scale(self.image, (60, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def correr(self):
        """Implementación del método abstracto correr"""
        # El carro se mueve automáticamente en el juego
        # Este método puede extenderse para animaciones o comportamientos especiales
        pass

    def mover_izquierda(self, limite_izquierdo=0):
        """Mueve el carro a la izquierda"""
        self.rect.x -= self.get_velocidad()
        if self.rect.x < limite_izquierdo:
            self.rect.x = limite_izquierdo

    def mover_derecha(self, limite_derecho=800):
        """Mueve el carro a la derecha"""
        self.rect.x += self.get_velocidad()
        if self.rect.x + self.rect.width > limite_derecho:
            self.rect.x = limite_derecho - self.rect.width

    def draw(self, screen):
        """Dibuja el carro en la pantalla"""
        screen.blit(self.image, self.rect)
    
    def get_velocidad(self):
        """Retorna la velocidad del carro (del modelo Carro)"""
        return self.velocidad
    
    def es_inmune(self):
        """Retorna si el carro es inmune (del modelo Carro)"""
        return self.inmunidad
    
    def get_rect(self):
        """Retorna el rectángulo del carro"""
        return self.rect