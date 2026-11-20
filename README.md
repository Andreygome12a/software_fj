# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

**Curso:** Programación (213023) – UNAD · **Fase 4** – Componente práctico
**Lenguaje:** Python 3.8 o superior (no requiere librerías externas)

Aplicación orientada a objetos, **sin base de datos**, que gestiona clientes, servicios y
reservas de la empresa Software FJ (salas, equipos y asesorías). Los datos viven en listas
en memoria y solo se usa un archivo para el registro de eventos y errores (`logs_software_fj.log`).

## Estructura del proyecto
| Archivo | Contenido |
|---|---|
| `entidades.py` | Clase abstracta `Entidad` (base de todo el sistema) |
| `cliente.py` | `Cliente`: datos personales encapsulados y validados |
| `servicios.py` | `Servicio` (abstracta) y sus hijas `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `reserva.py` | `Reserva`: confirmar, cancelar y procesar con manejo de excepciones |
| `excepciones.py` | Excepciones personalizadas |
| `logger.py` | Configuración del archivo de logs |
| `main.py` | Simulación de 15 operaciones válidas e inválidas |

## Conceptos aplicados
- **Abstracción:** `Entidad` y `Servicio` son clases abstractas (`ABC`).
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `Entidad`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** cada servicio sobrescribe `validar_parametros`, `costo_base` y `describir`.
- **Encapsulación:** atributos privados con `@property` y validación en los setters.
- **Sobrecarga (simulada):** `calcular_costo(duracion, impuesto=None, descuento=0.0)` y `calcular_costo_con_descuento_fijo`.

## Manejo de excepciones
| Elemento | Dónde |
|---|---|
| Excepciones personalizadas | `excepciones.py` (jerarquía desde `SoftwareFJError`) |
| `try/except` | `Reserva.procesar`, `ejecutar()` en `main.py` |
| `try/except/else` | `convertir_duracion()` en `main.py` y `Reserva.procesar` |
| `try/finally` | Bloque final de `main.py` y `Reserva.procesar` |
| Encadenamiento (`raise ... from`) | `Reserva.procesar` y `convertir_duracion()` |
| Logging | Todos los errores y eventos en `logs_software_fj.log` |

## Cómo ejecutarlo
    python main.py

Al terminar se genera/actualiza `logs_software_fj.log` en la misma carpeta.

## Operaciones simuladas
1-4 clientes (válidos e inválidos) · 5-7 servicios (válidos e inválido) ·
8-13 reservas (éxito, duración inválida, servicio no disponible, doble cancelación, descuento inválido) ·
14-15 duración recibida como texto (inválida y válida).

## Equipo y flujo de trabajo
Cada integrante trabaja en su propia rama (`feature/...`), enlazada a un issue, y fusiona
a `main` mediante pull request revisado por un compañero.

| Integrante | Rama | Archivos |
|---|---|---|
| Integrante 1 | `feature/excepciones-logger` | `excepciones.py`, `logger.py` |
| Integrante 2 | `feature/cliente` | `entidades.py`, `cliente.py` |
| Integrante 3 | `feature/servicios` | `servicios.py` |
| Integrante 4 | `feature/reserva` | `reserva.py` |
| Integrante 5 | `feature/simulacion-readme` | `main.py`, `README.md` |
