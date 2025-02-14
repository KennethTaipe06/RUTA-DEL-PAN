from flask import Blueprint, request, jsonify
from database import get_db_connection
from models.inventario import Inventario, InventarioDAO

inventario_bp = Blueprint('inventario_bp', __name__)

@inventario_bp.route('/inventario', methods=['GET'])
def obtener_productos():
    # Obtener parámetros de paginación
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    db = get_db_connection()
    dao = InventarioDAO(db)
    productos = dao.obtener_productos(limit, offset)
    db.close()
    return jsonify(productos)

@inventario_bp.route('/inventario/<int:id>', methods=['GET'])
def obtener_producto(id):
    db = get_db_connection()
    dao = InventarioDAO(db)
    producto = dao.obtener_producto_por_id(id)
    db.close()
    if producto:
        return jsonify(producto)
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

@inventario_bp.route('/inventario', methods=['POST'])
def agregar_producto():
    datos = request.json
    db = get_db_connection()
    dao = InventarioDAO(db)
    producto_id = dao.agregar_producto(Inventario(
        id=None,
        nombre=datos['nombre'],
        cantidad=datos['cantidad'],
        precio_neto=datos['precio_neto'],
        pvp=datos['pvp']
    ))
    db.close()
    return jsonify({"id": producto_id, "message": "Producto agregado"}), 201

@inventario_bp.route('/inventario/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    datos = request.json
    db = get_db_connection()
    dao = InventarioDAO(db)
    filas_actualizadas = dao.actualizar_producto(Inventario(
        id=id,
        nombre=datos.get('nombre'),
        cantidad=datos.get('cantidad'),
        precio_neto=datos.get('precio_neto'),
        pvp=datos.get('pvp')
    ))
    db.close()
    if filas_actualizadas > 0:
        return jsonify({"message": "Producto actualizado correctamente"}), 200
    else:
        return jsonify({"error": "No se encontró el producto con el ID proporcionado"}), 404

@inventario_bp.route('/inventario/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    db = get_db_connection()
    dao = InventarioDAO(db)
    filas_eliminadas = dao.eliminar_producto(id)
    db.close()
    if filas_eliminadas > 0:
        return jsonify({"message": "Producto eliminado correctamente"}), 200
    else:
        return jsonify({"error": "No se encontró el producto con el ID proporcionado"}), 404
