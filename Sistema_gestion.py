import datetime
from typing import List
class Ciudad :
    def __init__(self,codigo,nombre,provincia) :
        self.codigo = codigo
        self.nombre = nombre
        self.provincia = provincia

class Servicio : 
    def __init__(self,unidad,fecha_partida,fecha_llegada,calidad,precio,itinerario):
        self.unidad = unidad
        self.fecha_partida = fecha_partida
        self.fecha_llegada = fecha_llegada
        self.calidad = calidad
        self.precio = precio
        self.itinerario = itinerario
class Itinerario :
    def __init__(self,ciudad_origen,ciudad_destino)  :
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino
        self.ciudades : List[Ciudad]  = []
    
class Argentur : 
    def __init__(self) :
        self.sistemaActivo = True
    def _cambiar_estado(self,estado) :
        self.sistemaActivo = estado

class Patente:
    _patentes_asignadas = set()

    def init(self, codigo):
        if codigo in Patente._patentes_asignadas:
            raise ValueError(f"La patente '{codigo}' ya está asignada a otro autobús.")
        self.codigo = codigo
        self.asignada = False
        Patente._patentes_asignadas.add(codigo)

    def str(self):
        return self.codigo

class Unidad:
    def init(self, patente, cantidad_asientos):
        if not isinstance(patente, Patente):
            raise TypeError("Se esperaba una instancia de la clase Patente")
        if patente.asignada:
            raise ValueError(f"La patente '{patente}' ya está asignada a otro autobús.")
        self.patente = patente
        self.asientos = [Asiento(i + 1) for i in range(cantidad_asientos)]
        patente.asignada = True

    def mostrar_asientos(self):
        for asiento in self.asientos:
            print(asiento)

    def str(self):
        return f"Autobús con patente {self.patente}"

class Asiento(Unidad) :
    def __init__(self,numero) :
        self.numero = numero 
        self.estado = "libre"
        self.estados = ["libre","ocupado","reservado"]
    def _cambiar_estado_asiento(self,str) :
        if str not in self.estados :
            return None
        self.estado = str
        return True 

class Venta : 
    def __init__(self) :
        self.fecha_venta = datetime.datetime.now().date()
        self.hora_venta = datetime.datetime.now().time()

class Reserva :
    def __init__(self,pasajero,asiento) :
        self.pasajero = pasajero
        self.asiento = asiento
        self.fecha_reserva = datetime.datetime.now().date()
        self.hora_venta = datetime.datetime.now().time()

class Pasajero :
    def __init__(self,nombre,email,dni) :
        self.nombre = nombre
        self.email = email
        self.dni = dni


class MedioPago :
    def _realizarpago() :
        return
class TarjetaCredito(MedioPago) :
    def __init__(self,numero,dni_titular,nombre_titular,fecha_vencimiento) :
        self.numero = numero
        self.dni_titular = dni_titular
        self.nombre_titular = nombre_titular
        self.fecha_vencimiento = fecha_vencimiento
    
class MercadoPago(MedioPago) :
    def __init__(self,email,celular) :
        self.email = email
        self.celuar = celular

class Uala(MedioPago) :
    def __init__(self,email,nombre_titular):
        self.nombre_titular = nombre_titular
        self.email = email



Itinerario = Itinerario(1,2)
Itinerario.ciudades = ["","",""]
