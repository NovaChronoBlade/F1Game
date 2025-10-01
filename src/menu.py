import sys
import pygame
from config import ANCHO, ALTO, BOTON_ANCHO, BOTON_ALTO


class Menu:
    def __init__(self, pantalla, show_hitbox: bool = False):
        self.pantalla = pantalla
        self.fondo = pygame.image.load("assets/images/bg_principal.png")
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))

        # Botones
        self.boton_jugar = pygame.image.load("assets/images/jugar_boton.png").convert_alpha()
        self.boton_salir = pygame.image.load("assets/images/salir_boton.png").convert_alpha()

        # Escalar botones al tamaño definido en config
        self.boton_jugar = pygame.transform.scale(self.boton_jugar, (BOTON_ANCHO, BOTON_ALTO))
        self.boton_salir = pygame.transform.scale(self.boton_salir, (BOTON_ANCHO, BOTON_ALTO))

        # Rectángulos para posición
        self.boton_jugar_rect = self.boton_jugar.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        self.boton_salir_rect = self.boton_salir.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))

        # Máscaras (detectan solo pixeles no transparentes)
        self.jugar_mask = pygame.mask.from_surface(self.boton_jugar)
        self.salir_mask = pygame.mask.from_surface(self.boton_salir)

        # Mostrar hitboxes (para depuración)
        self.show_hitbox = show_hitbox

        # Inicializar Musica
        pygame.mixer.init()
        try:
            pygame.mixer.music.load("assets/sounds/menu.mp3")
            pygame.mixer.music.set_volume(0.5)  # Volumen al 50%
        except pygame.error as e:
            print(f"No se pudo cargar la música: {e}")

    def mostrar(self):
        # Reproducir música de fondo en loop
        try:
            pygame.mixer.music.play(-1)  # -1 = loop infinito
        except pygame.error:
            pass  # Continuar sin música si hay error
            
        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.mixer.music.stop()  # Detener música al cerrar
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # Verificar colisión con "Jugar"
                    if self.boton_jugar_rect.collidepoint(evento.pos):
                        x, y = evento.pos[0] - self.boton_jugar_rect.x, evento.pos[1] - self.boton_jugar_rect.y
                        if self.jugar_mask.get_at((x, y)):
                            pygame.mixer.music.stop()  # Detener música al salir del menú
                            return "jugar"

                    # Verificar colisión con "Salir"
                    if self.boton_salir_rect.collidepoint(evento.pos):
                        x, y = evento.pos[0] - self.boton_salir_rect.x, evento.pos[1] - self.boton_salir_rect.y
                        if self.salir_mask.get_at((x, y)):
                            pygame.mixer.music.stop()  # Detener música al salir
                            pygame.quit()
                            sys.exit()

            # Dibujar fondo y botones
            self.pantalla.blit(self.fondo, (0, 0))
            self.pantalla.blit(self.boton_jugar, self.boton_jugar_rect)
            self.pantalla.blit(self.boton_salir, self.boton_salir_rect)

            # Dibujar hitboxes (debug)


            pygame.display.flip()
