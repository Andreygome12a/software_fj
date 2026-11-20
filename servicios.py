# En este archivo manejo los servicios que ofrece el programa
# como las reservas de salas, el alquiler de equipos y las asesorias

from abc import abstractmethod
from entidades import Entidad
from excepciones import ParametroInvalidoError, CalculoError, ServicioNoDisponibleError


class Servicio(Entidad):
    # Defino el porcentaje de IVA que se utiliza para calcular los costos
    IVA = 0.19

    def __init__(self, identificador: str, nombre: str, tarifa_hora: float):
        super().__init__(identificador)

        # Verifico que el nombre del servicio no este vacio
        if not isinstance(nombre, str) or not nombre.strip():
            raise ParametroInvalidoError("El servicio requiere un nombre.")

        # Compruebo que la tarifa por hora sea un numero positivo
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ParametroInvalidoError("La tarifa por hora debe ser un número positivo.")

        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    def cambiar_disponibilidad(self, estado: bool):
        # Cambio la disponibilidad del servicio segun el estado recibido
        self._disponible = bool(estado)

    def verificar_disponibilidad(self):
        # Compruebo que el servicio se encuentre disponible
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._nombre}' no está disponible.")

    @abstractmethod
    def validar_parametros(self, duracion: float) -> None:
        # Este metodo permite validar la duracion de cada tipo de servicio
        pass

    @abstractmethod
    def costo_base(self, duracion: float) -> float:
        # Cada servicio tiene su propia forma de calcular el costo
        pass

    def calcular_costo(self, duracion: float, impuesto: float = None, descuento: float = 0.0) -> float:
        # Este metodo calcula el costo teniendo en cuenta los impuestos y descuentos

        # Primero verifico que la duracion sea valida
        self.validar_parametros(duracion)

        # Si no se indica un impuesto utilizo el IVA definido anteriormente
        impuesto = self.IVA if impuesto is None else impuesto

        # Compruebo que los porcentajes ingresados esten dentro del rango permitido
        if not (0 <= impuesto <= 1) or not (0 <= descuento < 1):
            raise CalculoError("Impuesto o descuento fuera de rango (0-1).")

        base = self.costo_base(duracion)

        # Aplico el descuento y despues agrego el impuesto al valor restante
        total = base * (1 - descuento) * (1 + impuesto)

        # Verifico que el resultado del calculo no sea negativo
        if total < 0:
            raise CalculoError("El cálculo produjo un costo negativo.")
        return round(total, 2)

    def calcular_costo_con_descuento_fijo(self, duracion: float, monto: float) -> float:
        # Calculo el costo del servicio restando un valor fijo
        total = self.calcular_costo(duracion) - monto
        if total < 0:
            raise CalculoError("El descuento fijo supera el costo del servicio.")
        return round(total, 2)


class ReservaSala(Servicio):
    # Esta clase maneja las reservas de salas y su capacidad

    def __init__(self, identificador, nombre, tarifa_hora, capacidad: int):
        super().__init__(identificador, nombre, tarifa_hora)

        # Verifico que la capacidad de la sala sea un numero entero positivo
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ParametroInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, duracion):
        # Compruebo que la reserva de la sala no supere las 8 horas
        if not isinstance(duracion, (int, float)) or not (0 < duracion <= 8):
            raise ParametroInvalidoError("Una sala se reserva entre 0 y 8 horas.")

    def costo_base(self, duracion):
        # Calculo el costo de la sala segun las horas reservadas
        return self._tarifa_hora * duracion

    def describir(self):
        return f"Sala '{self._nombre}' (capacidad {self._capacidad}) - ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    # Esta clase maneja el alquiler de los equipos

    SEGURO = 15000

    def __init__(self, identificador, nombre, tarifa_hora, tipo_equipo: str):
        super().__init__(identificador, nombre, tarifa_hora)

        # Compruebo que se indique el tipo de equipo que se va a alquilar
        if not tipo_equipo or not tipo_equipo.strip():
            raise ParametroInvalidoError("Debe indicar el tipo de equipo.")
        self._tipo_equipo = tipo_equipo

    def validar_parametros(self, duracion):
        # Verifico que el alquiler no supere las 72 horas
        if not isinstance(duracion, (int, float)) or not (0 < duracion <= 72):
            raise ParametroInvalidoError("Un equipo se alquila entre 0 y 72 horas.")

    def costo_base(self, duracion):
        # Calculo el valor del alquiler y le sumo el seguro
        return self._tarifa_hora * duracion + self.SEGURO

    def describir(self):
        return f"Equipo '{self._nombre}' ({self._tipo_equipo}) - ${self._tarifa_hora:,.0f}/h + seguro"


class Asesoria(Servicio):
    # Esta clase maneja las asesorias y tiene en cuenta si el asesor es experto

    def __init__(self, identificador, nombre, tarifa_hora, especialidad: str, experto: bool = False):
        super().__init__(identificador, nombre, tarifa_hora)

        # Verifico que la asesoria tenga una especialidad
        if not especialidad or not especialidad.strip():
            raise ParametroInvalidoError("La asesoría requiere una especialidad.")
        self._especialidad = especialidad
        self._experto = experto

    def validar_parametros(self, duracion):
        # Compruebo que la duracion este entre media hora y seis horas
        if not isinstance(duracion, (int, float)) or not (0.5 <= duracion <= 6):
            raise ParametroInvalidoError("Una asesoría dura entre 0.5 y 6 horas.")

    def costo_base(self, duracion):
        # Si el asesor es experto se aplica un recargo del 25 por ciento
        recargo = 1.25 if self._experto else 1.0
        return self._tarifa_hora * duracion * recargo

    def describir(self):
        nivel = "experto" if self._experto else "estándar"
        return f"Asesoría '{self._nombre}' en {self._especialidad} (nivel {nivel}) - ${self._tarifa_hora:,.0f}/h"