from database import conectar_base_datos


class StockService:
    def __init__(self):
        self.conexion = conectar_base_datos()

    def registrar_compra_stock(
        self,
        producto_id,
        inversion_total,
        cantidad_unidades,
        costo_unitario,
        precio_venta_sugerido=None,
        porcentaje_ganancia=0,
        usuario_id=None,
        observacion=None,
    ):
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = """
                INSERT INTO stock_compras (
                    producto_id,
                    usuario_id,
                    inversion_total,
                    cantidad_unidades,
                    costo_unitario,
                    precio_venta_sugerido,
                    porcentaje_ganancia,
                    observacion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    producto_id,
                    usuario_id,
                    inversion_total,
                    cantidad_unidades,
                    costo_unitario,
                    precio_venta_sugerido,
                    porcentaje_ganancia,
                    observacion,
                ),
            )
            self.conexion.commit()
            compra_id = cursor.lastrowid
            cursor.close()
            return {"ok": True, "compra_id": compra_id}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
