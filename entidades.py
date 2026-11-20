# En esta clase defino una entidad general que sirve como base para otras clases
# como Cliente, Servicio y Reserva

from abc import ABC, abstractmethod


class Entidad(ABC):
    # Esta clase sirve como base y no se puede utilizar directamente para crear objetos

    def __init__(self, identificador: str):
        # Guardo el identificador de cada entidad
        self._id = identificador

    @property
    def id(self) -> str:
        # Permito consultar el identificador
        return self._id

    @abstractmethod
    def describir(self) -> str:
        # Este metodo debe ser desarrollado por las clases que hereden de Entidad
        pass

    def __str__(self) -> str:
        # Utilizo este metodo para mostrar la descripcion cuando se imprime un objeto
        return self.describir()