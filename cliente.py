# En esta clase manejo la informacion de los clientes y sus datos personales
# tambien realizo algunas validaciones para evitar registrar datos incorrectos

import re
from entidades import Entidad
from excepciones import ClienteInvalidoError


class Cliente(Entidad):

    # Este patron lo utilizo para comprobar que el correo tenga un formato valido
    _PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w\.-]+$")

    def __init__(self, identificador: str, nombre: str, email: str, telefono: str):
        # Inicializo la clase principal y guardo el identificador del cliente
        super().__init__(identificador)

        # Asigno los datos del cliente para que pasen por sus respectivas validaciones
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    # Propiedad para consultar y validar el nombre del cliente
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        # Compruebo que el nombre sea texto y tenga minimo tres caracteres
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")

        # Evito que se ingresen numeros en el nombre
        if any(c.isdigit() for c in valor):
            raise ClienteInvalidoError("El nombre no puede contener números.")

        # Guardo el nombre sin espacios al principio ni al final
        self.__nombre = valor.strip()

    # Propiedad para consultar y validar el correo electronico
    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        # Verifico que el correo tenga una estructura correcta
        if not isinstance(valor, str) or not self._PATRON_EMAIL.match(valor):
            raise ClienteInvalidoError(f"Correo electrónico inválido: {valor!r}")

        # Guardo el correo en minusculas para mantener un mismo formato
        self.__email = valor.lower()

    # Propiedad para consultar y validar el telefono
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        # Compruebo que el telefono tenga solamente numeros y diez digitos
        if not isinstance(valor, str) or not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError("El teléfono debe tener exactamente 10 dígitos.")

        self.__telefono = valor

    # Metodo que muestra la informacion principal del cliente
    def describir(self) -> str:
        return f"Cliente[{self.id}] {self.nombre} <{self.email}> Tel: {self.telefono}"