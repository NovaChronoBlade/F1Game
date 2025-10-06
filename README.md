#andres felipe lopez martinez - 20241020052 #juan camilo mosquera palomino - 20241020120
# F1Game

Proyecto desarrollado en Python para ejecución en ambiente local.

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Recomendado: [virtualenv](https://virtualenv.pypa.io/) para crear entornos aislados

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/NovaChronoBlade/F1Game.git
   cd F1Game
   ```

2. (Opcional pero recomendado) Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   venv\Scripts\activate     # En Windows
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   > Si no existe `requirements.txt`, instala manualmente los paquetes necesarios según el código fuente.

## Ejecución

Busca el archivo principal (por ejemplo, `main.py`) y ejecútalo:
```bash
python main.py
```
> Si el nombre del archivo principal es distinto, ajusta el comando según corresponda.

## Notas

- Si el proyecto depende de variables de entorno, configura un archivo `.env` o exporta las variables necesarias antes de ejecutar.
- Consulta el código fuente para detalles específicos sobre configuración, uso de puertos, rutas de archivos, etc.

---
