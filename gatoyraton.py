import os
import time

ANCHO_TABLERO = 8
ALTO_TABLERO = 8
MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
TECLAS_MOVIMIENTO = {
    'w': (-1, 0),
    's': (1, 0),
    'a': (0, -1),
    'd': (0, 1)
}

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_tablero(pos_raton, pos_gato):
    for fila in range(ALTO_TABLERO):
        linea = ""
        for columna in range(ANCHO_TABLERO):
            posicion = (fila, columna)
            if posicion == pos_raton and posicion == pos_gato:
                linea += "💥 "
            elif posicion == pos_raton:
                linea += "🐭 "
            elif posicion == pos_gato:
                linea += "🐱 "
            else:
                linea += ". "
        print(linea)
    print()

def movimientos_validos(posicion):
    fila_actual, col_actual = posicion
    opciones = []
    for cambio_fila, cambio_columna in MOVIMIENTOS:
        nueva_fila = fila_actual + cambio_fila
        nueva_columna = col_actual + cambio_columna
        if 0 <= nueva_fila < ALTO_TABLERO and 0 <= nueva_columna < ANCHO_TABLERO:
            opciones.append((nueva_fila, nueva_columna))
    return opciones

def distancia(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def evaluar_estado(pos_raton, pos_gato):
    if pos_raton == pos_gato:
        return -1000  # el gato gana
    return distancia(pos_raton, pos_gato)

def minimax(pos_raton, pos_gato, profundidad, es_turno_raton):
    if profundidad == 0 or pos_raton == pos_gato:
        return evaluar_estado(pos_raton, pos_gato), pos_raton if es_turno_raton else pos_gato

    mejor_valor = float('-inf') if es_turno_raton else float('inf')
    mejor_movimiento = pos_raton if es_turno_raton else pos_gato

    opciones = movimientos_validos(pos_raton if es_turno_raton else pos_gato)

    for nueva_posicion in opciones:
        nueva_pos_raton = nueva_posicion if es_turno_raton else pos_raton
        nueva_pos_gato = nueva_posicion if not es_turno_raton else pos_gato

        valor, _ = minimax(nueva_pos_raton, nueva_pos_gato, profundidad -1, not es_turno_raton)

        if es_turno_raton and valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = nueva_posicion
        elif not es_turno_raton and valor < mejor_valor:
            mejor_valor = valor
            mejor_movimiento = nueva_posicion

    return mejor_valor, mejor_movimiento

def mover_gato(gato):
    while True:
        tecla = input("Movimiento del gato (w/a/s/d): ").lower()
        if tecla in TECLAS_MOVIMIENTO:
            cambio_fila, cambio_columna = TECLAS_MOVIMIENTO[tecla]
            nueva_fila = gato[0] + cambio_fila
            nueva_columna = gato[1] + cambio_columna
            if 0 <= nueva_fila < ALTO_TABLERO and 0 <= nueva_columna < ANCHO_TABLERO:
                return (nueva_fila, nueva_columna)
        print("Movimiento inválido. Usa solo w/a/s/d y no salgas del tablero.")

def jugar():
    pos_raton = (ALTO_TABLERO - 1, ANCHO_TABLERO - 1)
    pos_gato = (0, 0)
    max_turnos = 20

    for turno in range(1, max_turnos + 1):
        limpiar_consola()
        print(f"🎮 Turno {turno}")
        mostrar_tablero(pos_raton, pos_gato)

        pos_gato = mover_gato(pos_gato)
        if pos_gato == pos_raton:
            limpiar_consola()
            mostrar_tablero(pos_raton, pos_gato)
            print("💀 ¡El gato atrapó al ratón! Fin del juego.")
            return

        _, nueva_pos_raton = minimax(pos_raton, pos_gato, 3, True)
        pos_raton = nueva_pos_raton
        if pos_raton == pos_gato:
            limpiar_consola()
            mostrar_tablero(pos_raton, pos_gato)
            print("💀 ¡El gato atrapó al ratón! Fin del juego.")
            return

        time.sleep(0)  # pausa entre turnos

    limpiar_consola()
    mostrar_tablero(pos_raton, pos_gato)
    print("🎉 ¡El ratón escapó durante 20 turnos!")

# ejecutar el juego
jugar()
