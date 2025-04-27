from abc import ABC, abstractmethod
import datetime
from typing import List
from datetime import datetime
import uuid

class Pasajero:
    def __init__(self, nombre, email, dni):
        self.nombre = nombre
        self.email = email
        self.dni = dni

    def ver_nombre(self):
        return self.nombre

    def ver_email(self):
        return self.email

    def ver_dni(self):
        return self.dni


class Patente:
    def __init__(self, codigo):
        self.codigo = codigo

    def cod_patente(self):
        return self.codigo


class GestorPatentes:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            GestorPatentes._instancia = object.__new__(cls)
            cls._instancia._patentes_asignadas = set()
        return cls._instancia

    def asignar_patente(self, patente: Patente):
        if patente.cod_patente() in self._patentes_asignadas:
            raise ValueError(f"La patente '{patente.cod_patente()}' ya está asignada.")
        self._patentes_asignadas.add(patente.cod_patente())


class Unidad:
    def __init__(self, patente, cantidad_asientos):
        gestorPatente = GestorPatentes()
        gestorPatente.asignar_patente(patente)
        self.patente = patente
        self.asientos = [Asiento(i + 1) for i in range(cantidad_asientos)]
        patente.asignada = True

    def ver_asientos(self):
        return self.asientos

    def ver_patente(self):
        return self.patente.cod_patente()


class Provincia:
    def __init__(self, cod_provincia, nom_provincia):
        self.cod_provincia = cod_provincia
        self.nombre = nom_provincia

    def ver_nombre(self):
        return self.nombre

    def ver_codigo(self):
        return self.cod_provincia


class Ciudad:
    def __init__(self, cod_ciudad, nom_ciudad, provincia: Provincia):
        self.cod_ciudad = cod_ciudad
        self.nombre = nom_ciudad
        self.provincia = provincia

    def ver_nombre(self):
        return self.nombre

    def ver_cod_ciudad(self):
        return self.cod_ciudad

    def ver_provincia(self):
        return self.provincia.nombre()


class Itinerario:
    def __init__(self, ciudad_origen, ciudad_destino, ciudades=[]):
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino
        self.ciudades: List[Ciudad] = ciudades

    def ver_paradas(self):
        return self.ciudades

    def agregar_parada(self, ciudad: Ciudad, nro_parada: int):
        self.ciudades.insert(nro_parada, ciudad)
        return self.ciudades

    def eliminar_parada(self, nro_parada: int):
        self.ciudades.pop(nro_parada)
        return self.ciudades

    def ver_ciudad_destino(self):
        return self.ciudad_destino


class Servicio:
    def __init__(
        self,
        unidad: Unidad,
        fecha_partida: datetime,
        fecha_llegada: datetime,
        calidad: str,
        precio: int,
        itinerario: Itinerario,
    ):
        self.id = uuid.uuid4()
        self.unidad = unidad
        self.fecha_partida = fecha_partida
        self.fecha_llegada = fecha_llegada
        self.calidad = calidad
        self.precio = precio
        self.itinerario = itinerario

    def ver_id(self):
        return self.id

    def ver_unidad(self):
        return self.unidad

    def ver_fecha_partida(self):
        return self.fecha_partida

    def ver_fecha_llegada(self):
        return self.fecha_llegada

    def ver_calidad(self):
        return self.calidad

    def ver_precio(self):
        return self.precio

    def ver_itinerario(self):
        return self.itinerario


class Argentur:
    def __init__(self):
        self.sistemaActivo = True

    def _cambiar_estado(self, estado):
        self.sistemaActivo = estado


class Asiento:
    LIBRE = "libre"
    OCUPADO = "ocupado"
    RESERVADO = "reservado"
    ESTADOS_VALIDOS = {LIBRE, OCUPADO, RESERVADO}

    def __init__(self, numero):
        self.numero = numero
        self._estado= Asiento.LIBRE

    def _cambiar_estado_asiento(self, str):
        if str not in self.ESTADOS_VALIDOS:
            return None
        self._estado= str
        return True

    def reservar(self):
        if self._estado != Asiento.LIBRE:
            raise Exception(
                f"No se puede reservar. El asiento {self._numero} está {self._estado}."
            )
        self._cambiar_estado_asiento(Asiento.RESERVADO)

    def ocupar(self):
        if self._estado == Asiento.OCUPADO:
            raise Exception(f"El asiento {self._numero} ya está ocupado.")
        self._cambiar_estado_asiento(Asiento.OCUPADO)

    def liberar(self):
        if self._estado == Asiento.LIBRE:
            raise Exception(f"El asiento {self._numero} ya está libre.")
        self._cambiar_estado_asiento(Asiento.LIBRE)

    def ver_estado(self):
        return self._estado

    def ver_numero(self):
        return self.numero


class Venta:
    def __init__(self, monto, localidad_destino, medio_pago):
        self.fecha_venta = datetime.now()
        self.monto = monto
        self.localidad_destino = localidad_destino
        self.medio_pago = medio_pago


class GestorVentas:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            GestorVentas._instancia = object.__new__(cls)
            cls._instancia._ventas = []
        return cls._instancia

    def agregar_venta(self, venta: Venta):
        self._ventas.append(venta)

    def generar_informe(self, desde: datetime.date, hasta: datetime.date):
        monto_total = 0
        viajes_por_localidad = {}
        pagos_por_medio = {}
        for venta in self._ventas:
            if desde <= venta.fecha_venta <= hasta:
                monto_total += venta.monto

                if venta.localidad_destino in viajes_por_localidad:
                    viajes_por_localidad[venta.localidad_destino] += 1
                else:
                    viajes_por_localidad[venta.localidad_destino] = 1

                if venta.medio_pago in pagos_por_medio:
                    pagos_por_medio[venta.medio_pago] += 1
                else:
                    pagos_por_medio[venta.medio_pago] = 1

        print("--Informe de ventas--")
        print(f"Período: {desde} hasta {hasta}")
        print(f"Monto total facturdado: {monto_total} $")
        print("Cantidad de viajes por destino: ")
        for local, cantidad in viajes_por_localidad.items():
            print(f"{local}:{cantidad} viaje/s")
        print("Cantidad de pagos por medio de pago: ")
        for medio, cant in pagos_por_medio.items():
            print(f"{medio}:{cant} pago/s")


class Reserva:
    def __init__(self, pasajero: Pasajero, id_servicio, asiento):
        self.pasajero = pasajero
        self.asiento = asiento
        self.fecha_reserva = datetime.now()
        self.servicio = id_servicio

    def mostrar_pasajero(self):
        return self.pasajero

    def mostrar_asiento(self):
        return self.asiento

    def mostrar_fecha_reserva(self):
        return self.fecha_reserva.strftime("%d/%m/%Y %H:%M")

    def mostrar_servicio(self):
        return self.servicio


class GestorReserva:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            GestorReserva._instancia = object.__new__(cls)
            cls._instancia._reservas = []
        return cls._instancia

    def agregar_reserva(self, reserva):
        self._reservas.append(reserva)

    def buscar_reserva(self, pasajero, servicio):
        for reserva in self._reservas:
            if reserva.pasajero == pasajero and reserva.servicio == servicio:
                return reserva
        return None
    
class MedioPago(ABC):
    @abstractmethod
    def realizarpago():
        pass


class TarjetaCredito(MedioPago):
    def __init__(self, numero, dni_titular, nombre_titular, fecha_vencimiento):
        self.numero = numero
        self.dni_titular = dni_titular
        self.nombre_titular = nombre_titular
        self.fecha_vencimiento = fecha_vencimiento

    def realizarpago(self):
        print("Pago realizado con Tarjeta de Crédito")

    def __str__(self):
        return f"TarjetaCredito"


class MercadoPago(MedioPago):
    def __init__(self, email, celular):
        self.email = email
        self.celuar = celular

    def realizarpago(self):
        print("Pago realizado con Mercado Pago")

    def __str__(self):
        return f"Mercadopago"


class Uala(MedioPago):
    def __init__(self, email, nombre_titular):
        self.nombre_titular = nombre_titular
        self.email = email

    def realizarpago(self):
        print("Pago realizado con Ualá")

    def __str__(self):
        return f"Uala"


def mostrar_servicio(servicio: Servicio, numero: int):
    print(f"--- Servicio {numero} ---")
    print(f"Unidad: {servicio.ver_unidad().ver_patente()}")
    print(
        f"Fecha de partida: {servicio.ver_fecha_partida().strftime('%d/%m/%Y %H:%M')}"
    )
    print(
        f"Fecha de llegada: {servicio.ver_fecha_llegada().strftime('%d/%m/%Y %H:%M')}"
    )
    print(f"Calidad: {servicio.ver_calidad()}")
    print(f"Precio: ${servicio.ver_precio()}")
    print("Itinerario:")
    print(f"  Origen: {servicio.ver_itinerario().ciudad_origen.ver_nombre()}")
    print(f"  Destino: {servicio.ver_itinerario().ciudad_destino.ver_nombre()}")
    print("  Paradas intermedias:")
    for i, ciudad in enumerate(servicio.ver_itinerario().ver_paradas()):
        print(f"   - Parada {i + 1}: {ciudad.ver_nombre()}")
    print("")


def seleccionar_servicio(servicios: List[Servicio], ventas: GestorVentas) -> Servicio:
    print("Servicios disponibles:\n")
    for i, servicio in enumerate(servicios, start=1):
        mostrar_servicio(servicio, i)

    while True:
        try:
            seleccion = int(input(f"Seleccione un servicio (1-{len(servicios)}): "))
            if 1 <= seleccion <= len(servicios):
                return servicios[seleccion - 1]
            else:
                print("Número fuera de rango.")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")


def mostrar_asientos(unidad: Unidad):
    print("Estado de los asientos:\n")
    for asiento in unidad.ver_asientos():
        estado = asiento.ver_estado().capitalize()
        print(f"Asiento {asiento.ver_numero():02d}: {estado}")


def reservar_asiento(servicio: Servicio, pasajero: Pasajero, nro_asiento: int):
    unidad = servicio.ver_unidad()
    asientos = unidad.ver_asientos()

    if nro_asiento < 1 or nro_asiento > len(asientos):
        print(f"Asiento inválido. Debe estar entre 1 y {len(asientos)}.")
        return

    asiento = asientos[nro_asiento - 1]
    if asiento.ver_estado() != "libre":
        print(f"Error: El asiento {nro_asiento} no está disponible.")
        return

    print("Métodos de pagos disponibles: 1)Uala - 2)TarjetaCredito - 3)MercadoPago")
    metodo_pago = int(input("Escriba su metodo de pago: "))
    medio_pago = None
    match metodo_pago:
        case 1:
            medio_pago = Uala(pasajero.ver_email(), pasajero.ver_nombre())
        case 2:
            numero_tar = input("Ingrese número de la tarjeta: ")
            vencimiento = input("Ingrese vencimiento de la tarjeta: ")
            medio_pago = TarjetaCredito(
                numero_tar, pasajero.ver_dni(), pasajero.ver_nombre(), vencimiento
            )
        case 3:
            celular = input("Ingrese su celular: ")
            medio_pago = MercadoPago(pasajero.ver_email(), celular)
        case _:
            print("Método de pago inválido")
            return
    medio_pago.realizarpago()
    monto = servicio.ver_precio()
    nombre_localidad = servicio.ver_itinerario().ver_ciudad_destino().ver_nombre()
    nueva_venta = Venta(monto, nombre_localidad, medio_pago)
    ventas.agregar_venta(nueva_venta)

    asiento.reservar()
    gestorReserva = GestorReserva()
    reserva = Reserva(pasajero, servicio.ver_id(), asiento)
    gestorReserva.agregar_reserva(reserva)
    print(
        f"Reserva realizada: Pasajero {pasajero.ver_nombre()}, asiento {nro_asiento}, servicio del {servicio.ver_fecha_partida().strftime('%d/%m/%Y')}, a las {servicio.ver_fecha_partida().strftime("%H:%M")}hs"
    )


# Provincias
santa_fe = Provincia(1, "Santa Fe")
cordoba = Provincia(2, "Córdoba")
buenos_aires = Provincia(3, "Buenos Aires")
mendoza = Provincia(4, "Mendoza")
salta = Provincia(5, "Salta")
neuquen = Provincia(6, "Neuquén")


# Provincias
santa_fe = Provincia(1, "Santa Fe")
cordoba = Provincia(2, "Córdoba")
buenos_aires = Provincia(3, "Buenos Aires")
mendoza = Provincia(4, "Mendoza")
salta = Provincia(5, "Salta")
neuquen = Provincia(6, "Neuquén")


# Ciudades
santa_fe_capital = Ciudad(3000, "Santa Fe", santa_fe)
cordoba_santa_fe_capital = Ciudad(5000, "Córdoba", cordoba)
la_plata = Ciudad(1900, "La Plata", buenos_aires)
rosario = Ciudad(2000, "Rosario", santa_fe)
san_nicolas = Ciudad(2900, "San Nicolás", buenos_aires)
mendoza_capital = Ciudad(5500, "Mendoza", mendoza)
salta_capital = Ciudad(4400, "Salta", salta)
neuquen_capital = Ciudad(8300, "Neuquén", neuquen)
san_rafael = Ciudad(5600, "San Rafael", mendoza)
cafayate = Ciudad(4427, "Cafayate", salta)
cutral_co = Ciudad(8322, "Cutral Co", neuquen)

# Itinerarios
itinerario1 = Itinerario(santa_fe_capital, la_plata, [rosario])
itinerario2 = Itinerario(la_plata, santa_fe_capital, [san_nicolas, rosario])
itinerario3 = Itinerario(mendoza_capital, salta_capital, [san_rafael, cafayate])
itinerario4 = Itinerario(neuquen_capital, mendoza_capital, [cutral_co])
# print("Paradas itinerario 1:")
# nro = 0
# for parada in itinerario1.ver_paradas():
#     print(f"Parada {nro}: {parada.ver_nombre()}")
#     nro += 1
# print("")

# nro = 0
# print("Nuevas paradas itinerario 2")
itinerario1.agregar_parada(san_nicolas, 1)
# for parada in itinerario1.ver_paradas():
#     print(f"Parada {nro}: {parada.ver_nombre()}")
#     nro += 1
# print("")

# nro = 0
# nro_parada = int(input("Eliminar una parada:"))
# for parada in itinerario1.eliminar_parada(nro_parada):
#     print(f"Parada {nro}: {parada.ver_nombre()}")
#     nro += 1
# print("")

gestorPatentes = GestorPatentes()

# Patentes
patente1 = Patente("ABC123")
patente2 = Patente("DEF456")
patente3 = Patente("GHI789")

# Unidades
unidad1 = Unidad(patente1, 20)
unidad2 = Unidad(patente2, 30)
unidad3 = Unidad(patente3, 25)

# Servicios
servicio1 = Servicio(
    unidad1,
    datetime(2024, 5, 1, 16, 30),
    datetime(2024, 5, 1, 23, 30),
    "Común",
    100000,
    itinerario1,
)

servicio2 = Servicio(
    unidad1,
    datetime(2024, 5, 10, 16, 30),
    datetime(2024, 5, 10, 23, 30),
    "Común",
    100000,
    itinerario2,
)
servicio3 = Servicio(
    unidad2,
    datetime(2024, 5, 15, 18, 0),
    datetime(2024, 5, 16, 9, 0),
    "Ejecutivo",
    150000,
    itinerario3,
)
servicio4 = Servicio(
    unidad3,
    datetime(2024, 5, 20, 8, 30),
    datetime(2024, 5, 20, 20, 30),
    "Común",
    95000,
    itinerario4,
)

# Mostrar servicios
mostrar_servicio(servicio1, 1)
mostrar_servicio(servicio2, 2)
mostrar_servicio(servicio3, 3)
mostrar_servicio(servicio4, 4)
mostrar_servicio(servicio4, 4)

# Seleccionar servivico
ventas = GestorVentas()
servicios = [servicio1, servicio2, servicio3, servicio4]
servicio_seleccionado = seleccionar_servicio(servicios, ventas)

# Mostrar asientos
mostrar_asientos(servicio_seleccionado.ver_unidad())

# Crear un pasajero
pasajero1 = Pasajero("Larocca Ignacio", "laroccanacho@gmail.com", "45338215")

# Reserva asiento
asiento = int(input("Seleccione un asiento : "))
reservar_asiento(servicio_seleccionado, pasajero1, asiento)
mostrar_asientos(servicio_seleccionado.ver_unidad())

# Informe
fecha_desde = datetime(2025, 1, 1)
fecha_hasta = datetime(2025, 12, 31)
ventas.generar_informe(fecha_desde, fecha_hasta)

reservas = GestorReserva()

print(pasajero1.ver_nombre())
mostrar_servicio(servicio_seleccionado, 1)

reserva = reservas.buscar_reserva(pasajero1, servicio_seleccionado.ver_id())

print(f"Reserva a nombre de {reserva.mostrar_pasajero().ver_nombre()}")