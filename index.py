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
        
