import math
from datetime import date


# ==============================================================================
# FUNCIÓN: calcular_balance_gastos
# - QUÉ HACE: Suma todos los gastos mensuales del usuario, calcula el saldo
#   sobrante, determina qué porcentaje del ingreso representan los gastos y
#   clasifica la situación en un semáforo financiero (verde <= 70%, amarillo
#   < 90%, rojo >= 90%).
# - POR QUÉ LO HACE: Porque un usuario necesita conocer de forma visual e
#   inmediata qué proporción de su ingreso se consume en gastos corrientes
#   para prevenir el sobreendeudamiento.
# - PARA QUÉ SIRVE: Para alimentar el Módulo 1 (Cálculo de Gastos) con el
#   diagnóstico financiero y el nivel de alerta preventiva.
# ==============================================================================
def calcular_balance_gastos(nombre, capital, servicios_basicos, servicios_cable, otros_gastos):
    total_gastos = servicios_basicos + servicios_cable + otros_gastos
    saldo_restante = capital - total_gastos
    porcentaje_gastos = (total_gastos / capital) * 100.0 if capital > 0 else 0.0

    if total_gastos <= (capital * 0.70):
        nivel = "green"
        alerta = "EXCELENTE! Tus gastos estan bajo control, tienes un margen amplio para el ahorro y las emergencias"
        estado = "Bajo Control"
    elif total_gastos < (capital * 0.90):
        nivel = "amber"
        alerta = "Advertencia: Presupuesto ajustado, estas utilizando gran parte de tus ingresos en Gastos corrientes"
        estado = "Presupuesto Ajustado"
    else:
        nivel = "red"
        alerta = "CUIDADO! tus gastos pueden igualar o superar tu capital, estas en riesgo de endeudamiento"
        estado = "Riesgo de Endeudamiento"

    return {
        "nombre": nombre,
        "capital": capital,
        "servicios_basicos": servicios_basicos,
        "servicios_cable": servicios_cable,
        "otros_gastos": otros_gastos,
        "total_gastos": round(total_gastos, 2),
        "saldo_restante": round(saldo_restante, 2),
        "porcentaje_gastos": round(porcentaje_gastos, 2),
        "nivel": nivel,
        "alerta": alerta,
        "estado": estado
    }


# ==============================================================================
# FUNCIÓN: calcular_ahorro_mensual
# - QUÉ HACE: Evalúa si el usuario es apto para ahorrar según sus gastos y
#   distribuye su capital aplicando las reglas financieras:
#   * Regla 60/25/15 si gasta <= 60% de lo que gana (25% de ahorro).
#   * Regla 70/20/10 si gasta entre 60% y < 70% de lo que gana (20% de ahorro).
#   * Bloqueo de ahorro (No Apto) si gasta >= 70% de su ingreso.
# - POR QUÉ LO HACE: Porque forzar un ahorro cuando los gastos fijos superan
#   el 70% del ingreso deja al usuario sin liquidez básica; por eso adapta la
#   fórmula porcentual a su verdadera capacidad financiera.
# - PARA QUÉ SIRVE: Para calcular los montos exactos de Necesidades, Ahorro
#   y Gustos en el Módulo 2 y servir de base para la proyección anual.
# ==============================================================================
def calcular_ahorro_mensual(nombre, capital, servicios_basicos, servicios_cable, otros_gastos):
    total_gastos = servicios_basicos + servicios_cable + otros_gastos
    saldo_restante = capital - total_gastos

    if total_gastos <= (capital * 0.60):
        valor_necesidades = capital * 0.60
        ahorro_generado = capital * 0.25
        valor_gustos = capital * 0.15
        regla = "60/25/15"
        mensaje = "¡EXCELENTE! Puedes iniciar un plan de ahorro completo. Debido a que gastas menos del 60% de lo que ganas."
        nivel = "green"
        apto = True
    elif total_gastos < (capital * 0.70):
        valor_necesidades = capital * 0.70
        ahorro_generado = capital * 0.20
        valor_gustos = capital * 0.10
        regla = "70/20/10"
        mensaje = "Advertencia: Presupuesto ajustado, se programará el ahorro mínimo. Debido a que gastas más del 60% pero menos del 70% de lo que ganas."
        nivel = "amber"
        apto = True
    else:
        valor_necesidades = total_gastos
        ahorro_generado = 0.0
        valor_gustos = 0.0
        regla = "Sin plan aplicable"
        mensaje = "Lo sentimos pero no cuentas con los requisitos para iniciar un ahorro. Tus gastos superan más del 70% de tu capital."
        nivel = "red"
        apto = False

    return {
        "nombre": nombre,
        "capital": capital,
        "total_gastos": round(total_gastos, 2),
        "saldo_restante": round(saldo_restante, 2),
        "necesidades": round(valor_necesidades, 2),
        "ahorro": round(ahorro_generado, 2),
        "gustos": round(valor_gustos, 2),
        "regla": regla,
        "mensaje": mensaje,
        "nivel": nivel,
        "apto": apto
    }


# ==============================================================================
# FUNCIÓN: calcular_ahorro_anual
# - QUÉ HACE: Reutiliza el cálculo de ahorro mensual para obtener la cuota fija
#   y construye una MATRIZ BIDIMENSIONAL de 12 filas por 3 columnas:
#   [numero_mes, cuota_fija_mensual, total_acumulado_hasta_ese_mes].
# - POR QUÉ LO HACE: Porque al reutilizar `calcular_ahorro_mensual` evitamos
#   duplicar las reglas 60/25/15 y 70/20/10, y al usar una estructura matricial
#   [12 x 3] representamos formalmente la serie temporal mes a mes en memoria.
# - PARA QUÉ SIRVE: Para mostrar la tabla de proyección de 12 meses en el
#   Módulo 3 (Ahorro Anual con Modelo Matricial).
# ==============================================================================
def calcular_ahorro_anual(nombre, capital, servicios_basicos, servicios_cable, otros_gastos):
    base = calcular_ahorro_mensual(nombre, capital, servicios_basicos, servicios_cable, otros_gastos)
    cuota_fija = base["ahorro"]
    matriz_proyeccion = []
    total_acumulado = 0.0

    if base["apto"]:
        for mes in range(1, 13):
            total_acumulado += cuota_fija
            matriz_proyeccion.append([mes, round(cuota_fija, 2), round(total_acumulado, 2)])

    mensaje_anual = base["mensaje"].replace("plan de ahorro completo.", "plan de ahorro completo anual.")

    return {
        "nombre": nombre,
        "capital": capital,
        "total_gastos": base["total_gastos"],
        "saldo_restante": base["saldo_restante"],
        "cuota_fija": round(cuota_fija, 2),
        "total_acumulado": round(total_acumulado, 2),
        "regla": base["regla"],
        "mensaje": mensaje_anual,
        "nivel": base["nivel"],
        "apto": base["apto"],
        "matriz": matriz_proyeccion
    }


# ==============================================================================
# FUNCIÓN: calcular_meta_definida
# - QUÉ HACE: Calcula cuánto debe ahorrar el usuario por día, por semana y por
#   mes para alcanzar un monto objetivo antes de una fecha límite específica,
#   normalizando su ingreso (quincenal x 2 o mensual) y activando una alerta
#   si sus gastos fijos superan el 50% de sus ingresos.
# - POR QUÉ LO HACE: Porque para metas con fecha fija (ej. pagar matrícula o
#   comprar equipo), la incógnita es la cuota periódica necesaria según el
#   tiempo exacto disponible entre la fecha actual y la fecha límite.
# - PARA QUÉ SIRVE: Para generar el reporte de cuotas diarias, semanales y
#   mensuales en la pestaña "Meta Definida" del Módulo 4.
# ==============================================================================
def calcular_meta_definida(nombre, meta, costo_meta, fecha_limite_date, tipo_ingreso, ingreso_usuario, gastos_mensuales):
    ingreso_mensual = ingreso_usuario * 2.0 if tipo_ingreso == "quincenal" else ingreso_usuario

    alerta_financiera = gastos_mensuales > (ingreso_mensual * 0.50)
    mensaje_alerta = (
        "¡ALERTA FINANCIERA! Tus gastos mensuales superan el 50% de tus ingresos. "
        "Por tu bienestar financiero, no es recomendable iniciar este plan de ahorro. "
        "Intenta reducir tus gastos primero."
        if alerta_financiera else ""
    )

    dias_restantes = (fecha_limite_date - date.today()).days
    semanas_restantes = dias_restantes / 7.0
    meses_restantes = dias_restantes / 30.41

    ahorro_diario = costo_meta / dias_restantes
    ahorro_semanal = costo_meta / semanas_restantes
    ahorro_mensual = costo_meta / meses_restantes
    porcentaje_ingreso = (ahorro_mensual / ingreso_mensual) * 100.0

    return {
        "nombre": nombre,
        "meta": meta,
        "costo_meta": round(costo_meta, 2),
        "fecha_limite": fecha_limite_date.strftime("%d/%m/%Y"),
        "tipo_ingreso": tipo_ingreso,
        "ingreso_mensual": round(ingreso_mensual, 2),
        "gastos_mensuales": round(gastos_mensuales, 2),
        "dias_restantes": dias_restantes,
        "semanas_restantes": round(semanas_restantes, 1),
        "meses_restantes": round(meses_restantes, 1),
        "ahorro_diario": round(ahorro_diario, 2),
        "ahorro_semanal": round(ahorro_semanal, 2),
        "ahorro_mensual": round(ahorro_mensual, 2),
        "porcentaje_ingreso": round(porcentaje_ingreso, 2),
        "alerta_financiera": alerta_financiera,
        "mensaje_alerta": mensaje_alerta
    }


# ==============================================================================
# FUNCIÓN: calcular_fecha_futura
# - QUÉ HACE: Suma una cantidad entera de meses a una fecha base usando
#   aritmética modular (división entera `// 12` para los años y módulo `% 12`
#   para el mes resultante) y devuelve el texto "Mes de Año" en español.
# - POR QUÉ LO HACE: Porque en Python el módulo estándar `datetime` no permite
#   sumar meses directamente con `timedelta`, y usar aritmética modular evita
#   instalar librerías externas pesadas.
# - PARA QUÉ SIRVE: Para traducir un número de meses (ej. 14 meses) en una
#   fecha comprensible para el usuario (ej. "Enero de 2028").
# ==============================================================================
def calcular_fecha_futura(fecha_base, meses):
    meses_nombres = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    total_meses = (fecha_base.month - 1) + meses
    nuevo_ano = fecha_base.year + (total_meses // 12)
    nuevo_mes = total_meses % 12
    return f"{meses_nombres[nuevo_mes]} de {nuevo_ano}"


# ==============================================================================
# FUNCIÓN: calcular_meta_indefinida
# - QUÉ HACE: Calcula cuántos meses tardará el usuario en reunir una meta de
#   dinero aportando una cuota mensual elegida por él mismo, redondeando hacia
#   arriba con `math.ceil` y determinando el mes y año exacto de cumplimiento.
# - POR QUÉ LO HACE: Porque si una división da 5.2 meses, en la vida real el
#   usuario necesita 6 cuotas mensuales completas (redondeo hacia arriba) para
#   terminar de reunir el dinero sin quedar corto.
# - PARA QUÉ SIRVE: Para proyectar el tiempo estimado y la fecha de logro en
#   la subsección "Meta Indefinida (Tiempo)" del Módulo 4.
# ==============================================================================
def calcular_meta_indefinida(nombre, meta_dinero, ingreso_mensual, gastos_mensuales, ahorro_mensual):
    dinero_sobrante = ingreso_mensual - gastos_mensuales
    advertencia_50 = gastos_mensuales > (ingreso_mensual * 0.50)

    meses_exactos = meta_dinero / ahorro_mensual
    meses_enteros = int(math.ceil(meses_exactos))
    fecha_logro = calcular_fecha_futura(date.today(), meses_enteros)

    return {
        "nombre": nombre,
        "meta_dinero": round(meta_dinero, 2),
        "ingreso_mensual": round(ingreso_mensual, 2),
        "gastos_mensuales": round(gastos_mensuales, 2),
        "dinero_sobrante": round(dinero_sobrante, 2),
        "ahorro_mensual": round(ahorro_mensual, 2),
        "meses_exactos": round(meses_exactos, 2),
        "meses_enteros": meses_enteros,
        "fecha_logro": fecha_logro,
        "advertencia_50": advertencia_50
    }
