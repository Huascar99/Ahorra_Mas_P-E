from flask import Flask, render_template, request, redirect, url_for
import logica
import validaciones
import persistencia

app = Flask(__name__)
app.secret_key = "ahorramas_clave_propia"


# ==============================================================================
# FUNCIÓN: renderizar_panel
# - QUÉ HACE: Centraliza la carga de la matriz CRUD desde `persistencia` y el
#   renderizado de la plantilla única `index.html` con sus parámetros de sección,
#   subsección, datos de formulario, errores y resultados.
# - POR QUÉ LO HACE: Porque en el código original todas las rutas repetían una
#   y otra vez `persistencia.obtener_todos_los_registros()` y los mismos
#   argumentos de `render_template`. Centralizarlo en una función auxiliar
#   reduce el código repetido y evita olvidos.
# - PARA QUÉ SIRVE: Para que todas las rutas de Flask entreguen siempre la
#   vista actualizada con la matriz CRUD cargada y la pestaña activa correcta.
# ==============================================================================
def renderizar_panel(seccion="dashboard", subseccion="definida", form_data=None, **kwargs):
    return render_template(
        "index.html",
        seccion_activa=seccion,
        subseccion_activa=subseccion,
        form_data=form_data if form_data is not None else {},
        matriz_crud=persistencia.obtener_todos_los_registros(),
        **kwargs
    )


# ==============================================================================
# FUNCIÓN: index (Ruta GET "/")
# - QUÉ HACE: Recibe la petición inicial al abrir la aplicación o al volver de
#   una redirección del CRUD, lee qué pestaña (`seccion`) y mensaje (`msg`) se
#   deben mostrar y despliega el panel principal.
# - POR QUÉ LO HACE: Porque la aplicación funciona como una interfaz unificada
#   por pestañas donde el servidor indica qué sección abrir inicialmente.
# - PARA QUÉ SIRVE: Es la puerta de entrada principal de la aplicación web.
# ==============================================================================
@app.route("/", methods=["GET"])
def index():
    seccion = request.args.get("seccion", "dashboard")
    subseccion = request.args.get("subseccion", "definida")
    mensaje_exito = request.args.get("msg", "")
    return renderizar_panel(seccion=seccion, subseccion=subseccion, mensaje_exito=mensaje_exito)


# ==============================================================================
# FUNCIÓN: calcular_gastos (Ruta POST "/gastos")
# - QUÉ HACE: Procesa el formulario del Módulo 1, valida las entradas con
#   `validaciones.validar_datos_gastos` y, si son correctas, calcula el balance
#   y semáforo de gastos mediante `logica.calcular_balance_gastos`.
# - POR QUÉ LO HACE: Para separar el flujo en 3 capas limpias: primero validar,
#   luego calcular en el módulo de lógica y finalmente presentar en la vista.
# - PARA QUÉ SIRVE: Para responder al envío del formulario de "Cálculo de Gastos".
# ==============================================================================
@app.route("/gastos", methods=["POST"])
def calcular_gastos():
    es_valido, datos, errores = validaciones.validar_datos_gastos(request.form)
    if not es_valido:
        return renderizar_panel(seccion="gastos", form_data=request.form, errores=errores)

    resultado = logica.calcular_balance_gastos(
        datos["nombre"],
        datos["capital"],
        datos["servicios_basicos"],
        datos["servicios_cable"],
        datos["otros_gastos"]
    )
    return renderizar_panel(seccion="gastos", form_data=request.form, resultado_gastos=resultado)


# ==============================================================================
# FUNCIÓN: calcular_ahorro_mensual (Ruta POST "/ahorro-mensual")
# - QUÉ HACE: Valida los datos de ingresos y gastos enviados desde el Módulo 2
#   y ejecuta `logica.calcular_ahorro_mensual` para aplicar la regla 60/25/15
#   o 70/20/10.
# - POR QUÉ LO HACE: Porque el cálculo de distribución presupuestaria debe
#   ejecutarse en el servidor sólo después de comprobar que el capital es
#   positivo y los gastos no son negativos.
# - PARA QUÉ SIRVE: Para mostrar al usuario si es apto para ahorrar y cuánto
#   debe destinar a necesidades, ahorro y gustos en el mes.
# ==============================================================================
@app.route("/ahorro-mensual", methods=["POST"])
def calcular_ahorro_mensual():
    es_valido, datos, errores = validaciones.validar_datos_ahorro_mensual(request.form)
    if not es_valido:
        return renderizar_panel(seccion="ahorro_mensual", form_data=request.form, errores=errores)

    resultado = logica.calcular_ahorro_mensual(
        datos["nombre"],
        datos["capital"],
        datos["servicios_basicos"],
        datos["servicios_cable"],
        datos["otros_gastos"]
    )
    return renderizar_panel(seccion="ahorro_mensual", form_data=request.form, resultado_ahorro_mensual=resultado)


# ==============================================================================
# FUNCIÓN: calcular_ahorro_anual (Ruta POST "/ahorro-anual")
# - QUÉ HACE: Valida los parámetros financieros del Módulo 3 y llama a
#   `logica.calcular_ahorro_anual` para generar la matriz de proyección de
#   12 meses `[mes, cuota_fija, total_acumulado]`.
# - POR QUÉ LO HACE: Para conectar el formulario de simulación anual con el
#   generador matricial de 12 filas en la capa de lógica.
# - PARA QUÉ SIRVE: Para renderizar la tabla de proyección anual mes a mes en
#   la pestaña "Ahorro Anual (Matriz)".
# ==============================================================================
@app.route("/ahorro-anual", methods=["POST"])
def calcular_ahorro_anual():
    es_valido, datos, errores = validaciones.validar_datos_ahorro_anual(request.form)
    if not es_valido:
        return renderizar_panel(seccion="ahorro_anual", form_data=request.form, errores=errores)

    resultado = logica.calcular_ahorro_anual(
        datos["nombre"],
        datos["capital"],
        datos["servicios_basicos"],
        datos["servicios_cable"],
        datos["otros_gastos"]
    )
    return renderizar_panel(seccion="ahorro_anual", form_data=request.form, resultado_ahorro_anual=resultado)


# ==============================================================================
# FUNCIÓN: plan_definido (Ruta POST "/plan-definido")
# - QUÉ HACE: Valida los datos del formulario de meta con fecha límite y llama
#   a `logica.calcular_meta_definida` para obtener las cuotas diaria, semanal
#   y mensual requeridas.
# - POR QUÉ LO HACE: Para asegurar que la fecha límite ingresada sea futura
#   antes de calcular el desglose temporal de cuotas.
# - PARA QUÉ SIRVE: Para mostrar el plan personalizado con fecha límite en la
#   subsección "Meta Definida" del Módulo 4.
# ==============================================================================
@app.route("/plan-definido", methods=["POST"])
def plan_definido():
    es_valido, datos, errores = validaciones.validar_meta_definida(request.form)
    if not es_valido:
        return renderizar_panel(seccion="planes", subseccion="definida", form_data=request.form, errores=errores)

    resultado = logica.calcular_meta_definida(
        datos["nombre"],
        datos["meta"],
        datos["costo_meta"],
        datos["fecha_limite"],
        datos["tipo_ingreso"],
        datos["ingreso_usuario"],
        datos["gastos_mensuales"]
    )
    return renderizar_panel(seccion="planes", subseccion="definida", form_data=request.form, resultado_plan_definido=resultado)


# ==============================================================================
# FUNCIÓN: plan_indefinido (Ruta POST "/plan-indefinido")
# - QUÉ HACE: Valida los datos del formulario de meta sin fecha fija y ejecuta
#   `logica.calcular_meta_indefinida` para estimar cuántos meses y en qué fecha
#   exacta se alcanzará el monto deseado.
# - POR QUÉ LO HACE: Para verificar primero que la cuota mensual deseada no
#   supere el excedente real (ingresos menos gastos) del usuario.
# - PARA QUÉ SIRVE: Para responder al formulario de la subsección "Meta
#   Indefinida (Tiempo)" del Módulo 4.
# ==============================================================================
@app.route("/plan-indefinido", methods=["POST"])
def plan_indefinido():
    es_valido, datos, errores = validaciones.validar_meta_indefinida(request.form)
    if not es_valido:
        return renderizar_panel(seccion="planes", subseccion="indefinida", form_data=request.form, errores=errores)

    resultado = logica.calcular_meta_indefinida(
        datos["nombre"],
        datos["meta_dinero"],
        datos["ingreso_mensual"],
        datos["gastos_mensuales"],
        datos["ahorro_mensual"]
    )
    return renderizar_panel(seccion="planes", subseccion="indefinida", form_data=request.form, resultado_plan_indefinido=resultado)


# ==============================================================================
# FUNCIÓN: crud_crear (Ruta POST "/crud/crear")
# - QUÉ HACE: Valida los datos de un nuevo registro y, si son válidos, ordena
#   a `persistencia.crear_registro` insertarlo en la matriz de `registros.txt`,
#   redirigiendo luego al panel CRUD con un mensaje de confirmación.
# - POR QUÉ LO HACE: Utiliza el patrón Post/Redirect/Get (`redirect(url_for(...))`)
#   para evitar que al recargar la página en el navegador el registro se
#   duplique accidentalmente.
# - PARA QUÉ SIRVE: Para guardar registros nuevos en la matriz tanto desde el
#   modal "Nuevo Registro Manual" como desde los botones "Guardar en Matriz CRUD"
#   de todos los módulos de cálculo.
# ==============================================================================
@app.route("/crud/crear", methods=["POST"])
def crud_crear():
    es_valido, datos, errores = validaciones.validar_registro_crud(request.form)
    if not es_valido:
        return renderizar_panel(seccion="crud", form_data=request.form, errores=errores)

    persistencia.crear_registro(datos["nombre"], datos["tipo"], datos["monto"])
    return redirect(url_for("index", seccion="crud", msg="Registro guardado exitosamente en la matriz."))


# ==============================================================================
# FUNCIÓN: crud_actualizar (Ruta POST "/crud/actualizar")
# - QUÉ HACE: Valida los datos del modal de edición y llama a
#   `persistencia.actualizar_registro` para modificar la fila correspondiente
#   en la matriz de almacenamiento.
# - POR QUÉ LO HACE: Para permitir cambios sobre un registro existente
#   verificando antes que el nuevo monto y nombre cumplan las reglas de negocio.
# - PARA QUÉ SIRVE: Para procesar el formulario de edición del Panel CRUD.
# ==============================================================================
@app.route("/crud/actualizar", methods=["POST"])
def crud_actualizar():
    es_valido, datos, errores = validaciones.validar_actualizacion_crud(request.form)
    if not es_valido:
        return renderizar_panel(seccion="crud", form_data=request.form, errores=errores)

    exito = persistencia.actualizar_registro(
        datos["id_registro"],
        datos["nombre"],
        datos["tipo"],
        datos["monto"]
    )
    msg = (
        f"Registro #{datos['id_registro']} actualizado correctamente."
        if exito else f"No se encontró el registro #{datos['id_registro']} para actualizar."
    )
    return redirect(url_for("index", seccion="crud", msg=msg))


# ==============================================================================
# FUNCIÓN: crud_eliminar (Ruta POST "/crud/eliminar")
# - QUÉ HACE: Lee el `id_registro` enviado por el formulario de baja y solicita
#   a `persistencia.eliminar_registro` remover esa fila de la matriz.
# - POR QUÉ LO HACE: Porque las operaciones destructivas deben realizarse
#   mediante peticiones POST y no GET por seguridad web.
# - PARA QUÉ SIRVE: Para eliminar una fila específica desde la tabla del CRUD.
# ==============================================================================
@app.route("/crud/eliminar", methods=["POST"])
def crud_eliminar():
    id_registro = request.form.get("id_registro", "").strip()
    if id_registro:
        persistencia.eliminar_registro(id_registro)
    return redirect(url_for("index", seccion="crud", msg=f"Registro #{id_registro} eliminado de la matriz."))


# ==============================================================================
# FUNCIÓN: crud_limpiar (Ruta POST "/crud/limpiar")
# - QUÉ HACE: Llama a `persistencia.eliminar_todos_los_registros()` para vaciar
#   toda la matriz de registros y redirige al panel CRUD.
# - POR QUÉ LO HACE: Para ofrecer una forma rápida de reiniciar la matriz de
#   datos tras la confirmación del usuario.
# - PARA QUÉ SIRVE: Para dar funcionalidad al botón "Vaciar Todo" en el CRUD.
# ==============================================================================
@app.route("/crud/limpiar", methods=["POST"])
def crud_limpiar():
    persistencia.eliminar_todos_los_registros()
    return redirect(url_for("index", seccion="crud", msg="Todos los registros han sido eliminados de la matriz."))


# ==============================================================================
# FUNCIÓN: error_404 (Manejador de error HTTP 404)
# - QUÉ HACE: Captura cualquier intento de entrar a una ruta URL que no exista
#   y redirige amigablemente al usuario al Dashboard mostrando un aviso.
# - POR QUÉ LO HACE: Para evitar que Flask muestre la página de error genérica
#   en inglés ("Not Found") y mantener al usuario dentro de la interfaz.
# - PARA QUÉ SIRVE: Para mejorar la experiencia de usuario y tolerancia a fallos
#   de navegación.
# ==============================================================================
@app.errorhandler(404)
def error_404(e):
    return renderizar_panel(
        seccion="dashboard",
        errores=["La página solicitada no existe. Se le ha redirigido al panel principal."]
    ), 404


# ==============================================================================
# FUNCIÓN: error_500 (Manejador de error HTTP 500)
# - QUÉ HACE: Intercepta cualquier fallo interno inesperado del servidor y
#   renderiza el Dashboard con un mensaje controlado en lugar de colapsar.
# - POR QUÉ LO HACE: Por seguridad y robustez, nunca se deben exponer trazas
#   de código internas al usuario final si ocurre una excepción imprevista.
# - PARA QUÉ SIRVE: Como red de seguridad final de la aplicación web.
# ==============================================================================
@app.errorhandler(500)
def error_500(e):
    return renderizar_panel(
        seccion="dashboard",
        errores=["Ocurrió un error interno en el servidor. Por favor verifique los datos ingresados."]
    ), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
