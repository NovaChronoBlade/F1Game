"""
Controlador de pociones que utiliza el patrón Wrapper/Decorator.
Este módulo gestiona la aplicación de los decoradores de pociones al carro.
"""
from src.models.carro_decorador import (
    VelocidadDecorator, 
    LentitudDecorator, 
    InmunidadDecorator,
    CarroComponent
)


class GestorPociones:
    """Gestor que aplica y remueve decoradores de pociones al carro"""
    
    def __init__(self):
        self.decoradores_activos = []  # Lista de decoradores aplicados
        self.carro_base = None  # Referencia al carro base sin decorar
    
    def aplicar_pocion(self, carro_actual: CarroComponent, tipo_pocion: str) -> CarroComponent:
        """
        Aplica una poción al carro usando el patrón Decorator
        
        :param carro_actual: El carro (posiblemente ya decorado)
        :param tipo_pocion: Tipo de poción ('velocidad', 'lentitud', 'inmunidad')
        :return: El carro decorado con la nueva poción
        """
        # Si es la primera poción, guardamos el carro base
        if self.carro_base is None:
            self.carro_base = carro_actual
        
        # Crear el decorador apropiado
        if tipo_pocion == "velocidad":
            decorador = VelocidadDecorator(carro_actual, boost_velocidad=3)
        elif tipo_pocion == "lentitud":
            decorador = LentitudDecorator(carro_actual, reduccion_velocidad=3)
        elif tipo_pocion == "inmunidad":
            decorador = InmunidadDecorator(carro_actual)
        else:
            return carro_actual
        
        # Registrar el decorador activo
        self.decoradores_activos.append(decorador)
        
        return decorador
    
    def actualizar_decoradores(self, carro_actual: CarroComponent) -> CarroComponent:
        """
        Verifica y remueve decoradores expirados
        
        :param carro_actual: El carro actual (posiblemente decorado)
        :return: El carro con los decoradores activos (sin los expirados)
        """
        # Filtrar decoradores expirados
        decoradores_validos = [d for d in self.decoradores_activos if not d.ha_expirado()]
        
        # Si se removieron decoradores
        if len(decoradores_validos) != len(self.decoradores_activos):
            self.decoradores_activos = decoradores_validos
            
            # Reconstruir la cadena de decoradores
            if len(self.decoradores_activos) == 0:
                # No hay decoradores, retornar el carro base
                return self.carro_base
            else:
                # Aplicar los decoradores restantes en orden
                carro = self.carro_base
                for decorador_tipo in self.decoradores_activos:
                    # Reenvolver el carro con los decoradores que no expiraron
                    if isinstance(decorador_tipo, VelocidadDecorator):
                        carro = VelocidadDecorator(carro, decorador_tipo.boost_velocidad)
                    elif isinstance(decorador_tipo, LentitudDecorator):
                        carro = LentitudDecorator(carro, decorador_tipo.reduccion_velocidad)
                    elif isinstance(decorador_tipo, InmunidadDecorator):
                        carro = InmunidadDecorator(carro)
                return carro
        
        return carro_actual
    
    def limpiar(self):
        """Limpia todos los decoradores y resetea el estado"""
        self.decoradores_activos.clear()
        resultado = self.carro_base
        self.carro_base = None
        return resultado