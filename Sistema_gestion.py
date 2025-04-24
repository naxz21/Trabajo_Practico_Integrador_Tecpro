from abc import ABC, abstractmethod
import datetime
from typing import List


class Patente:
    _patentes_asignadas = set()

    def __init__(self, codigo):
        if codigo in Patente._patentes_asignadas:
            raise ValueError(f"La patente '{codigo}' ya está asignada a otro autobús.")
        self.codigo = codigo
        self.asignada = False
        Patente._patentes_asignadas.add(codigo)

    def cod_patente(self):
        return self.codigo


class Unidad:
    def __init__(self, patente, cantidad_asientos):
        if not isinstance(patente, Patente):
            raise TypeError("Se esperaba una instancia de la clase Patente")
        if patente.asignada:
            raise ValueError(f"La patente '{patente}' ya está asignada a otro autobús.")
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
        self.unidad = unidad
        self.fecha_partida = fecha_partida
        self.fecha_llegada = fecha_llegada
        self.calidad = calidad
        self.precio = precio
        self.itinerario = itinerario

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


class Asiento(Unidad):
    def __init__(self, numero):
        self.numero = numero
        self.estado = "libre"
        self.estados = ["libre", "ocupado", "reservado"]

    def _cambiar_estado_asiento(self, str):
        if str not in self.estados:
            return None
        self.estado = str
        return True


class Venta:
    def __init__(self):
        self.fecha_venta = datetime.datetime.now().date()
        self.hora_venta = datetime.datetime.now().time()


class Reserva:
    def __init__(self, pasajero, asiento):
        self.pasajero = pasajero
        self.asiento = asiento
        self.fecha_reserva = datetime.datetime.now().date()
        self.hora_venta = datetime.datetime.now().time()


class Pasajero:
    def __init__(self, nombre, email, dni):
        self.nombre = nombre
        self.email = email
        self.dni = dni


class MedioPago(ABC):
    # @abstractmethod
    def _realizarpago():
        pass


class TarjetaCredito(MedioPago):
    def __init__(self, numero, dni_titular, nombre_titular, fecha_vencimiento):
        self.numero = numero
        self.dni_titular = dni_titular
        self.nombre_titular = nombre_titular
        self.fecha_vencimiento = fecha_vencimiento


class MercadoPago(MedioPago):
    def __init__(self, email, celular):
        self.email = email
        self.celuar = celular


class Uala(MedioPago):
    def __init__(self, email, nombre_titular):
        self.nombre_titular = nombre_titular
        self.email = email

def mostrar_servicio(servicio: Servicio, numero: int):
    print(f"--- Servicio {numero} ---")
    print(f"Unidad: {servicio.ver_unidad().ver_patente()}")
    print(f"Fecha de partida: {servicio.ver_fecha_partida().strftime('%d/%m/%Y %H:%M')}")
    print(f"Fecha de llegada: {servicio.ver_fecha_llegada().strftime('%d/%m/%Y %H:%M')}")
    print(f"Calidad: {servicio.ver_calidad()}")
    print(f"Precio: ${servicio.ver_precio()}")
    print("Itinerario:")
    print(f"  Origen: {servicio.ver_itinerario().ciudad_origen.ver_nombre()}")
    print(f"  Destino: {servicio.ver_itinerario().ciudad_destino.ver_nombre()}")
    print("  Paradas intermedias:")
    for i, ciudad in enumerate(servicio.ver_itinerario().ver_paradas()):
        print(f"   - Parada {i + 1}: {ciudad.ver_nombre()}")
    print("")

# Provincias
santa_fe = Provincia(1, "Santa Fe")
cordoba = Provincia(2, "Córdoba")
buenos_aires = Provincia(3, "Buenos Aires")
mendoza = Provincia(4, "Mendoza")
salta = Provincia(5, "Salta")
neuquen = Provincia(6, "Neuquén")

#Ciudades
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
    datetime.datetime(2024, 5, 1, 16, 30),
    datetime.datetime(2024, 5, 1, 23, 30),
    "Común",
    100000,
    itinerario1,
)
servicio2 = Servicio(
    unidad1,
    datetime.datetime(2024, 5, 10, 16, 30),
    datetime.datetime(2024, 5, 10, 23, 30),
    "Común",
    100000,
    itinerario2,
)
servicio3 = Servicio(
    unidad2,
    datetime.datetime(2024, 5, 15, 18, 0),
    datetime.datetime(2024, 5, 16, 9, 0),
    "Ejecutivo",
    150000,
    itinerario3
)
servicio4 = Servicio(
    unidad3,
    datetime.datetime(2024, 5, 20, 8, 30),
    datetime.datetime(2024, 5, 20, 20, 30),
    "Común",
    95000,
    itinerario4
)

# Mostrar servicios
mostrar_servicio(servicio1, 1)
mostrar_servicio(servicio2, 2)
mostrar_servicio(servicio3, 3)
mostrar_servicio(servicio4, 4)