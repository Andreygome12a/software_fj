# En este archivo configuro el registro de los eventos y errores del programa
# para guardar la informacion en un archivo de log

import logging
import os

# Creo la ruta donde se va a guardar el archivo de registro
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs_software_fj.log")


def obtener_logger() -> logging.Logger:
    # Obtengo el registro con el nombre del programa
    logger = logging.getLogger("SoftwareFJ")

    # Compruebo si ya tiene una configuracion para evitar registros repetidos
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(RUTA_LOG, encoding="utf-8")

        # Defino el formato en el que se guardan los registros
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))
        logger.addHandler(handler)
    return logger


# Creo el registro para poder utilizarlo desde los demas archivos
log = obtener_logger()