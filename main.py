# En este archivo ejecuto el programa y realizo varias pruebas
# para comprobar que las operaciones funcionen correctamente
# tambien verifico que los errores no detengan todo el programa

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
import logging
from excepciones import SoftwareFJError, ParametroInvalidoError
from logger import log, RUTA_LOG

# Estas listas guardan los datos mientras se ejecuta el programa
clientes, servicios, reservas = [], [], []


def ejecutar(num: int, titulo: str, accion):
    # Esta funcion ejecuta cada operacion y controla los posibles errores
    print(f"\n[{num:02d}] {titulo}")
    try:
        resultado = accion()
    except SoftwareFJError as e:
        # Capturo los errores que fueron definidos para el programa
        # y muestro el motivo por el que ocurrio el problema
        causa = f" (causa: {e.__cause__})" if e.__cause__ else ""
        print(f"     ERROR CONTROLADO: {e}{causa}")
        log.error("Operación %02d '%s' falló: %s%s", num, titulo, e, causa)
    except Exception as e:
        # Capturo otros errores que puedan aparecer durante la ejecucion
        # para evitar que el programa se cierre inesperadamente
        print(f"     ERROR INESPERADO: {type(e).__name__}: {e}")
        log.critical("Operación %02d error inesperado: %r", num, e)
    else:
        # Si la operacion sale bien muestro el resultado y lo guardo en el log
        print(f"     OK -> {resultado}")
        log.info("Operación %02d '%s' exitosa", num, titulo)
    finally:
        # Registro el final de cada operacion
        log.info("Fin operación %02d", num)


def registrar_cliente(*datos):
    # Creo el cliente con los datos recibidos y lo agrego a la lista
    c = Cliente(*datos)
    clientes.append(c)
    return c


def registrar_servicio(clase, *datos):
    # Creo el servicio dependiendo de la clase que se reciba
    s = clase(*datos)
    servicios.append(s)
    return s


def crear_reserva(cliente, servicio, horas, descuento=0.0):
    # Creo un identificador diferente para cada reserva
    r = Reserva(f"R{len(reservas) + 1:03d}", cliente, servicio, horas)

    # Agrego la reserva a la lista antes de procesarla
    reservas.append(r)
    r.procesar(descuento)
    return r


def convertir_duracion(texto):
    # Convierto la duracion recibida como texto a un numero
    try:
        horas = float(texto)
    except (ValueError, TypeError) as e:
        # Si el valor no se puede convertir muestro el error correspondiente
        raise ParametroInvalidoError(f"La duración {texto!r} no es un número válido.") from e
    else:
        # Compruebo que la duracion ingresada sea mayor que cero
        if horas <= 0:
            raise ParametroInvalidoError("La duración debe ser mayor que cero.")
        return horas


def main():
    log.info("===== Inicio de la simulación =====")

    # Registro algunos clientes para probar los datos validos e invalidos
    ejecutar(1, "Registrar cliente válido",
             lambda: registrar_cliente("C1", "Ana Pérez", "ana@correo.com", "3001234567"))
    ejecutar(2, "Registrar cliente con correo inválido",
             lambda: registrar_cliente("C2", "Luis Gómez", "luis#correo", "3109876543"))
    ejecutar(3, "Registrar cliente con teléfono inválido",
             lambda: registrar_cliente("C3", "Marta Ruiz", "marta@correo.com", "123"))
    ejecutar(4, "Registrar cliente válido (2)",
             lambda: registrar_cliente("C4", "Carlos Díaz", "carlos@correo.com", "3201112233"))

    # Creo servicios para probar su funcionamiento y las validaciones
    ejecutar(5, "Crear sala válida",
             lambda: registrar_servicio(ReservaSala, "S1", "Sala Júpiter", 50000, 12))
    ejecutar(6, "Crear equipo con tarifa negativa",
             lambda: registrar_servicio(AlquilerEquipo, "S2", "Portátil", -100, "Computador"))

    # En esta operacion creo un equipo y una asesoria
    ejecutar(7, "Crear equipo y asesoría válidos",
             lambda: (registrar_servicio(AlquilerEquipo, "S3", "Video Beam", 20000, "Proyector"),
                      registrar_servicio(Asesoria, "S4", "Asesoría Python", 80000, "Programación", True))[1])

    # Realizo varias pruebas para comprobar el funcionamiento de las reservas
    ejecutar(8, "Reserva exitosa de sala (3 h, 10 % descuento)",
             lambda: crear_reserva(clientes[0], servicios[0], 3, 0.10))
    ejecutar(9, "Reserva con duración inválida (10 h en sala)",
             lambda: crear_reserva(clientes[0], servicios[0], 10))

    # Desactivo el servicio para comprobar que no se pueda reservar
    ejecutar(10, "Reserva de servicio no disponible",
             lambda: (servicios[1].cambiar_disponibilidad(False), crear_reserva(clientes[1], servicios[1], 5))[1])
    ejecutar(11, "Reserva exitosa de asesoría experta (2 h)",
             lambda: crear_reserva(clientes[1], servicios[2], 2))

    # Intento cancelar la misma reserva dos veces para probar la validacion
    ejecutar(12, "Cancelar dos veces la misma reserva",
             lambda: (reservas[0].cancelar(), reservas[0].cancelar()))
    ejecutar(13, "Descuento inválido (150 %)",
             lambda: crear_reserva(clientes[0], servicios[0], 2, 1.5))

    # Pruebo la conversion de duraciones ingresadas como texto
    ejecutar(14, "Reserva con duración escrita como texto no numérico ('tres')",
             lambda: crear_reserva(clientes[0], servicios[0], convertir_duracion("tres")))
    ejecutar(15, "Reserva válida con duración como texto ('2.5')",
             lambda: crear_reserva(clientes[1], servicios[0], convertir_duracion("2.5")))

    # Muestro un resumen con los datos que se guardaron durante las pruebas
    print("\n=== Resumen ===")
    print(f"Clientes: {len(clientes)} | Servicios: {len(servicios)} | Reservas: {len(reservas)}")
    for s in servicios:
        print(" -", s.describir())
    for r in reservas:
        print(" -", r.describir())
    print(f"\nLog generado en: {RUTA_LOG}")
    log.info("===== Fin de la simulación =====")


# Ejecuto el programa solamente cuando abro este archivo directamente
if __name__ == "__main__":
    # Me aseguro de cerrar los registros cuando termina la ejecucion
    try:
        main()
    finally:
        logging.shutdown()
        print("Programa finalizado. Logs cerrados correctamente.")