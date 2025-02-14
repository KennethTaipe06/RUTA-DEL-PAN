class Inventario:
    def __init__(self, id, nombre, cantidad, precio_neto, pvp):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio_neto = precio_neto
        self.pvp = pvp


class InventarioDAO:
    def __init__(self, db):
        self.db = db

    def obtener_productos(self, limit, offset):
        cursor = self.db.cursor(dictionary=True)
        cursor.callproc('ObtenerProductos', (limit, offset))
        for result in cursor.stored_results():
            return result.fetchall()

    def obtener_producto_por_id(self, id):
        cursor = self.db.cursor(dictionary=True)
        cursor.callproc('ObtenerProductoPorId', (id,))
        for result in cursor.stored_results():
            return result.fetchone()

    def agregar_producto(self, producto):
        cursor = self.db.cursor()
        cursor.callproc('AgregarProducto', (producto.nombre, producto.cantidad, producto.precio_neto, producto.pvp))
        self.db.commit()
        return cursor.lastrowid

    def actualizar_producto(self, producto):
        cursor = self.db.cursor()
        cursor.callproc('ActualizarProducto', (
            producto.id,
            producto.nombre,
            producto.cantidad,
            producto.precio_neto,
            producto.pvp
        ))
        self.db.commit()
        return cursor.rowcount

    def eliminar_producto(self, id):
        cursor = self.db.cursor()
        cursor.callproc('EliminarProducto', (id,))
        self.db.commit()
        return cursor.rowcount
