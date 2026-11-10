"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""
from arkanoid_core import *
# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #

@arkanoid_method
def cargar_nivel(self) -> list[str]:
    """Lee el fichero de nivel y devuelve la cuadrícula como lista de filas."""
    # - Comprueba que `self.level_path` existe y es fichero.
    # - Lee su contenido, filtra líneas vacías y valida que todas tienen el mismo ancho.
    # - Guarda el resultado en `self.layout` y devuélvelo.
    if not self.level_path.is_file():
        raise FileNotFoundError(f"No existe el nivel: {self.level_path}")
    
    res = []
    with open(self.level_path, encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                res.append(linea)
    if not res:
        raise ValueError("El nivel esta vacio")
    ancho = len(res[0])
    for fila in res:
        if len(fila) != ancho:
            raise ValueError("no todas las filas miden lo mismo")

    self.layout = res
    return self.layout


@arkanoid_method
def preparar_entidades(self) -> None:
    """Posiciona paleta y bola, y reinicia puntuación y vidas."""
    # - Ajusta el tamaño de `self.paddle` y céntrala usando `midbottom`.
    self.paddle.size = self.PADDLE_SIZE
    self.paddle.midbottom = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - self.PADDLE_OFFSET)
    # - Reinicia `self.score`, `self.lives` y `self.end_message`.
    self.score = 0
    self.lives= 3
    self.end_message = ""
    # - Llama a `self.reiniciar_bola()` para colocar la bola sobre la paleta.
    self.reiniciar_bola()

@arkanoid_method
def crear_bloques(self) -> None:
    """Genera los rectángulos de los bloques en base a la cuadrícula."""
    # - Limpia `self.blocks`, `self.block_colors` y `self.block_symbols`.
    self.blocks = []
    self.block_colors = []
    self.block_symbols = []
    # - Recorre `self.layout` para detectar símbolos de bloque.
    # - Usa `self.calcular_posicion_bloque` y rellena las listas paralelas.
    for fila in range(len(self.layout)):
        for columna in range(len(self.layout[fila])):
            simbolo = self.layout[fila][columna]
            if simbolo in self.BLOCK_COLORS:
                rect = self.calcular_posicion_bloque(fila, columna)
                self.blocks.append(rect)
                self.block_colors.append(self.BLOCK_COLORS[simbolo])
                self.block_symbols.append(simbolo)



@arkanoid_method
def procesar_input(self) -> None:
    """Gestiona la entrada de teclado para mover la paleta."""
    # - Obtén el estado de teclas con `self.obtener_estado_teclas()`.
    teclas = self.obtener_estado_teclas()
    # - Desplaza la paleta con `self.PADDLE_SPEED` si se pulsan las teclas izquierda/derecha.
    movimiento = 0
    if teclas[self.KEY_LEFT] or teclas[self.KEY_A]:
        movimiento -= self.PADDLE_SPEED
    if teclas[self.KEY_RIGHT] or teclas[self.KEY_D]:
        movimiento += self.PADDLE_SPEED

    self.paddle.x += movimiento
    # - Limita la posición para que no salga de la pantalla.
    self.paddle.left = max(0, self.paddle.left)
    self.paddle.right = min(self.SCREEN_WIDTH, self.paddle.right)

@arkanoid_method
def actualizar_bola(self) -> None:
    """Actualiza la posición de la bola y resuelve colisiones."""
    # - Suma `self.ball_velocity` a `self.ball_pos` y genera `ball_rect` con `self.obtener_rect_bola()`.
    self.ball_pos += self.ball_velocity
    ball_rect = self.obtener_rect_bola()

    # - Gestiona rebotes con paredes, paleta y bloques, modificando velocidad y puntuación.
    if ball_rect.left <= 0:
        self.ball_velocity.x = abs(self.ball_velocity.x)
    if ball_rect.right >= self.SCREEN_WIDTH:
        self.ball_velocity.x = -abs(self.ball_velocity.x)
    if ball_rect.top <= 0:
        self.ball_velocity.y = abs(self.ball_velocity.y)

    if ball_rect.colliderect(self.paddle) and self.ball_velocity.y > 0:
        desplazamiento = (self.ball_pos.x - self.paddle.centerx) / (self.paddle.width / 2)
        direccion = Vector2(desplazamiento, -1)
        self.ball_velocity = direccion.normalize() * self.BALL_SPEED


    for i in range(len(self.blocks)):
        if ball_rect.colliderect(self.blocks[i]):
            simbolo = self.block_symbols[i]
            self.score += self.BLOCK_POINTS[simbolo]
            self.blocks.pop(i)
            self.block_colors.pop(i)
            self.block_symbols.pop(i)
            self.ball_velocity.y = -self.ball_velocity.y
            break

    # - Controla fin de nivel cuando no queden bloques y resta vidas si la bola cae.
    if len(self.blocks) == 0:
        self.end_message = "Has ganado!"
    if ball_rect.top > self.SCREEN_HEIGHT:
        self.lives -= 1
        if self.lives > 0:
            self.reiniciar_bola()
        else:
            self.end_message = "Has perdido"

@arkanoid_method
def dibujar_escena(self) -> None:
    """Renderiza fondo, bloques, paleta, bola y HUD."""
    # - Rellena el fondo y dibuja cada bloque con `self.dibujar_rectangulo`.
    self.screen.fill(self.BACKGROUND_COLOR)

    for i in range(len(self.blocks)):
        self.dibujar_rectangulo(self.blocks[i], self.block_colors[i])
    # - Pinta la paleta y la bola con las utilidades proporcionadas.
    self.dibujar_rectangulo(self.paddle, self.PADDLE_COLOR)
    self.dibujar_circulo((int(self.ball_pos.x), int(self.ball_pos.y)), self.BALL_RADIUS, self.BALL_COLOR)
    # - Muestra puntuación, vidas y mensajes usando `self.dibujar_texto`.
    self.dibujar_texto(f"Puntos: {self.score}", (10, 10))
    self.dibujar_texto(f"Vidas: {self.lives}", (self.SCREEN_WIDTH -100, 10))

    if self.end_message:
        self.dibujar_texto(self.end_message, (self.SCREEN_WIDTH // 2 -100, self.SCREEN_HEIGHT //  2), grande=True)


@arkanoid_method
def run(self) -> None:
    """Ejecuta el bucle principal del juego."""
    # - Inicializa recursos (`self.inicializar_pygame`, `self.cargar_nivel`, etc.).
    self.inicializar_pygame()
    self.cargar_nivel()
    self.crear_bloques()
    self.preparar_entidades()
    # - Procesa eventos de `self.iterar_eventos()` y llama a los métodos de actualización/dibujo.
    self.running = True
    while self.running:
        for evento in self.iterar_eventos():
            if evento.type == self.EVENT_QUIT:
                self.running = False
            elif evento.type == self.EVENT_KEYDOWN and evento.key == self.KEY_ESCAPE:
                self.running = False

        self.procesar_input()
        self.actualizar_bola()

        # - Refresca la pantalla con `self.actualizar_pantalla()` y cierra con `self.finalizar_pygame()`.
        self.dibujar_escena()
        self.actualizar_pantalla()
        self.clock.tick(self.FPS)
        if self.end_message:
            self.esperar(2000)
            self.running = False
    self.finalizar_pygame()


def main() -> None:
    """Permite ejecutar el juego desde la línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plantilla del hito M2: Arkanoid con pygame.",
    )
    parser.add_argument(
        "level",
        type=str,
        help="Ruta al fichero de nivel (texto con # para bloques y . para huecos).",
    )
    args = parser.parse_args()

    game = ArkanoidGame(args.level)
    game.run()

if __name__ == "__main__":
    main()

