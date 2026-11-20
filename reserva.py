# En esta clase manejo las reservas y relaciono los clientes con los servicios
# tambien controlo el estado de cada reserva y el calculo de su costo

from entidades import Entidad
from cliente import Cliente
from servicios import Servicio
from excepciones import ReservaError, SoftwareFJError, ParametroInvalidoError
from logger import log


class Reserva(Entidad):
    # Defino los estados que puede tener una reserva
    PENDIENTE, CONFIRMADA, CANCELADA = "PENDIENTE", "CONFIRMADA", "CANCELADA"

    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, duracion: float):
        super().__init__(identificador)

        # Verifico que los datos recibidos sean un cliente y un servicio
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ParametroInvalidoError("La reserva requiere un cliente y un servicio válidos.")

        # Compruebo que la duracion sea valida para el servicio seleccionado
        servicio.validar_parametros(duracion)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = self.PENDIENTE
        self._costo = None

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self):
        # Solo permito confirmar reservas que esten pendientes
        if self._estado != self.PENDIENTE:
            raise ReservaError(f"No se puede confirmar una reserva en estado {self._estado}.")

        # Verifico que el servicio todavia este disponible
        self._servicio.verificar_disponibilidad()
        self._estado = self.CONFIRMADA

    def cancelar(self):
        # Compruebo que la reserva no este cancelada anteriormente
        if self._estado == self.CANCELADA:
            raise ReservaError("La reserva ya estaba cancelada.")
        self._estado = self.CANCELADA

    def procesar(self, descuento: float = 0.0) -> bool:
        # Este metodo se encarga de confirmar la reserva y calcular su costo
        try:
            # Confirmo la reserva y calculo el valor del servicio
            self.confirmar()
            self._costo = self._servicio.calcular_costo(self._duracion, descuento=descuento)
        except SoftwareFJError as e:
            # Si ocurre un error lo guardo en el registro
            log.error("Reserva %s no procesada: %s", self.id, e)

            # Si la reserva ya estaba confirmada la dejo nuevamente pendiente
            if self._estado == self.CONFIRMADA:
                self._estado = self.PENDIENTE

            # Lanzo el error de reserva indicando cual fue el problema
            raise ReservaError(f"Fallo al procesar la reserva {self.id}") from e
        else:
            # Si todo sale bien guardo el costo y confirmo que el proceso termino correctamente
            log.info("Reserva %s procesada. Costo total: $%s", self.id, f"{self._costo:,.2f}")
            return True
        finally:
            # Registro el estado en el que termino el intento de procesamiento
            log.info("Intento de procesamiento de reserva %s finalizado (estado=%s)", self.id, self._estado)

    def describir(self):
        # Muestro el costo si ya fue calculado o indico que todavia no esta disponible
        costo = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (f"Reserva[{self.id}] {self._cliente.nombre} -> {self._servicio.nombre} "
                f"{self._duracion}h | {self._estado} | {costo}")