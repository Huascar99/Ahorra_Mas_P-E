from datetime import datetime, date


def sanitizar_texto(texto):
    return "" if texto is None else str(texto).strip()


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


def validar_numero_positivo(valor, nombre_campo):
    es_numero, numero = convertir_a_flotante(valor)
    if not es_numero:
        return False, 0.0, f"El campo '{nombre_campo}' debe ser un valor numérico válido."
    if numero <= 0:
        return False, 0.0, f"El campo '{nombre_campo}' debe ser mayor que cero."
    return True, numero, ""


def validar_numero_no_negativo(valor, nombre_campo):
    es_numero, numero = convertir_a_flotante(valor)
    if not es_numero:
        return False, 0.0, f"El campo '{nombre_campo}' debe ser un valor numérico válido (ingrese 0 si no aplica)."
    if numero < 0:
        return False, 0.0, f"El campo '{nombre_campo}' no puede ser negativo."
    return True, numero, ""


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


def validar_datos_ahorro_mensual(form):
    return validar_datos_gastos(form)


def validar_datos_ahorro_anual(form):
    return validar_datos_gastos(form)


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


def validar_actualizacion_crud(form):
    es_valido, datos, errores = validar_registro_crud(form)
    id_registro = sanitizar_texto(form.get("id_registro"))
    if not id_registro:
        errores.insert(0, "El identificador del registro es requerido.")

    datos["id_registro"] = id_registro
    datos["tipo"] = sanitizar_texto(form.get("tipo")) or "Registro Modificado"
    return len(errores) == 0, datos, errores
