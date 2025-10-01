import pygame
from config import ANCHO, ALTO, FPS

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Pista Infinita")
        self.clock = pygame.time.Clock()
        self.running = True

        # Cargar imagen de la pista
        self.track = pygame.image.load("assets/pista.png")
        self.track_width = self.track.get_width()
        self.track_height = self.track.get_height()

        # Inicializar la posición de la pista
        self.track_x = 0
        self.track_y = ALTO - self.track_height  # Poner la pista en el fondo de la pantalla
        
    def run(self):
        while self.running:
            self.clock.tick(FPS)  # Controlar los FPS
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Desplazar la pista hacia la izquierda
        self.track_x -= 5  # Ajusta esta velocidad según lo desees

        # Cuando la pista se haya desplazado completamente fuera de la pantalla, la volvemos a colocar
        if self.track_x <= -self.track_width:
            self.track_x = 0

    def draw(self):
        # Rellenar el fondo con el color de fondo
        self.screen.fill((0, 0, 0))

        # Dibujar la pista infinita en la pantalla
        self.screen.blit(self.track, (self.track_x, self.track_y))
        self.screen.blit(self.track, (self.track_x + self.track_width, self.track_y))

        # Actualizar pantalla
        pygame.display.flip()
