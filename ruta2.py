# simulador de rutas simple con trafico temporal 
import random
import time

# nombres de terrenos
CAMINO = "camino"
EDIFICIO = "edificio"
AGUA = "agua"
BLOQUEO_TEMPORAL = "trafico"

# cómo se ve cada tipo de terreno en el mapa
DIBUJOS = {
    CAMINO: '.',
    EDIFICIO: 'X',
    AGUA: '~',
    BLOQUEO_TEMPORAL: '?'
}

# genera un mapa lleno de caminos
def crear_mapa(filas, columnas):
    return [[CAMINO for _ in range(columnas)] for _ in range(filas)]

# muestra el mapa en consola
def mostrar_mapa(mapa, ruta=None, inicio=None, destino=None):
    for fila in range(len(mapa)):
        linea = ""
        for col in range(len(mapa[0])):
            if inicio == (fila, col):
                linea += 'E'
            elif destino == (fila, col):
                linea += 'S'
            elif ruta and (fila, col) in ruta:
                linea += '*'
            else:
                linea += DIBUJOS[mapa[fila][col]]
        print(linea)
    print()

# le pregunta al usuario el tamaño del mapa
def pedir_tamano():
    filas = int(input("¿Cuántas filas tendrá el mapa? "))
    columnas = int(input("¿Y cuántas columnas? "))
    return filas, columnas

# deja que el usuario agregue obstáculos
def agregar_obstaculos(mapa):
    print("agregá obstáculos (escribí 'listo' para terminar):")
    while True:
        entrada = input("obstáculo en fila,columna: ")
        if entrada.lower() == 'listo':
            break
        try:
            fila, col = map(int, entrada.split(','))
            if 0 <= fila < len(mapa) and 0 <= col < len(mapa[0]):#porque mapa tiene [0]
                mapa[fila][col] = EDIFICIO
        except:
            print("formato inválido. Ejemplo válido: 2,3")

# permite agregar agua
def agregar_agua(mapa):
    print("agregá zonas de agua (escribí 'listo' para terminar):")
    while True:
        entrada = input("agua en fila,columna: ")
        if entrada.lower() == 'listo':
            break
        try:
            fila, col = map(int, entrada.split(','))
            if 0 <= fila < len(mapa) and 0 <= col < len(mapa[0]):#porque mapa tiene [0]
                if mapa[fila][col] == CAMINO:
                    mapa[fila][col] = AGUA
        except:
            print("formato inválido. ejemplo válido: 4,1")

# verifica si una celda es un camino libre
def coordenada_valida(mapa, x, y):
    return 0 <= x < len(mapa) and 0 <= y < len(mapa[0]) and mapa[x][y] == CAMINO

# pide una coordenada válida al usuario
def pedir_coordenada(mensaje, mapa):
    while True:
        entrada = input(mensaje)
        try:
            x, y = map(int, entrada.split(','))
            if coordenada_valida(mapa, x, y):
                return x, y
        except:
            pass
        print("coordenada inválida. probá otra vez. Ej: 1,5")

# algoritmo BFS para buscar camino más corto
def bfs(mapa, inicio, destino, permitir_agua=False):
    filas, columnas = len(mapa), len(mapa[0])
    visitado = [[False] * columnas for _ in range(filas)]
    anterior = [[None] * columnas for _ in range(filas)]
    cola = [inicio]
    visitado[inicio[0]][inicio[1]] = True

    while cola:
        x, y = cola.pop(0)
        if (x, y) == destino:
            camino = []
            while (x, y) != inicio:
                camino.append((x, y))
                x, y = anterior[x][y]
            camino.append(inicio)
            return camino[::-1]

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                if not visitado[nx][ny]:
                    terreno = mapa[nx][ny]
                    if terreno == CAMINO or (permitir_agua and terreno == AGUA):
                        visitado[nx][ny] = True
                        anterior[nx][ny] = (x, y)
                        cola.append((nx, ny))
    return None

# simula tráfico temporal
def simular_trafico(mapa, cantidad, duracion):
    print("simulando tráfico en algunas zonas...")
    bloqueos = []
    for _ in range(cantidad):
        x = random.randint(0, len(mapa)-1)
        y = random.randint(0, len(mapa[0])-1)
        if mapa[x][y] == CAMINO:
            mapa[x][y] = BLOQUEO_TEMPORAL
            bloqueos.append((x, y))

    mostrar_mapa(mapa)
    time.sleep(duracion)

    for x, y in bloqueos:
        mapa[x][y] = CAMINO
    print("El tráfico fue despejado.\n")

# funcion principal
def main():
    print("Bienvenido al Creador de Rutas de Liam")
    filas, columnas = pedir_tamano()
    mapa = crear_mapa(filas, columnas)
    mostrar_mapa(mapa)

    agregar_obstaculos(mapa)
    agregar_agua(mapa)
    mostrar_mapa(mapa)

    inicio = pedir_coordenada("¿Dónde comenzás? (fila,col): ", mapa)
    destino = pedir_coordenada("¿A dónde querés llegar? (fila,col): ", mapa)

    while True:
        simular_trafico(mapa, 4, 2)
        ruta = bfs(mapa, inicio, destino, permitir_agua=False)
        if not ruta:
            ruta = bfs(mapa, inicio, destino, permitir_agua=True)

        if ruta:
            print("¡Ruta encontrada!")
            mostrar_mapa(mapa, ruta, inicio, destino)
        else:
            print("No se pudo encontrar un camino válido.")
            mostrar_mapa(mapa, None, inicio, destino)

        seguir = input("¿Querés intentar otro turno? (s/n): ")
        if seguir.lower() != 's':
            break

main()
