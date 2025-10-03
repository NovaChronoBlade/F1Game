import pygame
import random
from config import ANCHO, ALTO, FPS, TITULO, COLOR_FONDO, ICON
from src.models.carro import CarroJugador
from src.models.roca import Roca
from src.models.pocion_item import PocionItem
from src.models.carro_decorador import VelocidadDecorator, LentitudDecorator, InmunidadDecorator

class Game:
    def __init__(self):
        # No inicializar pygame de nuevo, ya está inicializado desde main.py
        self.screen = pygame.display.get_surface()  # Obtener la superficie existente
        if self.screen is None:
            self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.running = True

        # Cargar imagen de la pista
        self.track = pygame.image.load("assets/images/pista.png")
        self.track_width = self.track.get_width()
        self.track_height = self.track.get_height()

        # Inicializar la posición de la pista
        self.track_x = 0
        self.track_y = ALTO - self.track_height  # Poner la pista en el fondo de la pantalla

        # Definir los límites de la pista (márgenes laterales)
        self.limite_izquierdo = 150  # Margen izquierdo de la pista
        self.limite_derecho = 700    # Margen derecho de la pista

        # Crear el carro base del jugador
        self.carro_base = CarroJugador(
            x=ANCHO // 2 - 30,  # Centrar el carro horizontalmente
            y=ALTO - 150,  # Posición cerca del fondo de la pantalla
            imagen_path="assets/images/f1.png"
        )
        # El carro actual puede ser el base o estar envuelto por decoradores
        self.player_car = self.carro_base
        
        # Lista de decoradores activos (patrón Wrapper)
        self.decoradores_activos = []

        # Lista de rocas y configuración
        self.rocas = []
        self.roca_timer = 0
        self.roca_spawn_interval = 60  # Frames entre cada generación de roca
        self.velocidad_rocas = 7  # Velocidad de caída de las rocas

        # Lista de pociones y configuración
        self.pociones_items = []
        self.pocion_timer = 0
        self.pocion_spawn_interval = 180  # Frames entre cada generación de poción (más espaciadas)
        self.velocidad_pociones = 5  # Velocidad de caída de las pociones

        # Estado del juego
        self.game_over = False
        self.return_to_menu = False

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            
            if not self.game_over:
                self.update()
            
            self.draw()
            
            # Si el jugador perdió y presiona una tecla, volver al menú
            if self.return_to_menu:
                self.running = False
        
        # NO cerrar pygame aquí, solo salir del loop

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Si hay game over, cualquier tecla vuelve al menú
            if event.type == pygame.KEYDOWN and self.game_over:
                self.return_to_menu = True
        
        # Manejar el movimiento del carro con las teclas solo si no hay game over
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player_car.mover_izquierda(limite_izquierdo=self.limite_izquierdo)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player_car.mover_derecha(limite_derecho=self.limite_derecho)

    def update(self):
        # Desplazar la pista hacia abajo
        self.track_y += 10  # Velocidad hacia abajo

        # Cuando la pista se haya desplazado completamente fuera de la pantalla, la volvemos a colocar arriba justo detrás
        if self.track_y >= self.track_height:
            self.track_y = 0

        # Generar rocas aleatorias
        self.roca_timer += 1
        if self.roca_timer >= self.roca_spawn_interval:
            self.generar_roca()
            self.roca_timer = 0

        # Actualizar rocas
        for roca in self.rocas[:]:
            roca.update()
            
            # Eliminar rocas que están fuera de la pantalla
            if roca.esta_fuera_pantalla(ALTO):
                self.rocas.remove(roca)
            
            # Verificar colisión con el jugador (solo si no tiene inmunidad)
            if roca.rect.colliderect(self.player_car.get_rect()) and not self.player_car.es_inmune():
                self.game_over = True

        # Generar pociones aleatorias
        self.pocion_timer += 1
        if self.pocion_timer >= self.pocion_spawn_interval:
            self.generar_pocion()
            self.pocion_timer = 0

        # Actualizar pociones
        for pocion_item in self.pociones_items[:]:
            pocion_item.update()
            
            # Eliminar pociones que están fuera de la pantalla
            if pocion_item.esta_fuera_pantalla(ALTO):
                self.pociones_items.remove(pocion_item)
            
            # Verificar colisión con el jugador
            if pocion_item.rect.colliderect(self.player_car.get_rect()):
                self.aplicar_pocion(pocion_item.tipo)
                self.pociones_items.remove(pocion_item)

        # Actualizar decoradores activos y eliminar los expirados (Patrón Wrapper)
        self.actualizar_decoradores()

    def generar_roca(self):
        """Genera una roca en una posición aleatoria dentro de la pista"""
        x = random.randint(self.limite_izquierdo, self.limite_derecho - 100)
        y = -50  # Empezar arriba de la pantalla
        nueva_roca = Roca(x, y, "assets/images/roca.png", self.velocidad_rocas)
        self.rocas.append(nueva_roca)

    def generar_pocion(self):
        """Genera una poción en una posición aleatoria dentro de la pista"""
        x = random.randint(self.limite_izquierdo, self.limite_derecho - 50)
        y = -50  # Empezar arriba de la pantalla
        nueva_pocion = PocionItem.crear_aleatoria(x, y, self.velocidad_pociones)
        self.pociones_items.append(nueva_pocion)

    def aplicar_pocion(self, tipo):
        """Aplica el efecto de una poción al carro usando el patrón Wrapper/Decorator"""
        if tipo == "velocidad":
            # Envolver el carro actual con el decorador de velocidad
            decorador = VelocidadDecorator(self.player_car)
            self.player_car = decorador
            self.decoradores_activos.append(decorador)
        elif tipo == "lentitud":
            # Envolver el carro actual con el decorador de lentitud
            decorador = LentitudDecorator(self.player_car)
            self.player_car = decorador
            self.decoradores_activos.append(decorador)
        elif tipo == "inmunidad":
            # Envolver el carro actual con el decorador de inmunidad
            decorador = InmunidadDecorator(self.player_car)
            self.player_car = decorador
            self.decoradores_activos.append(decorador)
    
    def actualizar_decoradores(self):
        """Actualiza y elimina los decoradores expirados (Patrón Wrapper)"""
        for decorador in self.decoradores_activos[:]:
            if hasattr(decorador, 'ha_expirado') and decorador.ha_expirado():
                self.decoradores_activos.remove(decorador)
        
        # Reconstruir la cadena de decoradores sin los expirados
        if not self.decoradores_activos:
            # Si no hay decoradores activos, usar el carro base
            self.player_car = self.carro_base
        else:
            # Reconstruir la cadena desde el carro base
            self.player_car = self.carro_base
            for decorador_activo in self.decoradores_activos:
                # Crear un nuevo decorador con el carro actual
                if isinstance(decorador_activo, VelocidadDecorator):
                    self.player_car = VelocidadDecorator(self.player_car)
                    self.player_car.tiempo_inicio = decorador_activo.tiempo_inicio
                elif isinstance(decorador_activo, LentitudDecorator):
                    self.player_car = LentitudDecorator(self.player_car)
                    self.player_car.tiempo_inicio = decorador_activo.tiempo_inicio
                elif isinstance(decorador_activo, InmunidadDecorator):
                    self.player_car = InmunidadDecorator(self.player_car)
                    self.player_car.tiempo_inicio = decorador_activo.tiempo_inicio

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Dibuja dos pistas para cubrir la pantalla sin huecos
        self.screen.blit(self.track, (0, self.track_y - self.track_height))
        self.screen.blit(self.track, (0, self.track_y))

        # Dibujar las rocas
        for roca in self.rocas:
            roca.draw(self.screen)

        # Dibujar las pociones
        for pocion in self.pociones_items:
            pocion.draw(self.screen)

        # Dibujar el carro del jugador
        self.player_car.draw(self.screen)

        # Dibujar efectos activos en la parte superior
        self.mostrar_efectos_activos()

        # Si hay game over, mostrar mensaje
        if self.game_over:
            self.mostrar_game_over()

        pygame.display.flip()

    def mostrar_efectos_activos(self):
        """Muestra los efectos activos en la parte superior de la pantalla (Patrón Wrapper)"""
        if not self.decoradores_activos:
            return
        
        x_offset = 10
        y_offset = 10
        icon_size = 40
        
        for i, decorador in enumerate(self.decoradores_activos):
            # Determinar el tipo de decorador y cargar su ícono
            try:
                if isinstance(decorador, VelocidadDecorator):
                    icono_path = "assets/images/pocion_velocidad.png"
                    nombre = "Velocidad"
                elif isinstance(decorador, LentitudDecorator):
                    icono_path = "assets/images/pocion_lentitud.png"
                    nombre = "Lentitud"
                elif isinstance(decorador, InmunidadDecorator):
                    icono_path = "assets/images/pocion_inmunidad.png"
                    nombre = "Inmunidad"
                else:
                    continue
                
                # Cargar y escalar el ícono
                icono = pygame.image.load(icono_path)
                icono = pygame.transform.scale(icono, (icon_size, icon_size))
                self.screen.blit(icono, (x_offset, y_offset))
                
                # Calcular tiempo restante
                tiempo_transcurrido = (pygame.time.get_ticks() - decorador.tiempo_inicio) / 1000
                tiempo_restante = max(0, decorador.duracion / 1000 - tiempo_transcurrido)
                
                # Mostrar nombre y tiempo restante
                font = pygame.font.Font(None, 24)
                texto = font.render(f"{nombre}: {tiempo_restante:.1f}s", True, (255, 255, 255))
                self.screen.blit(texto, (x_offset + icon_size + 10, y_offset + 10))
                
                y_offset += icon_size + 10
            except Exception as e:
                pass

    def mostrar_game_over(self):
        """Muestra la pantalla de Game Over"""
        # Crear superficie semi-transparente
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Texto "GAME OVER"
        font_grande = pygame.font.Font(None, 100)
        texto_game_over = font_grande.render("¡PERDISTE!", True, (255, 0, 0))
        rect_game_over = texto_game_over.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        self.screen.blit(texto_game_over, rect_game_over)

        # Texto secundario
        font_pequena = pygame.font.Font(None, 40)
        texto_continuar = font_pequena.render("Presiona cualquier tecla para volver al menú", True, (255, 255, 255))
        rect_continuar = texto_continuar.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
        self.screen.blit(texto_continuar, rect_continuar)



