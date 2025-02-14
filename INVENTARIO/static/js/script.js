document.addEventListener('DOMContentLoaded', function() {
    const productoForm = document.getElementById('productoForm');
    const btnIngresar = document.getElementById('btnIngresar');
    const btnActualizar = document.getElementById('btnActualizar');
    const tablaProductos = document.getElementById('tablaProductos');
    const btnAnterior = document.getElementById('btnAnterior');
    const btnSiguiente = document.getElementById('btnSiguiente');

    let productoEditando = null;
    let offset = 0; // Iniciar en la primera página
    const limit = 10; // Número de productos por página

    // Cargar productos al iniciar la página
    cargarProductos(limit, offset);

    // Función para cargar los productos desde el backend
    function cargarProductos(limit, offset) {
        fetch(`/inventario?limit=${limit}&offset=${offset}`)
            .then(response => response.json())
            .then(data => {
                tablaProductos.innerHTML = '';
                data.forEach(producto => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${producto.id}</td>
                        <td>${producto.nombre}</td>
                        <td>${producto.cantidad}</td>
                        <td>${producto.precio_neto}</td>
                        <td>${producto.pvp}</td>
                        <td>
                            <button class="btn btn-warning btn-sm" onclick="editarProducto(${producto.id})">Editar</button>
                            <button class="btn btn-danger btn-sm" onclick="eliminarProducto(${producto.id})">Eliminar</button>
                        </td>
                    `;
                    tablaProductos.appendChild(row);
                });
            });
    }

    // Función para editar un producto
    window.editarProducto = function(id) {
        fetch(`/inventario/${id}`)
            .then(response => response.json())
            .then(producto => {
                document.getElementById('nombre').value = producto.nombre;
                document.getElementById('cantidad').value = producto.cantidad;
                document.getElementById('precio_neto').value = producto.precio_neto;
                document.getElementById('pvp').value = producto.pvp;
                btnIngresar.style.display = 'none';
                btnActualizar.style.display = 'inline-block';
                productoEditando = id;
            });
    };

    // Función para eliminar un producto
    window.eliminarProducto = function(id) {
        if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
            fetch(`/inventario/${id}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (response.ok) {
                    cargarProductos(limit, offset);
                }
            });
        }
    };

    // Manejar el envío del formulario (Ingresar o Actualizar)
    productoForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const nombre = document.getElementById('nombre').value;
        const cantidad = document.getElementById('cantidad').value;
        const precio_neto = document.getElementById('precio_neto').value;
        const pvp = document.getElementById('pvp').value;

        const producto = {
            nombre,
            cantidad,
            precio_neto,
            pvp
        };

        if (productoEditando === null) {
            // Ingresar un nuevo producto
            fetch('/inventario', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(producto)
            })
            .then(response => response.json())
            .then(data => {
                cargarProductos(limit, offset);
                productoForm.reset();
            });
        } else {
            // Actualizar un producto existente
            fetch(`/inventario/${productoEditando}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(producto)
            })
            .then(response => {
                if (response.ok) {
                    cargarProductos(limit, offset);
                    productoForm.reset();
                    btnIngresar.style.display = 'inline-block';
                    btnActualizar.style.display = 'none';
                    productoEditando = null;
                }
            });
        }
    });

    // Manejar el botón "Anterior"
    btnAnterior.addEventListener('click', function() {
        if (offset >= limit) {
            offset -= limit;
            cargarProductos(limit, offset);
        }
    });

    // Manejar el botón "Siguiente"
    btnSiguiente.addEventListener('click', function() {
        offset += limit;
        cargarProductos(limit, offset);
    });
});