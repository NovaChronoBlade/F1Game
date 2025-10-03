import sys
import pygame
from src.menu import Menu
from src.game import Game
from config import ANCHO, ALTO, TITULO, ICON

# Inicializar pygame y configurar la pantalla primero
pygame.init()
pygame.display.init()  # Asegurar que display esté inicializado
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(TITULO)

# Configurar el ícono de la ventana
try:
    icono = pygame.image.load(ICON)
    pygame.display.set_icon(icono)
except pygame.error as e:
    print(f"No se pudo cargar el ícono: {e}")

# Loop principal para mantener el juego activo
game_running = True
while game_running:
    # Mostrar el menú
    menu = Menu(pantalla, show_hitbox=False)
    accion = menu.mostrar()

    # Si el usuario hace clic en "Jugar", inicia el juego
    if accion == "jugar":
        juego = Game()
        juego.run()
        # Después de que termine el juego, vuelve al menú
        continue

    if accion == "salir":
        game_running = False

pygame.quit()
sys.exit()
