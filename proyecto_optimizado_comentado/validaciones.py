from datetime import datetime, date


# ==============================================================================
# FUNCIÓN: sanitizar_texto
# - QUÉ HACE: Convierte cualquier valor recibido en una cadena de texto y
#   elimina los espacios en blanco al inicio y al final. Si recibe None,
#   devuelve una cadena vacía "".
# - POR QUÉ LO HACE: Porque los formularios web pueden enviar campos vacíos
#   (None) o textos con espacios accidentales (ej. "  Juan  ") que alterarían
#   las comparaciones y el almacenamiento en el archivo plano.
# - PARA QUÉ SIRVE: Para limpiar y estandarizar todas las entradas de texto
#   del usuario antes de validarlas o guardarlas en la matriz.
# ==============================================================================
def sanitizar_texto(texto):
    return "" if texto is None else str(texto).strip()


# ==============================================================================
# FUNCIÓN: convertir_a_flotante
# - QUÉ HACE: Toma un valor de entrada, limpia espacios, normaliza comas o
#   puntos decimales e intenta convertirlo al tipo numérico decimal (float).
#   Retorna una tupla (exito_booleano, numero_float).
# - POR QUÉ LO HACE: Porque en distintos dispositivos o configuraciones de
#   teclado el usuario puede escribir "1,500.50" o "1500,50", y un float()
#   directo lanzaría un error ValueError que detendría el servidor.
# - PARA QUÉ SIRVE: Para garantizar que ningún dato numérico mal escrito
#   provoque una caída (Error 500) en la aplicación web.
# ==============================================================================
def convertir_a_flotante(valor):
    texto = sanitizar_texto(valor).replace(" ", "")
    if not texto:
        return False, 0.0

    if "," in texto and "." in texto:
        texto = texto.replace(",", "")
    elif "," in texto:
        texto = texto.replace(",", ".")

    try:
        return True, float(texto)
    except ValueError:
        return False, 0.0


# ==============================================================================
# FUNCIÓN: validar_numero_positivo
# - QUÉ HACE: Verifica que un valor sea un número válido y estrictamente
#   mayor que cero (> 0). Retorna (es_valido, numero, mensaje_error).
# - POR QUÉ LO HACE: Porque magnitudes como el ingreso mensual, el costo de
#   una meta o un depósito de ahorro no tienen sentido financiero si son 0
#   o negativos, y además podrían causar divisiones entre cero en la lógica.
# - PARA QUÉ SIRVE: Para proteger las fórmulas financieras que dividen entre
#   el capital o la cuota de ahorro y asegurar datos reales.
# ==============================================================================
def validar_numero_positivo(valor, nombre_campo):
    es_numero, numero = convertir_a_flotante(valor)
    if not es_numero:
        return False, 0.0, f"El campo '{nombre_campo}' debe ser un valor numérico válido."
    if numero <= 0:
        return False, 0.0, f"El campo '{nombre_campo}' debe ser mayor que cero."
    return True, numero, ""


# ==============================================================================
# FUNCIÓN: validar_numero_no_negativo
# - QUÉ HACE: Verifica que un valor sea un número válido mayor o igual a
#   cero (>= 0). Retorna (es_valido, numero, mensaje_error).
# - POR QUÉ LO HACE: Porque ciertos gastos (como cable o gastos extras) pueden
#   ser 0 si el usuario no los tiene, pero jamás pueden ser negativos.
# - PARA QUÉ SIRVE: Para validar campos de gastos opcionales permitiendo el
#   cero pero bloqueando números negativos.
# ==============================================================================
def validar_numero_no_negativo(valor, nombre_campo):
    es_numero, numero = convertir_a_flotante(valor)
    if not es_numero:
        return False, 0.0, f"El campo '{nombre_campo}' debe ser un valor numérico válido (ingrese 0 si no aplica)."
    if numero < 0:
        return False, 0.0, f"El campo '{nombre_campo}' no puede ser negativo."
    return True, numero, ""


# ==============================================================================
# FUNCIÓN: validar_datos_gastos
# - QUÉ HACE: Extrae y valida los 5 campos del formulario de presupuesto
#   (nombre, capital, servicios básicos, internet/cable y otros gastos).
#   Retorna (es_valido, diccionario_datos, lista_errores).
# - POR QUÉ LO HACE: Porque antes de realizar cualquier cálculo de balance o
#   regla de ahorro necesitamos comprobar todos los campos juntos y mostrar
#   al usuario todos los errores encontrados de una sola vez.
# - PARA QUÉ SIRVE: Para alimentar con datos limpios y seguros a los módulos
#   de Balance de Gastos, Ahorro Mensual y Ahorro Anual.
# ==============================================================================
def validar_datos_gastos(form):
    errores = []
    nombre = sanitizar_texto(form.get("nombre"))
    if not nombre:
        errores.append("El nombre y apellido no pueden estar vacíos.")

    val_cap, capital, err_cap = validar_numero_positivo(form.get("capital"), "Ingresos mensuales (capital)")
    if not val_cap:
        errores.append(err_cap)

    val_sb, servicios_basicos, err_sb = validar_numero_no_negativo(form.get("servicios_basicos"), "Servicios básicos")
    if not val_sb:
        errores.append(err_sb)

    val_sc, servicios_cable, err_sc = validar_numero_no_negativo(form.get("servicios_cable"), "Internet y Cable")
    if not val_sc:
        errores.append(err_sc)

    val_og, otros_gastos, err_og = validar_numero_no_negativo(form.get("otros_gastos"), "Otros gastos")
    if not val_og:
        errores.append(err_og)

    datos = {
        "nombre": nombre,
        "capital": capital,
        "servicios_basicos": servicios_basicos,
        "servicios_cable": servicios_cable,
        "otros_gastos": otros_gastos
    }
    return len(errores) == 0, datos, errores


# ==============================================================================
# FUNCIÓN: validar_datos_ahorro_mensual
# - QUÉ HACE: Reutiliza la función validar_datos_gastos(form) para validar
#   los datos del formulario de ahorro mensual.
# - POR QUÉ LO HACE: Porque el módulo de ahorro mensual solicita exactamente
#   los mismos parámetros de entrada que el cálculo de gastos, aplicando el
#   principio DRY (No te repitas) para evitar duplicar código.
# - PARA QUÉ SIRVE: Para mantener una interfaz clara en app.py sin repetir
#   líneas de validación.
# ==============================================================================
def validar_datos_ahorro_mensual(form):
    return validar_datos_gastos(form)


# ==============================================================================
# FUNCIÓN: validar_datos_ahorro_anual
# - QUÉ HACE: Reutiliza la función validar_datos_gastos(form) para validar
#   los parámetros del módulo de proyección anual.
# - POR QUÉ LO HACE: Porque la proyección anual parte de la misma estructura
#   de ingresos y gastos mensuales del usuario.
# - PARA QUÉ SIRVE: Para simplificar el mantenimiento del código reutilizando
#   la lógica de validación general de presupuesto.
# ==============================================================================
def validar_datos_ahorro_anual(form):
    return validar_datos_gastos(form)


# ==============================================================================
# FUNCIÓN: validar_meta_definida
# - QUÉ HACE: Valida los datos de un plan de ahorro con fecha límite (nombre,
#   meta, costo, fecha futura, frecuencia de ingreso, monto de ingreso y gastos).
# - POR QUÉ LO HACE: Porque el cálculo de cuotas diarias, semanales y mensuales
#   divide el costo entre los días restantes `(fecha_limite - hoy).days`. Si la
#   fecha fuera hoy o pasada, los días serían <= 0 provocando división por cero
#   o cuotas negativas.
# - PARA QUÉ SIRVE: Para garantizar que la fecha límite sea válida y
#   estrictamente futura, y que los montos financieros sean coherentes.
# ==============================================================================
def validar_meta_definida(form):
    errores = []
    nombre = sanitizar_texto(form.get("nombre"))
    if not nombre:
        errores.append("El nombre del titular es obligatorio.")

    meta = sanitizar_texto(form.get("meta"))
    if not meta:
        errores.append("Debe especificar la meta u objetivo de ahorro.")

    val_cm, costo_meta, err_cm = validar_numero_positivo(form.get("costo_meta"), "Costo total de la meta")
    if not val_cm:
        errores.append(err_cm)

    fecha_str = sanitizar_texto(form.get("fecha_limite"))
    fecha_limite_valida = None
    if not fecha_str:
        errores.append("Debe seleccionar una fecha límite.")
    else:
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                fecha_limite_valida = datetime.strptime(fecha_str, fmt).date()
                break
            except ValueError:
                continue

        if fecha_limite_valida is None:
            errores.append("El formato de la fecha límite no es válido (use AAAA-MM-DD o DD/MM/AAAA).")
        elif fecha_limite_valida <= date.today():
            errores.append("La fecha límite no puede pertenecer al pasado ni ser el día en curso.")

    tipo_ingreso = sanitizar_texto(form.get("tipo_ingreso")).lower()
    if tipo_ingreso not in ("mensual", "quincenal"):
        errores.append("El tipo de ingreso debe ser 'mensual' o 'quincenal'.")

    val_ing, ingreso_usuario, err_ing = validar_numero_positivo(form.get("ingreso_usuario"), "Monto de ingreso")
    if not val_ing:
        errores.append(err_ing)

    val_gm, gastos_mensuales, err_gm = validar_numero_no_negativo(form.get("gastos_mensuales"), "Total de gastos mensuales")
    if not val_gm:
        errores.append(err_gm)

    datos = {
        "nombre": nombre,
        "meta": meta,
        "costo_meta": costo_meta,
        "fecha_limite": fecha_limite_valida,
        "tipo_ingreso": tipo_ingreso,
        "ingreso_usuario": ingreso_usuario,
        "gastos_mensuales": gastos_mensuales
    }
    return len(errores) == 0, datos, errores


# ==============================================================================
# FUNCIÓN: validar_meta_indefinida
# - QUÉ HACE: Valida el formulario de meta con tiempo libre y comprueba que
#   el usuario tenga excedente positivo (ingreso > gastos) y que la cuota de
#   ahorro elegida no supere dicho excedente disponible.
# - POR QUÉ LO HACE: Porque nadie puede ahorrar una cuota mensual mayor al
#   dinero que le sobra después de pagar sus gastos mensuales.
# - PARA QUÉ SIRVE: Para asegurar la viabilidad matemática y financiera antes
#   de estimar cuántos meses tardará el usuario en alcanzar su objetivo.
# ==============================================================================
def validar_meta_indefinida(form):
    errores = []
    nombre = sanitizar_texto(form.get("nombre"))
    if not nombre:
        errores.append("El nombre del titular es obligatorio.")

    val_md, meta_dinero, err_md = validar_numero_positivo(form.get("meta_dinero"), "Meta de dinero a acumular")
    if not val_md:
        errores.append(err_md)

    val_ing, ingreso_mensual, err_ing = validar_numero_positivo(form.get("ingreso_mensual"), "Ingreso mensual")
    if not val_ing:
        errores.append(err_ing)

    val_gm, gastos_mensuales, err_gm = validar_numero_no_negativo(form.get("gastos_mensuales"), "Gastos mensuales")
    if not val_gm:
        errores.append(err_gm)

    val_ah, ahorro_mensual, err_ah = validar_numero_positivo(form.get("ahorro_mensual"), "Cuota de ahorro mensual")
    if not val_ah:
        errores.append(err_ah)

    if val_ing and val_gm:
        excedente = ingreso_mensual - gastos_mensuales
        if excedente <= 0:
            errores.append("Actualmente tus gastos son mayores o iguales a tus ingresos. No cuentas con excedente mensual para ahorrar.")
        elif val_ah and ahorro_mensual > excedente:
            errores.append(f"La cuota de ahorro mensual elegida ({ahorro_mensual:.2f} C$) no puede superar el excedente mensual disponible ({excedente:.2f} C$).")

    datos = {
        "nombre": nombre,
        "meta_dinero": meta_dinero,
        "ingreso_mensual": ingreso_mensual,
        "gastos_mensuales": gastos_mensuales,
        "ahorro_mensual": ahorro_mensual
    }
    return len(errores) == 0, datos, errores


# ==============================================================================
# FUNCIÓN: validar_registro_crud
# - QUÉ HACE: Valida los campos necesarios para insertar una nueva fila en la
#   matriz CRUD (nombre del titular, tipo de operación y monto positivo).
# - POR QUÉ LO HACE: Porque la matriz persistente en archivo de texto requiere
#   que todos los registros tengan un titular válido y un monto numérico real.
# - PARA QUÉ SIRVE: Para impedir que se guarden registros corruptos o vacíos
#   en el archivo registros.txt.
# ==============================================================================
def validar_registro_crud(form):
    errores = []
    nombre = sanitizar_texto(form.get("nombre"))
    if not nombre:
        errores.append("El nombre es requerido para guardar el registro.")

    tipo = sanitizar_texto(form.get("tipo")) or "Ahorro General"

    val_monto, monto, err_monto = validar_numero_positivo(form.get("monto"), "Monto de ahorro")
    if not val_monto:
        errores.append(err_monto)

    datos = {"nombre": nombre, "tipo": tipo, "monto": monto}
    return len(errores) == 0, datos, errores


# ==============================================================================
# FUNCIÓN: validar_actualizacion_crud
# - QUÉ HACE: Valida los datos enviados al editar un registro existente de la
#   matriz CRUD, incluyendo su identificador único (id_registro).
# - POR QUÉ LO HACE: Porque además de validar los nuevos datos (nombre, tipo,
#   monto), es indispensable contar con el ID para saber qué fila de la matriz
#   se debe modificar.
# - PARA QUÉ SIRVE: Para garantizar que la operación Update del CRUD sea
#   segura y consistente.
# ==============================================================================
def validar_actualizacion_crud(form):
    es_valido, datos, errores = validar_registro_crud(form)
    id_registro = sanitizar_texto(form.get("id_registro"))
    if not id_registro:
        errores.insert(0, "El identificador del registro es requerido.")

    datos["id_registro"] = id_registro
    datos["tipo"] = sanitizar_texto(form.get("tipo")) or "Registro Modificado"
    return len(errores) == 0, datos, errores
