import pygame
from abc import ABC, abstractmethod


class CarroComponent(ABC):
    """Componente base para el patrón Decorator/Wrapper"""
    
    @abstractmethod
    def mover_izquierda(self, limite_izquierdo=0):
        pass
    
    @abstractmethod
    def mover_derecha(self, limite_derecho=800):
        pass
    
    @abstractmethod
    def draw(self, screen):
        pass
    
    @abstractmethod
    def get_velocidad(self):
        pass
    
    @abstractmethod
    def es_inmune(self):
        pass
    
    @abstractmethod
    def get_rect(self):
        pass


class CarroDecorator(CarroComponent):
    """Decorador base que envuelve un CarroComponent"""
    
    def __init__(self, carro_component: CarroComponent):
        self._carro = carro_component
    
    def mover_izquierda(self, limite_izquierdo=0):
        self._carro.mover_izquierda(limite_izquierdo)
    
    def mover_derecha(self, limite_derecho=800):
        self._carro.mover_derecha(limite_derecho)
    
    def draw(self, screen):
        self._carro.draw(screen)
    
    def get_velocidad(self):
        return self._carro.get_velocidad()
    
    def es_inmune(self):
        return self._carro.es_inmune()
    
    def get_rect(self):
        return self._carro.get_rect()


class VelocidadDecorator(CarroDecorator):
    """Wrapper que añade velocidad extra al carro"""
    
    def __init__(self, carro_component: CarroComponent, boost_velocidad: int = 3):
        super().__init__(carro_component)
        self.boost_velocidad = boost_velocidad
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = 5000  # 5 segundos en milisegundos
    
    def get_velocidad(self):
        return self._carro.get_velocidad() + self.boost_velocidad
    
    def mover_izquierda(self, limite_izquierdo=0):
        # Usa la velocidad aumentada
        rect = self.get_rect()
        rect.x -= self.get_velocidad()
        if rect.x < limite_izquierdo:
            rect.x = limite_izquierdo
    
    def mover_derecha(self, limite_derecho=800):
        # Usa la velocidad aumentada
        rect = self.get_rect()
        rect.x += self.get_velocidad()
        if rect.x + rect.width > limite_derecho:
            rect.x = limite_derecho - rect.width
    
    def draw(self, screen):
        # Dibuja el carro con un aura verde (efecto visual)
        self._carro.draw(screen)
        rect = self.get_rect()
        pygame.draw.rect(screen, (0, 255, 0), rect, 3)  # Borde verde
    
    def ha_expirado(self):
        tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_inicio
        return tiempo_transcurrido >= self.duracion


class LentitudDecorator(CarroDecorator):
    """Wrapper que reduce la velocidad del carro"""
    
    def __init__(self, carro_component: CarroComponent, reduccion_velocidad: int = 3):
        super().__init__(carro_component)
        self.reduccion_velocidad = reduccion_velocidad
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = 5000  # 5 segundos en milisegundos
    
    def get_velocidad(self):
        velocidad_reducida = self._carro.get_velocidad() - self.reduccion_velocidad
        return max(2, velocidad_reducida)  # Velocidad mínima de 2
    
    def mover_izquierda(self, limite_izquierdo=0):
        # Usa la velocidad reducida
        rect = self.get_rect()
        rect.x -= self.get_velocidad()
        if rect.x < limite_izquierdo:
            rect.x = limite_izquierdo
    
    def mover_derecha(self, limite_derecho=800):
        # Usa la velocidad reducida
        rect = self.get_rect()
        rect.x += self.get_velocidad()
        if rect.x + rect.width > limite_derecho:
            rect.x = limite_derecho - rect.width
    
    def draw(self, screen):
        # Dibuja el carro con un aura roja (efecto visual)
        self._carro.draw(screen)
        rect = self.get_rect()
        pygame.draw.rect(screen, (255, 0, 0), rect, 3)  # Borde rojo
    
    def ha_expirado(self):
        tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_inicio
        return tiempo_transcurrido >= self.duracion


class InmunidadDecorator(CarroDecorator):
    """Wrapper que hace al carro inmune a las rocas"""
    
    def __init__(self, carro_component: CarroComponent):
        super().__init__(carro_component)
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = 5000  # 5 segundos en milisegundos
    
    def es_inmune(self):
        return True
    
    def draw(self, screen):
        # Dibuja el carro con un aura azul brillante (efecto visual)
        self._carro.draw(screen)
        rect = self.get_rect()
        pygame.draw.rect(screen, (0, 150, 255), rect, 3)  # Borde azul
        # Efecto de brillo
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((0, 150, 255, 50))  # Azul semi-transparente
        screen.blit(s, (rect.x, rect.y))
    
    def ha_expirado(self):
        tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_inicio
        return tiempo_transcurrido >= self.duracion
