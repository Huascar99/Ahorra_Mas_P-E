from flask import Flask, render_template, request, redirect, url_for
import logica
import validaciones
import persistencia

app = Flask(__name__)
app.secret_key = "ahorramas_clave_propia"


def renderizar_panel(seccion="dashboard", subseccion="definida", form_data=None, **kwargs):
    return render_template(
        "index.html",
        seccion_activa=seccion,
        subseccion_activa=subseccion,
        form_data=form_data if form_data is not None else {},
        matriz_crud=persistencia.obtener_todos_los_registros(),
        **kwargs
    )


@app.route("/", methods=["GET"])
def index():
    seccion = request.args.get("seccion", "dashboard")
    subseccion = request.args.get("subseccion", "definida")
    mensaje_exito = request.args.get("msg", "")
    return renderizar_panel(seccion=seccion, subseccion=subseccion, mensaje_exito=mensaje_exito)


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


@app.route("/crud/crear", methods=["POST"])
def crud_crear():
    es_valido, datos, errores = validaciones.validar_registro_crud(request.form)
    if not es_valido:
        return renderizar_panel(seccion="crud", form_data=request.form, errores=errores)

    persistencia.crear_registro(datos["nombre"], datos["tipo"], datos["monto"])
    return redirect(url_for("index", seccion="crud", msg="Registro guardado exitosamente en la matriz."))


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


@app.route("/crud/eliminar", methods=["POST"])
def crud_eliminar():
    id_registro = request.form.get("id_registro", "").strip()
    if id_registro:
        persistencia.eliminar_registro(id_registro)
    return redirect(url_for("index", seccion="crud", msg=f"Registro #{id_registro} eliminado de la matriz."))


@app.route("/crud/limpiar", methods=["POST"])
def crud_limpiar():
    persistencia.eliminar_todos_los_registros()
    return redirect(url_for("index", seccion="crud", msg="Todos los registros han sido eliminados de la matriz."))


@app.errorhandler(404)
def error_404(e):
    return renderizar_panel(
        seccion="dashboard",
        errores=["La página solicitada no existe. Se le ha redirigido al panel principal."]
    ), 404


@app.errorhandler(500)
def error_500(e):
    return renderizar_panel(
        seccion="dashboard",
        errores=["Ocurrió un error interno en el servidor. Por favor verifique los datos ingresados."]
    ), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
