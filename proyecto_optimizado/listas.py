def crear_lista():
    return []


def agregar_elemento(lista, registro):
    lista.append(registro)
    return True


def mostrar_lista(lista):
    return lista.copy()


def buscar_por_id(lista, id_registro):
    id_str = str(id_registro)
    for registro in lista:
        if str(registro.get("id")) == id_str:
            return registro
    return None


def actualizar_elemento(lista, id_registro, nuevos_datos):
    registro = buscar_por_id(lista, id_registro)
    if registro is None:
        return False
    registro.update(nuevos_datos)
    return True


def eliminar_elemento(lista, id_registro):
    id_str = str(id_registro)
    for posicion, registro in enumerate(lista):
        if str(registro.get("id")) == id_str:
            lista.pop(posicion)
            return True
    return False


def filtrar_por_tipo(lista, tipo):
    tipo_buscado = tipo.lower()
    return [reg for reg in lista if reg.get("tipo", "").lower() == tipo_buscado]


def obtener_monto_numerico(registro):
    return float(registro.get("monto", 0))


def ordenar_por_monto(lista):
    return sorted(lista, key=obtener_monto_numerico)


def cantidad_elementos(lista):
    return len(lista)


def lista_vacia(lista):
    return len(lista) == 0


def limpiar_lista(lista):
    lista.clear()
