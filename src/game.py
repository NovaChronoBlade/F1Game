import pygame
from config import ANCHO, ALTO, FPS, TITULO, COLOR_FONDO, ICON

class Game:
    def __init__(self):
        pygame.init()
        self.icon = pygame.image.load(ICON)
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        pygame.display.set_icon(self.icon)
        pygame.image()
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass  # Update game state here

    def draw(self):
        self.screen.fill(COLOR_FONDO)
        pygame.display.flip()