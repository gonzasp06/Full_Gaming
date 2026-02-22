from dataclasses import dataclass


@dataclass
class Producto:
    id: int
    nombre: str
    costo_unitario: float = 0.0
    precio_venta_unitario: float = 0.0


@dataclass
class IngresoStock:
    producto_id: int | None
    inversion_total: float
    cantidad_unidades: int
    porcentaje_ganancia: float = 0.0

    def costo_unitario(self) -> float:
        if self.cantidad_unidades <= 0:
            return 0.0
        return float(self.inversion_total) / float(self.cantidad_unidades)

    def precio_venta_sugerido(self) -> float:
        costo = self.costo_unitario()
        return costo * (1 + (float(self.porcentaje_ganancia) / 100.0))


@dataclass
class Venta:
    producto_id: int
    cantidad: int
    precio_unitario: float
    costo_unitario: float

    def ingreso_total(self) -> float:
        return float(self.precio_unitario) * int(self.cantidad)

    def costo_total(self) -> float:
        return float(self.costo_unitario) * int(self.cantidad)

    def ganancia_real(self) -> float:
        return self.ingreso_total() - self.costo_total()


class Balance:
    @staticmethod
    def calcular_ingresos_acumulados(ventas_totales: float) -> float:
        return float(ventas_totales or 0)

    @staticmethod
    def calcular_egresos_acumulados(egresos_totales: float) -> float:
        return float(egresos_totales or 0)

    @staticmethod
    def calcular_ganancia_real(ingresos: float, costo_vendido: float) -> float:
        return float(ingresos or 0) - float(costo_vendido or 0)
