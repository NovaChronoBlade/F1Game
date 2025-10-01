import sys
import pygame
from src.menu import Menu
from src.game import Game
from config import ANCHO, ALTO, TITULO

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(TITULO)

# Mostrar el menú (activar show_hitbox=True para depuración de hitboxes)
menu = Menu(pantalla, show_hitbox=True)
accion = menu.mostrar()

# Si el usuario hace clic en "Jugar", inicia el juego
if accion == "jugar":
    juego = Game()
    juego.run()

if accion == "salir":
    pygame.quit()
    sys.exit()
