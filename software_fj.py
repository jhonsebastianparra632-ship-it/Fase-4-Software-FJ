"""Software FJ - Fase 4, Programación 213023 (UNAD).
Sistema de clientes, servicios y reservas sin bases de datos.
Los datos son ficticios y las tarifas son supuestos de la simulación.
"""
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
import logging
import re

# Configuración del archivo de eventos y errores (sin almacenar clientes).
RUTA_LOG = Path('software_fj.log')
log = logging.getLogger('software_fj')
log.setLevel(logging.INFO)
log.propagate = False


def configurar_log():
    """Configura un registro nuevo por ejecución y evita manejadores duplicados."""
    for manejador in log.handlers[:]:
        log.removeHandler(manejador)
        manejador.close()
    manejador = logging.FileHandler(RUTA_LOG, mode='w', encoding='utf-8')
    manejador.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    log.addHandler(manejador)


# Excepciones propias del dominio.
class ErrorSistema(Exception):
    """Excepción base de Software FJ."""


class DatosInvalidos(ErrorSistema):
    """Datos ausentes, incorrectos o inconsistentes."""


class OperacionNoPermitida(ErrorSistema):
    """Operación incompatible con el estado del sistema."""


class ServicioNoDisponible(ErrorSistema):
    """Servicio ocupado o deshabilitado."""


def texto(valor, campo):
    """Valida cadenas obligatorias y elimina espacios externos."""
    if not isinstance(valor, str) or not valor.strip():
        raise DatosInvalidos(f'{campo}: debe ser un texto no vacío.')
    return valor.strip()


def numero(valor, campo, minimo=0, maximo=None, entero=False):
    """Convierte números y encadena la excepción original si hay un error."""
    try:
        if isinstance(valor, bool):
            raise TypeError('Un booleano no es un número válido aquí.')
        n = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError) as error:
        raise DatosInvalidos(f'{campo}: valor numérico inválido.') from error
    if not n.is_finite() or n < minimo or (maximo is not None and n > maximo):
        raise DatosInvalidos(f'{campo}: valor fuera del rango permitido.')
    if entero and n != n.to_integral_value():
        raise DatosInvalidos(f'{campo}: debe ser entero.')
    return n


class Entidad(ABC):
    """Abstracción de una entidad identificable del sistema."""
    def __init__(self, codigo):
        self.__codigo = texto(codigo, 'Código')

    @property
    def codigo(self):
        return self.__codigo

    @abstractmethod
    def describir(self):
        """Cada entidad define su propia descripción."""


class Cliente(Entidad):
    """Cliente con información personal encapsulada y validada."""
    def __init__(self, codigo, nombre, correo, telefono):
        super().__init__(codigo)
        self.__nombre = texto(nombre, 'Nombre')
        correo = texto(correo, 'Correo')
        telefono = texto(telefono, 'Teléfono')
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', correo):
            raise DatosInvalidos('Correo electrónico inválido.')
        if not re.fullmatch(r'[0-9]{10}', telefono):
            raise DatosInvalidos('El teléfono debe contener 10 dígitos.')
        self.__correo = correo
        self.__telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def describir(self):
        return f'Cliente {self.codigo}: {self.nombre}'


class Servicio(Entidad, ABC):
    """Base abstracta para los tres servicios especializados."""
    def __init__(self, codigo, nombre, tarifa, disponible=True):
        super().__init__(codigo)
        self.__nombre = texto(nombre, 'Nombre del servicio')
        self.__tarifa = numero(tarifa, 'Tarifa', Decimal('0.01'), 100000000)
        if not isinstance(disponible, bool):
            raise DatosInvalidos('Disponibilidad debe ser True o False.')
        self.__habilitado = disponible
        self.__ocupado_por = None

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tarifa(self):
        return self.__tarifa

    @property
    def disponible(self):
        return self.__habilitado and self.__ocupado_por is None

    def ocupar(self, reserva):
        if not self.disponible:
            raise ServicioNoDisponible(f'Servicio {self.codigo} no disponible.')
        self.__ocupado_por = reserva

    def liberar(self, reserva):
        if self.__ocupado_por is not reserva:
            raise OperacionNoPermitida('La reserva no es titular del servicio.')
        self.__ocupado_por = None

    @abstractmethod
    def validar_parametros(self, duracion, **parametros):
        """Valida la duración y los parámetros propios del servicio."""

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0, **parametros):
        """Método polimórfico con variantes mediante argumentos opcionales."""

    def _total(self, base, impuesto, descuento):
        # Los porcentajes se expresan de 0 a 100; primero se aplica descuento.
        i = numero(impuesto, 'Impuesto', 0, 100)
        d = numero(descuento, 'Descuento', 0, 100)
        return (base * (1-d/100) * (1+i/100)).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP)


class ReservaSala(Servicio):
    """Reserva de sala: tarifa por hora y capacidad máxima."""
    def __init__(self, codigo, nombre, tarifa, capacidad, disponible=True):
        super().__init__(codigo, nombre, tarifa, disponible)
        self.__capacidad = int(numero(capacidad, 'Capacidad', 1, 500, entero=True))

    def validar_parametros(self, duracion, personas=1):
        horas = numero(duracion, 'Horas de sala', 1, 12)
        numero(personas, 'Personas', 1, self.__capacidad, entero=True)
        return horas

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **parametros):
        horas = self.validar_parametros(duracion, **parametros)
        return self._total(horas*self.tarifa, impuesto, descuento)

    def describir(self):
        return f'Sala {self.nombre}: capacidad {self.__capacidad} personas.'


class AlquilerEquipo(Servicio):
    """Alquiler por hora y por unidad, limitado al inventario."""
    def __init__(self, codigo, nombre, tarifa, unidades, disponible=True):
        super().__init__(codigo, nombre, tarifa, disponible)
        self.__unidades = int(numero(unidades, 'Inventario', 1, 100, entero=True))

    def validar_parametros(self, duracion, cantidad=1):
        horas = numero(duracion, 'Horas de alquiler', 1, 72)
        numero(cantidad, 'Cantidad', 1, self.__unidades, entero=True)
        return horas

    def calcular_costo(self, duracion, impuesto=0, descuento=0, cantidad=1):
        horas = self.validar_parametros(duracion, cantidad)
        return self._total(horas*self.tarifa*Decimal(str(cantidad)), impuesto, descuento)

    def describir(self):
        return f'Equipo {self.nombre}: {self.__unidades} unidades.'


class Asesoria(Servicio):
    """Asesoría por hora, con recargo opcional para modalidad especializada."""
    def validar_parametros(self, duracion, especializada=False):
        horas = numero(duracion, 'Horas de asesoría', 1, 8)
        if not isinstance(especializada, bool):
            raise DatosInvalidos('Especializada debe ser True o False.')
        return horas

    def calcular_costo(self, duracion, impuesto=0, descuento=0, especializada=False):
        horas = self.validar_parametros(duracion, especializada)
        factor = Decimal('1.25') if especializada else Decimal('1')
        return self._total(horas*self.tarifa*factor, impuesto, descuento)

    def describir(self):
        return f'Asesoría {self.nombre}: tarifa por hora, recargo especializado del 25%.'


class Reserva(Entidad):
    """Relaciona cliente y servicio; controla las transiciones de estado."""
    def __init__(self, codigo, cliente, servicio, duracion, impuesto=0, descuento=0,
                 **parametros):
        super().__init__(codigo)
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise DatosInvalidos('Cliente o servicio inválido.')
        if not servicio.disponible:
            raise ServicioNoDisponible(f'Servicio {servicio.codigo} no disponible.')
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = numero(duracion, 'Duración', 1, 72)
        self.__estado = 'PENDIENTE'
        # El método concreto se determina en tiempo de ejecución (polimorfismo).
        try:
            self.__costo = servicio.calcular_costo(duracion, impuesto, descuento, **parametros)
        except TypeError as error:
            raise DatosInvalidos('Parámetros incorrectos para el servicio.') from error

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    def confirmar(self):
        if self.estado != 'PENDIENTE':
            raise OperacionNoPermitida('Solo se confirman reservas pendientes.')
        self.__servicio.ocupar(self)
        self.__estado = 'CONFIRMADA'
        log.info('Reserva %s confirmada.', self.codigo)

    def cancelar(self):
        if self.estado not in ('PENDIENTE', 'CONFIRMADA'):
            raise OperacionNoPermitida('La reserva no puede cancelarse en este estado.')
        if self.estado == 'CONFIRMADA':
            self.__servicio.liberar(self)
        self.__estado = 'CANCELADA'
        log.info('Reserva %s cancelada.', self.codigo)

    def procesar(self):
        # finally registra el cierre incluso si la operación falla.
        try:
            if self.estado != 'CONFIRMADA':
                raise OperacionNoPermitida('Solo se procesan reservas confirmadas.')
            self.__servicio.liberar(self)
            self.__estado = 'PROCESADA'
            log.info('Reserva %s procesada; costo COP %s.', self.codigo, self.costo)
            return self.costo
        finally:
            log.info('Fin del intento de procesamiento de %s.', self.codigo)

    def describir(self):
        return (f'Reserva {self.codigo}: cliente {self.__cliente.codigo}, '
                f'servicio {self.__servicio.codigo}, {self.__duracion} h, '
                f'{self.estado}, COP {self.costo}')


class Sistema:
    """Coordina las operaciones y conserva los objetos en listas privadas."""
    def __init__(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    def _agregar(self, lista, entidad):
        if any(e.codigo == entidad.codigo for e in lista):
            raise DatosInvalidos(f'Código duplicado: {entidad.codigo}.')
        lista.append(entidad)
        log.info('Registro exitoso: %s %s.', type(entidad).__name__, entidad.codigo)
        return entidad

    def _buscar(self, lista, codigo):
        codigo = texto(codigo, 'Código de búsqueda')
        for entidad in lista:
            if entidad.codigo == codigo:
                return entidad
        raise DatosInvalidos(f'No existe el código {codigo}.')

    def registrar_cliente(self, *args, **kwargs):
        return self._agregar(self.__clientes, Cliente(*args, **kwargs))

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatosInvalidos('Objeto de servicio inválido.')
        return self._agregar(self.__servicios, servicio)

    def crear_reserva(self, codigo, cliente, servicio, duracion, **parametros):
        c = self._buscar(self.__clientes, cliente)
        s = self._buscar(self.__servicios, servicio)
        return self._agregar(self.__reservas, Reserva(codigo, c, s, duracion, **parametros))

    def reserva(self, codigo):
        return self._buscar(self.__reservas, codigo)

    def ejecutar(self, nombre, operacion):
        """Frontera de errores: registra cada fallo y permite seguir operando."""
        try:
            resultado = operacion()
        except ErrorSistema as error:
            log.exception('%s: %s', nombre, error)
            return False, error
        except (TypeError, ValueError, ArithmeticError) as error:
            log.exception('%s: parámetro o cálculo inválido.', nombre)
            return False, error
        except Exception as error:
            log.exception('%s: error inesperado.', nombre)
            return False, error
        else:
            log.info('%s: operación exitosa.', nombre)
            return True, resultado
        finally:
            log.info('%s: intento finalizado.', nombre)


def simular():
    """Ejecuta 20 casos y compara cada resultado con lo esperado."""
    configurar_log()
    sistema = Sistema()
    log.info('Inicio de la simulación Software FJ.')
    # Cada función se ejecuta dentro del controlador de excepciones.
    casos = [
        ('Cliente válido', True, lambda: sistema.registrar_cliente('C1', 'Ana Demo', 'ana@example.com', '3000000001')),
        ('Correo inválido', False, lambda: sistema.registrar_cliente('C2', 'Luis Demo', 'correo_invalido', '3000000002')),
        ('Teléfono inválido', False, lambda: sistema.registrar_cliente('C2', 'Luis Demo', 'luis@example.com', '123')),
        ('Cliente duplicado', False, lambda: sistema.registrar_cliente('C1', 'Otro Demo', 'otro@example.com', '3000000003')),
        ('Sala válida', True, lambda: sistema.registrar_servicio(ReservaSala('S1', 'Sala A', 50000, 10))),
        ('Equipo válido', True, lambda: sistema.registrar_servicio(AlquilerEquipo('S2', 'Portátil', 20000, 5))),
        ('Asesoría válida', True, lambda: sistema.registrar_servicio(Asesoria('S3', 'Sistemas', 80000))),
        ('Tarifa inválida', False, lambda: sistema.registrar_servicio(Asesoria('S4', 'Prueba', -10))),
        ('Servicio deshabilitado', True, lambda: sistema.registrar_servicio(Asesoria('S4', 'No disponible', 10000, False))),
        ('Reserva de sala válida', True, lambda: sistema.crear_reserva('R1', 'C1', 'S1', 2, personas=4, impuesto=19, descuento=10)),
        ('Confirmación válida', True, lambda: sistema.reserva('R1').confirmar()),
        ('Sala ocupada', False, lambda: sistema.crear_reserva('R2', 'C1', 'S1', 1)),
        ('Duración no numérica', False, lambda: sistema.crear_reserva('R2', 'C1', 'S2', 'abc')),
        ('Inventario insuficiente', False, lambda: sistema.crear_reserva('R2', 'C1', 'S2', 2, cantidad=8)),
        ('Servicio no disponible', False, lambda: sistema.crear_reserva('R2', 'C1', 'S4', 1)),
        ('Procesamiento válido', True, lambda: sistema.reserva('R1').procesar()),
        ('Procesamiento repetido', False, lambda: sistema.reserva('R1').procesar()),
        ('Reserva de equipo válida', True, lambda: sistema.crear_reserva('R2', 'C1', 'S2', 3, cantidad=2)),
        ('Cancelación válida', True, lambda: sistema.reserva('R2').cancelar()),
        ('Reserva de asesoría válida', True, lambda: sistema.crear_reserva('R3', 'C1', 'S3', 2, especializada=True)),
    ]
    aprobadas = 0
    for indice, (nombre, esperado, operacion) in enumerate(casos, 1):
        exito, resultado = sistema.ejecutar(nombre, operacion)
        correcto = exito == esperado
        aprobadas += int(correcto)
        detalle = resultado.describir() if isinstance(resultado, Entidad) else resultado
        print(f'{indice:02d}. {nombre}: {"OK" if correcto else "FALLO"} | {detalle if detalle is not None else "Operación completada"}')
    # Verifica además los importes y estados resultantes de las operaciones.
    assert sistema.reserva('R1').costo == Decimal('107100.00')
    assert sistema.reserva('R1').estado == 'PROCESADA'
    assert sistema.reserva('R2').costo == Decimal('120000.00')
    assert sistema.reserva('R2').estado == 'CANCELADA'
    assert sistema.reserva('R3').costo == Decimal('200000.00')
    print(f'\nResultado: {aprobadas}/{len(casos)} simulaciones conformes.')
    print(f'Archivo de eventos y errores: {RUTA_LOG}')
    log.info('Fin de simulación: %s/%s casos conformes.', aprobadas, len(casos))
    return aprobadas


if __name__ == '__main__':
    simular()
