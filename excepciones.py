# En este archivo creo las excepciones que utilizo en el programa
# para identificar mejor los diferentes errores que se pueden presentar


class SoftwareFJError(Exception):
    # Esta es la excepcion principal de la que heredan las demas
    pass


class ClienteInvalidoError(SoftwareFJError):
    # Este error se utiliza cuando los datos del cliente no son correctos
    pass


class ParametroInvalidoError(SoftwareFJError):
    # Lo utilizo cuando algun dato ingresado no cumple con lo solicitado
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    # Se presenta cuando se intenta utilizar un servicio que no esta disponible
    pass


class ReservaError(SoftwareFJError):
    # Este error se utiliza cuando ocurre algun problema con una reserva
    pass


class CalculoError(SoftwareFJError):
    # Lo utilizo cuando se presenta un problema al realizar algun calculo
    pass