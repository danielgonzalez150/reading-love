# Resumen de Cambios

## Fecha
- 2026-05-11

## Cambios principales
- Se corrigio el flujo de compra para respetar la estructura real de la BD:
  - `transacciones`: se inserta `id_cliente`, `fecha`, `total`.
  - `detalle_transaccion`: se inserta `id_transaccion`, `id_libro`, `cantidad`, `precio_unitario`.
  - Se elimino `subtotal` del insert porque es una columna generada en la BD.
- Se actualiza el stock del libro despues de crear la compra.

## Nuevo mini historial de compras
- Backend:
  - Se agrego `get_purchase_history(user_id)` en `database/book_repository.py`.
  - Se agrego endpoint `GET /api/historial-compras` en `app.py`.
  - El historial se devuelve solo para el usuario autenticado (segun cookie `session_token`).
- Frontend:
  - Se agrego boton `Mi historial` en la barra de navegacion.
  - Se agrego modal desplegable de historial en `templates/index.html`.
  - Se agrego funcion JS `abrirHistorialCompras()` para consultar la API y renderizar compras.
  - Se agrego funcion `cerrarModalHistorial()` y cierre al click fuera del modal.
- Estilos:
  - Se agregaron estilos para tarjetas del historial, lista de items, total por compra y estado vacio en `static/css/styles.css`.

## Archivos modificados
- `database/book_repository.py`
- `app.py`
- `templates/index.html`
- `static/css/styles.css`

## Archivo nuevo
- `RESUMEN_CAMBIOS.md`