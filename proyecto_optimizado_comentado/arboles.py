# ==============================================================================
# MÓDULO: arboles.py (100% Estructurado / Sin Clases ni POO)
# Representa un árbol general N-ario de categorías financieras utilizando
# diccionarios anidados con la forma: {"nombre": str, "hijos": list}
# ==============================================================================


# ==============================================================================
# FUNCIÓN: crear_nodo_arbol
# - QUÉ HACE: Crea y retorna un diccionario que representa un nodo de un árbol
#   general con dos llaves: `"nombre"` (texto) e `"hijos"` (lista vacía).
# - POR QUÉ LO HACE: Porque al no utilizar Programación Orientada a Objetos
#   (sin `class`), un diccionario nativo de Python permite modelar la misma
#   estructura jerárquica de forma más ligera, directa y rápida.
# - PARA QUÉ SIRVE: Para instanciar la raíz o cualquier categoría/subcategoría
#   financiera dentro del árbol.
# ==============================================================================
def crear_nodo_arbol(nombre):
    return {"nombre": nombre, "hijos": []}


# ==============================================================================
# FUNCIÓN: crear_arbol_financiero
# - QUÉ HACE: Inicializa el árbol financiero creando su nodo raíz (por defecto
#   llamado `"Finanzas personales"`).
# - POR QUÉ LO HACE: Porque todo árbol jerárquico necesita un punto de partida
#   único (raíz) del cual cuelguen las categorías principales y subcategorías.
# - PARA QUÉ SIRVE: Para iniciar la estructura de árbol lista para usar.
# ==============================================================================
def crear_arbol_financiero(raiz="Finanzas personales"):
    return crear_nodo_arbol(raiz)


# ==============================================================================
# FUNCIÓN: buscar_nodo
# - QUÉ HACE: Busca recursivamente un nodo por su nombre (sin importar
#   mayúsculas o minúsculas) partiendo desde `nodo_actual`.
# - POR QUÉ LO HACE: Porque un árbol tiene múltiples niveles de profundidad y
#   la recursividad (DFS) permite explorar cada rama e hijo hasta dar con el
#   nodo buscado.
# - PARA QUÉ SIRVE: Para localizar categorías padre antes de insertar una
#   subcategoría o para verificar si un nombre ya existe en el árbol.
# ==============================================================================
def buscar_nodo(nodo_actual, nombre):
    if nodo_actual is None:
        return None

    if nodo_actual["nombre"].lower() == nombre.lower():
        return nodo_actual

    for hijo in nodo_actual["hijos"]:
        encontrado = buscar_nodo(hijo, nombre)
        if encontrado is not None:
            return encontrado

    return None


# ==============================================================================
# FUNCIÓN: agregar_categoria
# - QUÉ HACE: Busca el nodo `padre` dentro del árbol `raiz`, verifica que la
#   nueva categoría `nombre` no esté duplicada y la agrega a la lista `"hijos"`
#   del padre.
# - POR QUÉ LO HACE: Para mantener la integridad del árbol evitando categorías
#   huérfanas (sin padre) o nombres repetidos en la jerarquía financiera.
# - PARA QUÉ SIRVE: Para clasificar ingresos, gastos fijos, gastos variables
#   y metas en niveles jerárquicos.
# ==============================================================================
def agregar_categoria(raiz, padre, nombre):
    nodo_padre = buscar_nodo(raiz, padre)
    if nodo_padre is None or buscar_nodo(raiz, nombre) is not None:
        return False

    nodo_padre["hijos"].append(crear_nodo_arbol(nombre))
    return True


# ==============================================================================
# FUNCIÓN: mostrar_arbol
# - QUÉ HACE: Recorre el árbol en preorden (profundidad) y construye una lista
#   de cadenas de texto con sangría proporcional al `nivel` de cada nodo.
# - POR QUÉ LO HACE: Porque una lista indentada permite visualizar claramente
#   qué subcategoría pertenece a qué categoría padre.
# - PARA QUÉ SIRVE: Para imprimir o exportar la jerarquía completa del árbol.
# ==============================================================================
def mostrar_arbol(nodo_actual, nivel=0):
    if nodo_actual is None:
        return []

    resultado = ["    " * nivel + nodo_actual["nombre"]]
    for hijo in nodo_actual["hijos"]:
        resultado.extend(mostrar_arbol(hijo, nivel + 1))
    return resultado


# ==============================================================================
# FUNCIÓN: categorias_principales
# - QUÉ HACE: Devuelve una lista con los nombres de los hijos directos de la
#   raíz del árbol (nivel 1).
# - POR QUÉ LO HACE: Porque las categorías de primer nivel representan los
#   pilares generales de las finanzas (ej. Ingresos, Gastos, Ahorros).
# - PARA QUÉ SIRVE: Para consultar rápidamente las ramas principales sin
#   recorrer todo el árbol.
# ==============================================================================
def categorias_principales(raiz):
    return [hijo["nombre"] for hijo in raiz["hijos"]]


# ==============================================================================
# FUNCIÓN: obtener_subcategorias
# - QUÉ HACE: Busca una categoría por su `nombre` y devuelve una lista con los
#   nombres de todos sus hijos directos.
# - POR QUÉ LO HACE: Para poder desglosar los componentes específicos de una
#   categoría (por ejemplo, ver qué servicios componen "Gastos Fijos").
# - PARA QUÉ SIRVE: Para consultas puntuales de subniveles dentro del árbol.
# ==============================================================================
def obtener_subcategorias(raiz, nombre):
    nodo = buscar_nodo(raiz, nombre)
    if nodo is None:
        return []
    return [hijo["nombre"] for hijo in nodo["hijos"]]


# ==============================================================================
# FUNCIÓN: eliminar_categoria
# - QUÉ HACE: Busca recursivamente una categoría por `nombre` y la elimina de
#   la lista `"hijos"` de su nodo padre junto con todas sus subcategorías.
# - POR QUÉ LO HACE: Porque en una estructura de árbol, al podar una rama
#   también deben desaparecer todos los nodos descendientes que dependían de ella.
# - PARA QUÉ SIRVE: Para remover categorías obsoletas de la jerarquía.
# ==============================================================================
def eliminar_categoria(nodo_actual, nombre):
    for hijo in nodo_actual["hijos"]:
        if hijo["nombre"].lower() == nombre.lower():
            nodo_actual["hijos"].remove(hijo)
            return True
        if eliminar_categoria(hijo, nombre):
            return True
    return False


# ==============================================================================
# FUNCIÓN: contar_nodos
# - QUÉ HACE: Cuenta recursivamente cuántos nodos existen en total dentro del
#   árbol o subárbol recibido.
# - POR QUÉ LO HACE: Suma `1` por el nodo actual más el conteo recursivo de
#   cada uno de sus hijos.
# - PARA QUÉ SIRVE: Para conocer el tamaño total de la estructura jerárquica.
# ==============================================================================
def contar_nodos(nodo_actual):
    if nodo_actual is None:
        return 0
    return 1 + sum(contar_nodos(hijo) for hijo in nodo_actual["hijos"])


# ==============================================================================
# FUNCIÓN: recorrido_profundidad
# - QUÉ HACE: Ejecuta el recorrido en profundidad (DFS Preorden) sobre la raíz
#   reutilizando `mostrar_arbol`.
# - POR QUÉ LO HACE: Para ofrecer un punto de acceso directo al algoritmo de
#   búsqueda en profundidad del árbol.
# - PARA QUÉ SIRVE: Para listar todos los nodos visitando primero cada rama
#   hasta el fondo antes de pasar a la siguiente.
# ==============================================================================
def recorrido_profundidad(raiz):
    return mostrar_arbol(raiz)
